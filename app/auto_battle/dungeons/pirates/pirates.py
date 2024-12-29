import time

from func_timeout import FunctionTimedOut

from app.auto_battle.dungeons.pirates.handler.desperado import init_handlers as desperado_init_handlers
from app.auto_battle.dungeons.pirates.handler.evangelist import init_handlers as evangelist_init_handlers
from app.auto_battle.dungeons.pirates.handler.grand_master import init_handlers as grand_master_init_handlers
from app.auto_battle.dungeons.pirates.handler.silent_eye import init_handlers as silent_eye_init_handlers
from app.auto_battle.dungeons.pirates.handler.wrecking_ball import init_handlers as wrecking_ball_init_handlers
from common.log import Logger
from detector.detector import Detector
from device.device import Device
from dungeon.dungeon import Dungeon, DungeonRoom
from runtime.ui import ui_elements
from ui.ui import UIElementCtx

LOGGER = Logger(__name__).logger
DUNGEON_NAME = "pirates"

"""
Pirates Room
       [  8  ][  7  ]              [  9  ][  10 ]
[  0  ][  1  ][  2  ][  3  ][  4  ][  5  ][  6  ]
"""


class Pirates(Dungeon):
    def __init__(self, device: Device, detector: Detector, ui_ctx: UIElementCtx):
        super().__init__(DUNGEON_NAME, device, detector, ui_ctx)
        self.valid_next_room = {
            -1: [0],
            0: [1],
            1: [0, 2],
            2: [1, 3, 7],
            3: [2, 4],
            4: [3, 5],
            5: [4, 6, 9],
            6: [5],
            7: [2, 8],
            8: [7],
            9: [5, 10],
            10: [9]
        }

    def goto_dungeon(self):
        LOGGER.info(f"Start to go to {self.name}")
        self.ui_ctx.click_ui_element(ui_elements.Common.Adventure)
        self.ui_ctx.click_ui_element(ui_elements.Common.AdventureReward, delay=1)
        swipe_center = list(self.ui_ctx.wait_ui_element(ui_elements.Common.AdventureRewardAdventureLevel))
        swipe_center[1] += 300
        self.device.swipe(swipe_center, (swipe_center[0], 0))
        time.sleep(5)
        self.ui_ctx.click_ui_element(ui_elements.Common.AdventureRewardOceanicExpress)
        self.ui_ctx.click_ui_element(ui_elements.Common.AdventureRewardMoveToArea)
        self.ui_ctx.click_ui_element(ui_elements.Dungeon.DungeonSelectNormalLevel, timeout=120)
        self.ui_ctx.click_ui_element(ui_elements.Dungeon.DungeonSelectPirates, delay=1)
        self.ui_ctx.click_ui_element(ui_elements.Dungeon.DungeonLabelPirates)
        self.ui_ctx.click_ui_element(ui_elements.Dungeon.DungeonSelectStartBattle)
        try:
            self.wait_in_dungeon()
        except FunctionTimedOut:
            self.ui_ctx.double_check()
            self.wait_in_dungeon()

        LOGGER.info(f"Succeed to go to {self.name}")

    def register_rooms(self):
        handlers = [
            desperado_init_handlers(self),
            evangelist_init_handlers(self),
            grand_master_init_handlers(self),
            silent_eye_init_handlers(self),
            wrecking_ball_init_handlers(self)
        ]

        for i in range(len(handlers[0])):
            room = DungeonRoom(DUNGEON_NAME, i, i == 6)
            for handler in handlers:
                room.register_handler(handler[i])
            self.register_room(room)
