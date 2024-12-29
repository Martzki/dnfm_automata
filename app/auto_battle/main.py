import argparse
import os
import random

import yaml
from func_timeout import FunctionTimedOut

from app.auto_battle.dungeons.pirates import pirates
from app.auto_battle.dungeons.pirates.pirates import Pirates
from app.base_app import BaseApp
from common.log import Logger
from common.util import timeout_handler, get_resource_base_dir
from detector.detector import Detector
from device.device import Device
from device.scrcpy_device import ScrcpyDevice
from runtime.character.champion import Champion
from runtime.character.desperado import Desperado
from runtime.character.evangelist import Evangelist
from runtime.character.grand_master import GrandMaster
from runtime.character.hell_bringer import HellBringer
from runtime.character.noblesse import Noblesse
from runtime.character.silent_eye import SilentEye
from runtime.character.trickster import Trickster
from runtime.character.wrecking_ball import WreckingBall
from ui.ui import UIElementCtx

LOGGER = Logger(__name__).logger


class AutoBattleApp(BaseApp):
    def __init__(self, device: Device, detector: Detector, character_list: list, ui_ctx: UIElementCtx):
        super(AutoBattleApp, self).__init__(device, ui_ctx)
        self.dungeons = {
            pirates.DUNGEON_NAME: Pirates(device, detector, ui_ctx)
        }
        for dungeon in self.dungeons.values():
            dungeon.register_rooms()
        self.character_list = character_list

    def start(self):
        LOGGER.info("App started")
        LOGGER.info(f"Character list: {[c['id'] for c in self.character_list]}")

        self.mute_game(True)

        try:
            for each in self.character_list:
                dungeon = self.dungeons.get(each["dungeon"])
                if not dungeon:
                    LOGGER.error(f"Ignore {each['id']} which has unregistered dungeon config: {each['dungeon']}")
                    continue

                self.change_character(each["id"])
                self.return_to_base_scenario()
                fatigue_points = dungeon.get_fatigue_points()
                LOGGER.info(f"{each['id']}'s fatigue points: {fatigue_points}")

                character = each["character"]
                character.reserve_fatigue_points = each.get("reserve_fatigue_points", 0)
                if fatigue_points <= character.reserve_fatigue_points:
                    LOGGER.info(
                        f"Fatigue points: {fatigue_points} is not greater than "
                        f"{character.reserve_fatigue_points}, skip"
                    )
                    continue

                suit_id = each.get("suit_id", -1)
                original_suit_id = -1
                if suit_id != -1:
                    original_suit_id = self.get_current_suit_id()
                    if original_suit_id == -1:
                        LOGGER.error("Failed to get current suit id")
                        continue

                    LOGGER.info(f"Get original suit id: {original_suit_id}")
                    if original_suit_id != suit_id:
                        self.change_suit(suit_id)

                self.set_fatigue_points_config(each.get("gain_tradable_item", True),
                                               each.get("fatigue_points_burn", False))

                try:
                    self.return_to_base_scenario()
                    dungeon.repair_equipments(in_dungeon=False)
                    self.return_to_base_scenario()
                    dungeon.goto_dungeon()
                except FunctionTimedOut:
                    LOGGER.warning(f"Go to dungeon timeout, skip {each['id']}")
                    continue

                dungeon.battle(character)

                if suit_id != -1 and original_suit_id != suit_id:
                    self.change_suit(original_suit_id)
        except FunctionTimedOut as e:
            timeout_handler(f"App timeout: {e}", LOGGER.critical, self.device.last_frame)
        finally:
            self.mute_game(False)
            self.exit_game()

    def frame_handler(self, frame):
        pass


def get_character_list(device, app_config):
    init_func = {
        "champion": Champion,
        "desperado": Desperado,
        "evangelist": Evangelist,
        "hell_bringer": HellBringer,
        "grand_master": GrandMaster,
        "noblesse": Noblesse,
        "silent_eye": SilentEye,
        "trickster": Trickster,
        "wrecking_ball": WreckingBall
    }

    character_list = []
    character_map = {}
    for priority in range(3):
        sub_list = []
        for character in app_config["character"]:
            each = app_config["character"][character]
            if each["priority"] != priority:
                continue

            character_class = each["character_class"]
            each["id"] = character
            each["character"] = character_map.get(
                character_class,
                init_func[character_class](device, ui_ctx)
            )
            character_map[character_class] = each["character"]
            sub_list.append(each)

        random.shuffle(sub_list)
        character_list.extend(sub_list)

    return character_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", dest="device", type=str, help="ADB device serial")
    parser.add_argument("--conf", dest="conf", type=str, help="APP config file")
    parser.add_argument("--model-conf", dest="model_conf", type=str, help="Model config file")
    parser.add_argument("--app-conf", dest="app_conf", type=str, help="APP config file")

    args = parser.parse_args()

    with open(args.conf, "r") as config_file:
        config = yaml.load(config_file, Loader=yaml.Loader)

    with open(args.app_conf, "r") as app_config_file:
        app_config = yaml.load(app_config_file, Loader=yaml.Loader)

    with open(args.model_conf, "r") as model_config_file:
        model_yaml = yaml.load(model_config_file, Loader=yaml.Loader)
        model_config = {model: os.path.dirname(args.model_conf) + "/" + model_yaml[model] for model in model_yaml}

    device = ScrcpyDevice(args.device)
    detector = Detector(model_config)
    ui_ctx = UIElementCtx(device, detector, get_resource_base_dir(args.conf, config["ui"]["base_dir"]))
    ui_ctx.load(config["ui"])
    ui_ctx.load(app_config, get_resource_base_dir(args.app_conf, app_config["ui"]["base_dir"]))

    app = AutoBattleApp(device, detector, get_character_list(device, app_config), ui_ctx)

    app.init()

    try:
        app.start()
    finally:
        app.stop()
