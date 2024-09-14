from evangelist import init_handlers as evangelist_init_handlers
from hell_bringer import init_handlers as hell_bringer_init_handlers
from src.common.log import Logger
from src.lib.dungeon.dungeon import DungeonRoom
from src.lib.scenario.scenario import Scenario

LOGGER = Logger(__name__).logger
DUNGEON_NAME = "bwanga"

"""
Bwanga Room
[  11 ][  10 ][  9  ]
[  0  ][  5  ][  4  ][  6  ][  7  ][  8  ]
[  1  ][  2  ][  3  ]
"""


def get_room_name(room_id):
    return DUNGEON_NAME + "_room_{}".format(room_id)


def register_room(app, room_scenario, detector):
    dungeon_ctx = app.dungeon_ctx
    evangelist_handlers = evangelist_init_handlers(detector, app.device.last_frame, dungeon_ctx.detect_room)
    hell_bringer_handlers = hell_bringer_init_handlers(detector, app.device.last_frame, dungeon_ctx.detect_room)

    i = 0
    for room in room_scenario:
        room = DungeonRoom(DUNGEON_NAME + room, i,
                           Scenario(DUNGEON_NAME + room, key_img_list=room_scenario[room]["key_img"]), detector)
        room.register_handler(evangelist_handlers[i])
        room.register_handler(hell_bringer_handlers[i])
        dungeon_ctx.register_room(room)
        i += 1
