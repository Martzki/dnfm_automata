import argparse
import random
import time

import yaml
from func_timeout import func_set_timeout, FunctionTimedOut

from app.auto_bwanga import room
from app.auto_bwanga.room import validate_next_room
from app.base_app import BaseApp
from character.champion import Champion
from character.character import Character
from character.evangelist import Evangelist
from character.hell_bringer import HellBringer
from character.noblesse import Noblesse
from character.silent_eye import SilentEye
from character.trickster import Trickster
from character.wrecking_ball import WreckingBall
from common.log import Logger
from common.util import timeout_handler
from detector.detector import Detector
from device.device import Device
from device.scrcpy_device import ScrcpyDevice
from dungeon.dungeon import Dungeon, DungeonReEntered, DungeonRoomChanged
from ui.ui import UIElementCtx

LOGGER = Logger(__name__).logger


class Bwanga(Dungeon):
    def goto_dungeon(self):
        LOGGER.info("Start to go to dungeon")
        self.ui_ctx.click_ui_element(UIElementCtx.CategoryCommon, "adventure")
        self.ui_ctx.click_ui_element(UIElementCtx.CategoryCommon, "adventure_reward", delay=1)
        self.ui_ctx.click_ui_element(UIElementCtx.CategoryCommon, "adventure_reward_adventure_level")
        self.ui_ctx.click_ui_element(UIElementCtx.CategoryCommon, "adventure_reward_mount_thunderime")
        self.ui_ctx.click_ui_element(UIElementCtx.CategoryCommon, "adventure_reward_move_to_area")
        self.ui_ctx.click_ui_element(UIElementCtx.CategoryDungeon, "dungeon_select_adventure_level", timeout=120)
        self.ui_ctx.click_ui_element(UIElementCtx.CategoryDungeon, "dungeon_select_bwanga")
        self.ui_ctx.wait_ui_element(UIElementCtx.CategoryDungeon, "dungeon_label_bwanga", timeout=3)
        self.ui_ctx.click_ui_element(UIElementCtx.CategoryDungeon, "dungeon_select_start_battle")
        try:
            self.wait_in_dungeon()
        except FunctionTimedOut:
            self.ui_ctx.double_check()
            self.wait_in_dungeon()

        LOGGER.info("Succeed to go to dungeon")


class BwangaApp(BaseApp):
    def __init__(self, device: Device, detector: Detector, character_list: list, ui_ctx: UIElementCtx):
        super(BwangaApp, self).__init__(device, ui_ctx)
        self.dungeon = Bwanga(device, detector, ui_ctx)
        self.character_list = character_list

    @func_set_timeout(1800)
    def battle_in_dungeon(self, character: Character):
        dungeon_finished = False
        dungeon_finished_time = None
        room_5_visited = False
        last_room_id = -1
        while True:
            room = self.dungeon.get_room()
            if not room:
                if not dungeon_finished or time.time() - dungeon_finished_time < 10:
                    continue

                try:
                    self.dungeon.ui_ctx.click_ui_element(UIElementCtx.CategoryDungeon, "exit_dungeon",
                                                         timeout=5, delay=10)
                    LOGGER.info("exit dungeon")
                    return
                except LookupError:
                    continue

            if not validate_next_room(last_room_id, room.room_id):
                continue

            LOGGER.info("detect room {}".format(room.room_id))

            if room.room_id == 0:
                dungeon_finished = False

            room_args = {
                'last_room_id': last_room_id,
                'room_5_visited': room_5_visited
            }

            dungeon_re_entered = False
            try:
                room.exec(character, **room_args)
            except FunctionTimedOut as e:
                timeout_handler(f"Timeout in room {room.room_id}: {e}", LOGGER.warning, self.device.last_frame)
                try:
                    self.dungeon.revive(room)
                except DungeonReEntered:
                    dungeon_re_entered = True
            except DungeonRoomChanged as e:
                LOGGER.info(e)
            finally:
                LOGGER.info(f"room {room.room_id} finished")
                last_room_id = -1 if dungeon_re_entered else room.room_id

            if room.room_id == 5:
                room_5_visited = True

            if room.is_last or dungeon_re_entered:
                LOGGER.info("Dungeon re-entered" if dungeon_re_entered else "Dungeon finished")
                self.dungeon.clear()
                room_5_visited = False
                dungeon_finished = True
                dungeon_finished_time = time.time()

    def start(self):
        LOGGER.info("App started")
        LOGGER.info(f"Character list: {[c['id'] for c in self.character_list]}")

        self.mute_game(True)

        try:
            for character in self.character_list:
                self.change_character(character["id"])

                try:
                    self.repair_equipments()
                    self.dungeon.goto_dungeon()
                except FunctionTimedOut:
                    LOGGER.warning(f"Go to dungeon timeout, skip {character['id']}")
                    continue

                self.battle_in_dungeon(character["character"])
        except FunctionTimedOut as e:
            timeout_handler(f"App timeout: {e}", LOGGER.critical, self.device.last_frame)
        finally:
            self.mute_game(False)
            self.exit_game()

    def frame_handler(self, frame):
        pass


def get_character_list(device, character_config):
    init_func = {
        "champion": Champion,
        "evangelist": Evangelist,
        "hell_bringer": HellBringer,
        "noblesse": Noblesse,
        "silent_eye": SilentEye,
        "trickster": Trickster,
        "wrecking_ball": WreckingBall
    }

    character_list = []
    character_map = {}
    for priority in range(3):
        sub_list = []
        for character in character_config["character"]:
            each = character_config["character"][character]
            if each["priority"] != priority:
                continue

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
    ui_ctx = UIElementCtx(device, detector, config["ui"]["base_dir"])
    ui_ctx.load(config["ui"])
    ui_ctx.load_character(character_config)

    app = BwangaApp(device, detector, get_character_list(device, character_config), ui_ctx)
    room.register_room(app)

    app.init()

    app.start()
