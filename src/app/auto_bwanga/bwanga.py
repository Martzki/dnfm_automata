import sys
import time

import yaml

from src.app.auto_bwanga import room
from src.app.base_app import BaseApp
from src.common.log import Logger
from src.lib.character.character import Character
from src.lib.character.evangelist import Evangelist
from src.lib.character.hell_bringer import HellBringer
from src.lib.character.trickster import Trickster
from src.lib.character.wrecking_ball import WreckingBall
from src.lib.detector.detector import Detector
from src.lib.device.device import Device
from src.lib.device.scrcpy_device import ScrcpyDevice
from src.lib.dungeon.dungeon import Dungeon
from src.lib.ui.ui import UIElementCtx

LOGGER = Logger(__name__).logger


class BwangaApp(BaseApp):
    def __init__(self, device: Device, detector: Detector, character: Character, ui_ctx: UIElementCtx):
        super(BwangaApp, self).__init__(device)
        self.dungeon = Dungeon(device, detector, ui_ctx)
        self.character = character

    def init(self):
        super(BwangaApp, self).init()

    def start(self):
        LOGGER.info("App started")

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

            if room.room_id == 4:
                room.exec(self.character, room_5_visited=room_5_visited)
            else:
                room.exec(self.character)

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
    trickster = Trickster(device, ui_ctx, config["character"]["Trickster"])
    wrecking_ball = WreckingBall(device, ui_ctx, config["character"]["WreckingBall"])
    if sys.argv[2] == "0":
        c = hell_bringer
    elif sys.argv[2] == "1":
        c = evangelist
    elif sys.argv[2] == "2":
        c = trickster
    elif sys.argv[2] == "4":
        c = wrecking_ball
    app = BwangaApp(device, detector, c, ui_ctx)
    room.register_room(app)

    app.init()

    app.start()
