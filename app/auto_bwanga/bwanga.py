import sys
import time

import yaml

from app.auto_bwanga import room
from app.base_app import BaseApp
from character.character import Character
from character.evangelist import Evangelist
from character.hell_bringer import HellBringer
from character.noblesse import Noblesse
from character.trickster import Trickster
from character.wrecking_ball import WreckingBall
from common.log import Logger
from detector.detector import Detector
from device.device import Device
from device.scrcpy_device import ScrcpyDevice
from dungeon.dungeon import Dungeon
from ui.ui import UIElementCtx

LOGGER = Logger(__name__).logger


class BwangaApp(BaseApp):
    def __init__(self, device: Device, detector: Detector, character: Character, ui_ctx: UIElementCtx):
        super(BwangaApp, self).__init__(device, ui_ctx)
        self.dungeon = Dungeon(device, detector, ui_ctx)
        self.character = character

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

        self.ui_ctx.click_ui_element(UIElementCtx.CategoryBase, "dungeon_select_start_battle")

        LOGGER.info("Succeed to go to dungeon")

    def start(self):
        LOGGER.info("App started")

        self.goto_dungeon()

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

            room.exec(self.character, **room_args)

            LOGGER.info(f"room {room.room_id} finished")

            if room.room_id == 5:
                room_5_visited = True

            if room.room_id == 8:
                LOGGER.info("Dungeon finished")
                self.dungeon.clear()
                room_5_visited = False
                dungeon_finished = True
                dungeon_finished_time = time.time()

    def frame_handler(self, frame):
        pass


if __name__ == '__main__':
    with open("conf/bwanga.yml", "r") as config_file:
        config = yaml.load(config_file, Loader=yaml.Loader)
    device = ScrcpyDevice(sys.argv[1])
    detector = Detector('weights/dnf.onnx')
    ui_ctx = UIElementCtx(device, detector)
    ui_ctx.load(config["ui"])
    evangelist = Evangelist(device, ui_ctx, config["character"]["Evangelist"])
    hell_bringer = HellBringer(device, ui_ctx, config["character"]["HellBringer"])
    noblesse = Noblesse(device, ui_ctx, config["character"]["Noblesse"])
    trickster = Trickster(device, ui_ctx, config["character"]["Trickster"])
    wrecking_ball = WreckingBall(device, ui_ctx, config["character"]["WreckingBall"])
    character_class = sys.argv[2]
    if character_class == "0":
        c = hell_bringer
    elif character_class == "1":
        c = evangelist
    elif character_class == "2":
        c = trickster
    elif character_class == "4":
        c = wrecking_ball
    elif character_class == "5":
        c = noblesse

    app = BwangaApp(device, detector, c, ui_ctx)
    room.register_room(app)

    app.init()

    app.start()
