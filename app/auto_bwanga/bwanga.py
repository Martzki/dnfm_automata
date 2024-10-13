import argparse
import random
import time

import yaml

from app.auto_bwanga import room
from app.base_app import BaseApp
from character.character import Character
from character.evangelist import Evangelist
from character.hell_bringer import HellBringer
from character.noblesse import Noblesse
from character.silent_eye import SilentEye
from character.trickster import Trickster
from character.wrecking_ball import WreckingBall
from common.log import Logger
from common.util import timeout
from detector.detector import Detector
from device.device import Device
from device.scrcpy_device import ScrcpyDevice
from dungeon.dungeon import Dungeon
from ui.ui import UIElementCtx

LOGGER = Logger(__name__).logger


class BwangaApp(BaseApp):
    def __init__(self, device: Device, detector: Detector, character_list: list, ui_ctx: UIElementCtx):
        super(BwangaApp, self).__init__(device, ui_ctx)
        self.dungeon = Dungeon(device, detector, ui_ctx)
        self.character_list = character_list

    def init(self):
        super(BwangaApp, self).init()

    def goto_dungeon(self):
        LOGGER.info("Start to go to dungeon")

        self.repair_equipments()

        self.ui_ctx.click_ui_element(UIElementCtx.CategoryBase, "commission")
        self.ui_ctx.click_ui_element(UIElementCtx.CategoryBase, "speciality")
        self.ui_ctx.click_ui_element(UIElementCtx.CategoryBase, "speciality_ridge")
        self.ui_ctx.click_ui_element(UIElementCtx.CategoryBase, "move_to_specific_area")

        LOGGER.info("Start to move to dungeon")

        self.ui_ctx.wait_ui_element(UIElementCtx.CategoryBase, "dungeon_label_ridge", timeout=120)

        while True:
            try:
                self.ui_ctx.wait_ui_element(UIElementCtx.CategoryBase, "dungeon_label_bwanga", timeout=3)
                break
            except TimeoutError:
                self.ui_ctx.click_ui_element(UIElementCtx.CategoryBase, "dungeon_select_previous", timeout=3)
                continue

        self.ui_ctx.click_ui_element(UIElementCtx.CategoryBase, "dungeon_select_start_battle", double_check=True)

        time.sleep(1)

        if self.ui_ctx.get_ui_coordinate(UIElementCtx.CategoryBase, "dungeon_select_start_battle", use_cache=False) is not None:
            raise TimeoutError("Start battle timeout")

        LOGGER.info("Succeed to go to dungeon")

    @timeout(1800)
    def battle_in_dungeon(self, character: Character):
        dungeon_finished = False
        dungeon_finished_time = None
        room_5_visited = False
        while True:
            room = self.dungeon.get_room()
            if not room:
                if not dungeon_finished or time.time() - dungeon_finished_time < 10:
                    continue

                coordinate = self.dungeon.ui_ctx.wait_ui_element(UIElementCtx.CategoryDungeon, "exit_dungeon",
                                                                 timeout=5)
                if coordinate is None:
                    continue

                LOGGER.info("exit dungeon")
                self.device.touch(coordinate)
                return

            LOGGER.info("detect room {}".format(room.room_id))

            if room.room_id == 0:
                dungeon_finished = False

            room_args = {
                'room_5_visited': room_5_visited
            }

            try:
                room.exec(character, **room_args)
            except TimeoutError as e:
                LOGGER.info(f"room {room.room_id} timeout: {e}")
            finally:
                LOGGER.info(f"room {room.room_id} finished")

            if room.room_id == 5:
                room_5_visited = True

            if room.room_id == 8:
                LOGGER.info("Dungeon finished")
                self.dungeon.clear()
                room_5_visited = False
                dungeon_finished = True
                dungeon_finished_time = time.time()

    def start(self):
        LOGGER.info("App started")

        LOGGER.info(f"Character list: {[c['id'] for c in self.character_list]}")

        try:
            for character in self.character_list:
                self.change_character(character["id"])

                try:
                    self.goto_dungeon()
                except TimeoutError:
                    LOGGER.warning(f"Go to dungeon timeout, skip {character['id']}")
                    continue

                self.battle_in_dungeon(character["character"])
        except TimeoutError as e:
            LOGGER.fatal(f"Timeout: {e}")
            self.exit_game()

    def frame_handler(self, frame):
        pass


def get_character_list(character_config):
    init_func = {
        "Evangelist": Evangelist,
        "HellBringer": HellBringer,
        "Noblesse": Noblesse,
        "SilentEye": SilentEye,
        "Trickster": Trickster,
        "WreckingBall": WreckingBall
    }

    character_list = []
    character_map = {}
    for priority in range(3):
        sub_list = []
        for character in character_config["character"]:
            each = character_config["character"][character]
            if each["priority"] == priority:
                character_class = each["character_class"]
                each["id"] = character
                each["character"] = character_map.get(
                    character_class,
                    init_func[character_class](device, ui_ctx, config["character"][character_class])
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
    parser.add_argument("--weights", dest="weights", type=str, help="YOLO weights file")
    parser.add_argument("--character-conf", dest="character_conf", type=str, help="character config file")

    args = parser.parse_args()

    with open(args.conf, "r") as config_file:
        config = yaml.load(config_file, Loader=yaml.Loader)

    with open(args.character_conf, "r") as character_config_file:
        character_config = yaml.load(character_config_file, Loader=yaml.Loader)

    device = ScrcpyDevice(args.device)
    detector = Detector(args.weights)
    ui_ctx = UIElementCtx(device, detector)
    ui_ctx.load(config["ui"])
    ui_ctx.load(character_config)

    app = BwangaApp(device, detector, get_character_list(character_config), ui_ctx)
    room.register_room(app)

    app.init()

    app.start()
