import sys
import time

import cv2
import yaml

from src.app.auto_bwanga import room
from src.app.auto_bwanga.room import detect_room_id
from src.app.base_app import BaseApp
from src.common.log import Logger
from src.common.util import get_capture_file
from src.lib.character.character import Character
from src.lib.character.evangelist import Evangelist
from src.lib.character.hell_bringer import HellBringer
from src.lib.character.trickster import Trickster
from src.lib.detector.detector import Detector
from src.lib.device.device import Device
from src.lib.device.scrcpy_device import ScrcpyDevice
from src.lib.dungeon.dungeon import Dungeon
from src.lib.dungeon.map import DungeonMap, get_map_img
from src.lib.ui.ui import UIElementCtx

LOGGER = Logger(__name__).logger


class Bwanga(Dungeon):
    def __init__(self, detector):
        super().__init__(detector)

    def detect_room(self, frame):
        map = DungeonMap(get_map_img(frame))
        if not map or not map.valid:
            return None

        room_id = detect_room_id(map)
        if room_id == -1:
            LOGGER.warning("unknown room")
            cv2.imwrite(get_capture_file("unknown_room"), frame)

        return self.room_map.get(room_id, None)


class BwangaApp(BaseApp):
    def __init__(self, device: Device, detector: Detector, character: Character, ui_ctx: UIElementCtx):
        super(BwangaApp, self).__init__(device)
        self.ui_ctx = ui_ctx
        self.dungeon = Bwanga(detector)
        self.character = character

    def start(self):
        LOGGER.info("App started")
        input()

        exit_button_img = cv2.imread('res/scenario/base/dungeon_finish.png')
        dungeon_finished = False
        dungeon_finished_time = None
        room_5_visited = False
        while True:
            frame = self.device.last_frame()
            room = self.dungeon.detect_room(frame)
            if not room:
                if dungeon_finished and time.time() - dungeon_finished_time > 5:
                    exit_button = self.dungeon.detector.img_match(frame, [exit_button_img])
                    if exit_button.confidence > 0.9:
                        LOGGER.info("exit dungeon")
                        for i in range(3):
                            self.device.touch(exit_button.center)
                            time.sleep(0.1)
                continue

            LOGGER.info("detect room {}".format(room.room_id))

            # FIXME: when yolo map detection is ready, remove this code
            if room.room_id == 0:
                LOGGER.info("Enter new dungeon")
                dungeon_finished = False
                room_5_visited = False
                self.dungeon.clear()

            # FIXME: when yolo map detection is ready, remove this code
            if room.room_id == 3 and dungeon_finished:
                # room = self.dungeon.room_map[8]
                continue

            if dungeon_finished and time.time() - dungeon_finished_time > 5:
                exit_button = self.dungeon.detector.img_match(frame, [exit_button_img])
                if exit_button.confidence > 0.8:
                    LOGGER.info("exit dungeon")
                    for i in range(3):
                        self.device.touch(exit_button.center)
                        time.sleep(0.1)

            if room.room_id != 4:
                room.exec(self.character)
            else:
                room.exec(self.character, room_5_visited=room_5_visited)

            if room.room_id == 5:
                room_5_visited = True

            if room.room_id == 8:
                LOGGER.info("Dungeon finished")
                self.dungeon.clear()
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
    if sys.argv[2] == "0":
        c = hell_bringer
    elif sys.argv[2] == "1":
        c = evangelist
    elif sys.argv[2] == "2":
        c = trickster
    app = BwangaApp(device, detector, c, ui_ctx)
    room.register_room(app, config["scenario"]["dungeon"]["bwanga"], detector)

    app.init()

    app.start()
