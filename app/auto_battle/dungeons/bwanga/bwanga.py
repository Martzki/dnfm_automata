from func_timeout import FunctionTimedOut

from common.log import Logger
from detector.detector import Detector
from device.device import Device
from dungeon.dungeon import Dungeon, DungeonRoom
from app.auto_battle.dungeons.bwanga.handler.champion import init_handlers as champion_init_handlers
from app.auto_battle.dungeons.bwanga.handler.evangelist import init_handlers as evangelist_init_handlers
from app.auto_battle.dungeons.bwanga.handler.hell_bringer import init_handlers as hell_bringer_init_handlers
from app.auto_battle.dungeons.bwanga.handler.noblesse import init_handlers as noblesse_init_handlers
from app.auto_battle.dungeons.bwanga.handler.silent_eye import init_handlers as silent_sys_init_handlers
from app.auto_battle.dungeons.bwanga.handler.trickster import init_handlers as trickster_init_handlers
from app.auto_battle.dungeons.bwanga.handler.wrecking_ball import init_handlers as wrecking_ball_init_handlers
from runtime.ui import ui_elements
from ui.ui import UIElementCtx

LOGGER = Logger(__name__).logger
DUNGEON_NAME = "bwanga"

"""
Bwanga Room
[  11 ][  10 ][  9  ]
[  0  ][  5  ][  4  ][  6  ][  7  ][  8  ]
[  1  ][  2  ][  3  ]
"""


class Bwanga(Dungeon):
    def __init__(self, device: Device, detector: Detector, ui_ctx: UIElementCtx):
        super().__init__(device, detector, ui_ctx)
        self.valid_next_room = {
            -1: [0],
            0: [1, 11],
            1: [0, 2],
            2: [1, 3],
            3: [2, 4],
            4: [3, 5, 6, 9],
            5: [4],
            6: [4, 7],
            7: [6, 8],
            8: [0],
            9: [4, 10],
            10: [9, 11],
            11: [0, 10]
        }

    def goto_dungeon(self):
        LOGGER.info("Start to go to dungeons")
        self.ui_ctx.click_ui_element(ui_elements.Common.Adventure)
        self.ui_ctx.click_ui_element(ui_elements.Common.AdventureReward, delay=1)
        self.ui_ctx.click_ui_element(ui_elements.Common.AdventureRewardAdventureLevel)
        self.ui_ctx.click_ui_element(ui_elements.Common.AdventureRewardMountThunderime)
        self.ui_ctx.click_ui_element(ui_elements.Common.AdventureRewardMoveToArea)
        self.ui_ctx.click_ui_element(ui_elements.Dungeon.DungeonSelectAdventureLevel, timeout=120)
        self.ui_ctx.click_ui_element(ui_elements.Dungeon.DungeonSelectBwanga)
        self.ui_ctx.wait_ui_element(ui_elements.Dungeon.DungeonLabelBwanga, timeout=3)
        self.ui_ctx.click_ui_element(ui_elements.Dungeon.DungeonSelectStartBattle)
        try:
            self.wait_in_dungeon()
        except FunctionTimedOut:
            self.ui_ctx.double_check()
            self.wait_in_dungeon()

        LOGGER.info("Succeed to go to dungeons")

    def register_rooms(self):
        champion_handlers = champion_init_handlers(self)
        evangelist_handlers = evangelist_init_handlers(self)
        hell_bringer_handlers = hell_bringer_init_handlers(self)
        noblesse_handlers = noblesse_init_handlers(self)
        silent_eye_handlers = silent_sys_init_handlers(self)
        trickster_handlers = trickster_init_handlers(self)
        wrecking_ball_handlers = wrecking_ball_init_handlers(self)

        for i in range(len(evangelist_handlers)):
            room = DungeonRoom(DUNGEON_NAME, i, i == 8)
            room.register_handler(champion_handlers[i])
            room.register_handler(evangelist_handlers[i])
            room.register_handler(hell_bringer_handlers[i])
            room.register_handler(noblesse_handlers[i])
            room.register_handler(silent_eye_handlers[i])
            room.register_handler(trickster_handlers[i])
            room.register_handler(wrecking_ball_handlers[i])
            self.register_room(room)
