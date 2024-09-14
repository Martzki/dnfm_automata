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
            if room is None:
                continue

            LOGGER.info("detect room {}".format(room.room_id))

            room.exec(self.character)

            if room.room_id == 8:
                self.dungeon_ctx.clear()

    def frame_handler(self, frame):
        pass


if __name__ == '__main__':
    with open("conf/bwanga.yml", "r") as config_file:
        config = yaml.load(config_file, Loader=yaml.Loader)
    device = ScrcpyDevice(sys.argv[1])
    detector = Detector('weights/dnf.onnx')

    # img = cv2.imread('../../../training_data/20240911/20240911014535.png')
    # res = detector.inference(img, save_img=True)
    # for each in res:
    #     print(each)
    # exit(0)

    ui_ctx = UIElementCtx(device, detector)
    ui_ctx.load(config["ui"])
    evangelist = Evangelist(device, ui_ctx, config["character"]["Evangelist"])
    hell_bringer = HellBringer(device, ui_ctx, config["character"]["HellBringer"])
    c = hell_bringer
    app = BwangaApp(device, detector, c, ui_ctx)
    room.register_room(app, config["scenario"]["dungeon"]["bwanga"], detector)

    app.init()

    # while True:
    #     c.move_toward((1219, 891), (272, 683))
    #     input("next")
    #
    # exit(0)

    # c.move(135, 0.3)
    # c.move(45, 0.3)

    # hell_bringer.move(BattleMetadata.get_angle((2022.5, 744), (624.0, 835)), 0.5)
    # hell_bringer.move(rad=BattleMetadata.get_rad((100, 100), (1000, 1000)), duration=0.5)
    # time.sleep(0.1)
    # hell_bringer.move(rad=BattleMetadata.get_rad((100, 100), (1000, 0)), duration=0.5)
    # time.sleep(0.1)
    # hell_bringer.move(rad=BattleMetadata.get_rad((100, 100), (0, 0)), duration=0.5)
    # time.sleep(0.1)
    # hell_bringer.move(rad=BattleMetadata.get_rad((100, 100), (0, 1000)), duration=0.5)
    # exit(0)

    # c.exec_skill(c.attack, 1)

    app.start()

    # import threading
    # t = threading.Thread(target=app.start)
    # t.start()
    #
    # while True:
    #     frame = app.frame
    #     if frame is None:
    #         continue
    #
    #     result = detector.onnx.inference(frame)
    #     for each in result:
    #         cv2.rectangle(frame, each.left_top, each.right_bottom, (255, 0, 0), lineType=cv2.LINE_AA, thickness=10)
    #     cv2.imshow("frame", frame)
    #
    #     cv2.waitKey(1)

    # while app.frame is None:
    #     time.sleep(1)
    #
    # cv2.imshow("frame", app.frame)
    # cv2.waitKey(0)
