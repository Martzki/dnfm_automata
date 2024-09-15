import sys

import yaml

from src.app.auto_bwanga import room
from src.app.base_app import BaseApp
from src.common.log import Logger
from src.lib.character.character import Character
from src.lib.character.evangelist import Evangelist
from src.lib.character.hell_bringer import HellBringer
from src.lib.detector.detector import Detector
from src.lib.device.device import Device
from src.lib.device.scrcpy_device import ScrcpyDevice
from src.lib.dungeon.dungeon import DungeonCtx
from src.lib.ui.ui import UIElementCtx

LOGGER = Logger(__name__).logger


class BwangaApp(BaseApp):
    def __init__(self, device: Device, detector: Detector, character: Character, ui_ctx: UIElementCtx):
        super(BwangaApp, self).__init__(device)
        self.ui_ctx = ui_ctx
        self.dungeon_ctx = DungeonCtx(detector)
        self.character = character

    def start(self):
        LOGGER.info("App started")

        while True:
            frame = self.device.last_frame()
            room = self.dungeon_ctx.detect_room(frame)
            if not room:
                continue

            LOGGER.info("detect room {}".format(room.room_id))

            room.exec(self.character)

            if room.room_id == 8:
                LOGGER.info("Dungeon finished")
                self.dungeon_ctx.clear()

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
    if sys.argv[2] == "0":
        c = hell_bringer
    else:
        c = evangelist
    app = BwangaApp(device, detector, c, ui_ctx)
    room.register_room(app, config["scenario"]["dungeon"]["bwanga"], detector)

    app.init()

    app.start()
