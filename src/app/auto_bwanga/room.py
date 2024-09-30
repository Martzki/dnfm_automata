from evangelist import init_handlers as evangelist_init_handlers
from hell_bringer import init_handlers as hell_bringer_init_handlers
from src.common.log import Logger
from src.lib.dungeon.dungeon import DungeonRoom
from src.lib.dungeon.map import DungeonMap, DungeonMapRoom
from src.lib.scenario.scenario import Scenario
from trickster import init_handlers as trickster_init_handlers

LOGGER = Logger(__name__).logger
DUNGEON_NAME = "bwanga"

"""
Bwanga Room
[  11 ][  10 ][  9  ]
[  0  ][  5  ][  4  ][  6  ][  7  ][  8  ]
[  1  ][  2  ][  3  ]
"""


def detect_room_id(map: DungeonMap):
    if ((map.center_room.gate_mask == DungeonMapRoom.HasUpGate | DungeonMapRoom.HasDownGate and
            not map.room_matrix[5].is_empty) or
            map.room_mask == 0 or
            map.room_mask == 0x30 or
            (map.center_room.gate_mask == 0 and
             not map.room_matrix[4].is_empty and
             not map.room_matrix[5].is_empty and
             map.room_matrix[0].is_empty and
             map.room_matrix[3].is_empty and
             map.room_matrix[6].is_empty and
             map.up_room.is_empty)):
        return 0
    elif map.up_room.gate_mask == DungeonMapRoom.HasUpGate | DungeonMapRoom.HasDownGate:
        return 1
    elif (map.left_room.gate_mask == DungeonMapRoom.HasUpGate | DungeonMapRoom.HasRightGate or
          map.right_room.gate_mask == DungeonMapRoom.HasLeftGate | DungeonMapRoom.HasUpGate):
        return 2
    elif ((map.left_room.gate_mask == DungeonMapRoom.HasLeftGate | DungeonMapRoom.HasRightGate and
           not map.room_matrix[0].is_empty) or
          map.up_room.gate_mask == DungeonMapRoom.HasLeftGate | DungeonMapRoom.HasRightGate | DungeonMapRoom.UpRoomIndex | DungeonMapRoom.HasDownGate):
        return 3
    elif (map.down_room.gate_mask == DungeonMapRoom.HasLeftGate | DungeonMapRoom.HasUpGate or
          map.up_room.gate_mask == DungeonMapRoom.HasLeftGate | DungeonMapRoom.HasDownGate):
        return 4
    elif map.right_room.gate_mask == DungeonMapRoom.HasRightGate | DungeonMapRoom.HasUpGate | DungeonMapRoom.HasDownGate:
        return 5
    elif map.left_room.gate_mask == DungeonMapRoom.HasLeftGate | DungeonMapRoom.HasRightGate | DungeonMapRoom.HasUpGate | DungeonMapRoom.HasDownGate:
        return 6
    elif (map.room_matrix[0].is_empty and
          map.room_matrix[1].is_empty and
          map.room_matrix[2].is_empty and
          map.room_matrix[6].is_empty and
          map.room_matrix[7].is_empty and
          map.room_matrix[8].is_empty):
        return 7 if not map.room_matrix[5].is_empty else 8
    elif ((map.left_room.gate_mask == DungeonMapRoom.HasLeftGate | DungeonMapRoom.HasRightGate and
           map.room_matrix[0].is_empty) or
          map.down_room.gate_mask == DungeonMapRoom.HasLeftGate | DungeonMapRoom.HasRightGate | DungeonMapRoom.UpRoomIndex | DungeonMapRoom.HasDownGate):
        return 9
    elif (map.right_room.gate_mask == DungeonMapRoom.HasLeftGate | DungeonMapRoom.HasDownGate or
          map.left_room.gate_mask == DungeonMapRoom.HasDownGate | DungeonMapRoom.HasRightGate or
          map.room_mask == 0x1f8):
        return 10
    elif map.down_room.gate_mask == DungeonMapRoom.HasUpGate | DungeonMapRoom.HasDownGate:
        return 11
    else:
        return -1


def get_room_name(room_id):
    return DUNGEON_NAME + "_room_{}".format(room_id)


def register_room(app, room_scenario, detector):
    dungeon_ctx = app.dungeon
    evangelist_handlers = evangelist_init_handlers(detector, app.device.last_frame, dungeon_ctx.detect_room)
    hell_bringer_handlers = hell_bringer_init_handlers(detector, app.device.last_frame, dungeon_ctx.detect_room)
    trickster_handlers = trickster_init_handlers(detector, app.device.last_frame, dungeon_ctx.detect_room)

    i = 0
    for room in room_scenario:
        room = DungeonRoom(DUNGEON_NAME + room, i,
                           Scenario(DUNGEON_NAME + room, key_img_list=room_scenario[room]["key_img"]), detector)
        room.register_handler(evangelist_handlers[i])
        room.register_handler(hell_bringer_handlers[i])
        room.register_handler(trickster_handlers[i])
        dungeon_ctx.register_room(room)
        i += 1
