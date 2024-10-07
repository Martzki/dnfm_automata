from common.log import Logger
from dungeon.dungeon import DungeonRoom
from evangelist import init_handlers as evangelist_init_handlers
from hell_bringer import init_handlers as hell_bringer_init_handlers
from noblesse import init_handlers as noblesse_init_handlers
from trickster import init_handlers as trickster_init_handlers
from wrecking_ball import init_handlers as wrecking_ball_init_handlers

LOGGER = Logger(__name__).logger
DUNGEON_NAME = "bwanga"

"""
Bwanga Room
[  11 ][  10 ][  9  ]
[  0  ][  5  ][  4  ][  6  ][  7  ][  8  ]
[  1  ][  2  ][  3  ]
"""


def register_room(app):
    dungeon = app.dungeon
    evangelist_handlers = evangelist_init_handlers(dungeon)
    hell_bringer_handlers = hell_bringer_init_handlers(dungeon)
    trickster_handlers = trickster_init_handlers(dungeon)
    noblesse_handlers = noblesse_init_handlers(dungeon)
    wrecking_ball_handlers = wrecking_ball_init_handlers(dungeon)

    for i in range(len(evangelist_handlers)):
        room = DungeonRoom(DUNGEON_NAME, i)
        room.register_handler(evangelist_handlers[i])
        room.register_handler(hell_bringer_handlers[i])
        room.register_handler(noblesse_handlers[i])
        room.register_handler(trickster_handlers[i])
        room.register_handler(wrecking_ball_handlers[i])
        dungeon.register_room(room)
