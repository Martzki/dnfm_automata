import time

import cv2

from src.common.log import Logger
from src.common.util import get_capture_file
from src.lib.character.character import Character
from src.lib.dungeon.battle import BattleMetadata
from src.lib.dungeon.dungeon import DungeonRoomHandler

LOGGER = Logger(__name__).logger


class BwangaRoom0Handler(DungeonRoomHandler):
    def __init__(self, character_class, detector, last_frame, detect_room, strategy):
        super().__init__(0, character_class, detector, last_frame, detect_room, strategy)

    def move_to_next_room(self, character: Character, enter_times: int):
        LOGGER.info(f"Searching next room gate for room {self.room_id}")

        while True:
            retry_times = 0
            start = time.time()
            last_coordinate = None
            while True:
                # if time.time() - start > 5:
                #     LOGGER.warning("Searching gate timeout")
                #     return

                frame = self.last_frame()
                meta = BattleMetadata(frame, self.detector)
                if meta.down_gate and meta.down_gate.is_open and meta.character:
                    break

                if self.room_changed(frame):
                    return

                if not meta.character:
                    cv2.imwrite(get_capture_file("character_not_found"), frame)
                    self.refind_character(character)
                    continue

                if meta.up_gate:
                    # input("move to anchor: ")
                    dst = (meta.up_gate.right_bottom[0] + 240, meta.up_gate.right_bottom[1] + 474)
                    LOGGER.info(f"move from {meta.character.coordinate()} to anchor {dst}")
                    # cv2.imwrite(get_capture_file("room_0_before_move_to_anchor"), frame)
                    character.move_toward(meta.character.coordinate(), dst)
                    # cv2.imwrite(get_capture_file("room_0_anchor"), frame)
                    continue

                retry_times += 1
                if retry_times < 5:
                    continue

                # Avoid already on gate scenario.
                if not last_coordinate:
                    character.move(135, 0.2)

                if not last_coordinate or abs(last_coordinate[0] - meta.character.coordinate()[0]) > 10:
                    character.move(0, 0.2)
                else:
                    character.move(270, 0.2)

                last_coordinate = meta.character.coordinate()

                retry_times = 0
                cv2.imwrite(get_capture_file("open_down_gate_not_found"), frame)

            LOGGER.info("found gate, move")
            if not character.move_toward(meta.character.coordinate(), meta.down_gate.coordinate(), self.room_changed):
                LOGGER.info("room not changed after moving, retry")
                continue

            LOGGER.info("room changed, return")

            return


class BwangaRoom1Handler(DungeonRoomHandler):
    def __init__(self, character_class, detector, last_frame, detect_room, strategy):
        super().__init__(1, character_class, detector, last_frame, detect_room, strategy)

    def move_to_next_room(self, character: Character, enter_times: int):
        LOGGER.info(f"Searching next room gate for room {self.room_id}")

        while True:
            start = time.time()
            last_coordinate = None
            while True:
                # if time.time() - start > 5:
                #     LOGGER.warning("Searching gate timeout")
                #     return

                frame = self.last_frame()
                meta = BattleMetadata(frame, self.detector)
                if meta.right_gate and meta.right_gate.is_open and meta.character:
                    break

                if not meta.character:
                    cv2.imwrite(get_capture_file(), frame)
                    self.refind_character(character)
                    continue

                if self.room_changed(frame):
                    return

                if meta.up_gate:
                    dst = (meta.up_gate.coordinate()[0] + 400, meta.up_gate.coordinate()[1] + 100)
                    LOGGER.info(f"move from {meta.character.coordinate()} to anchor {dst}")
                    character.move_toward(meta.character.coordinate(), dst)
                    continue

                # Avoid already on gate scenario.
                if not last_coordinate:
                    character.move(135, 0.2)

                if not last_coordinate or abs(last_coordinate[1] - meta.character.coordinate()[1]) > 10:
                    character.move(270, 0.1)
                else:
                    character.move(0, 0.1)

                last_coordinate = meta.character.coordinate()

            LOGGER.info("found gate, move")
            if not character.move_toward(meta.character.coordinate(), meta.right_gate.coordinate(), self.room_changed):
                LOGGER.info("room not changed after moving, retry")
                continue

            LOGGER.info("room changed, return")

            return


class BwangaRoom2Handler(DungeonRoomHandler):
    def __init__(self, character_class, detector, last_frame, detect_room, strategy):
        super().__init__(2, character_class, detector, last_frame, detect_room, strategy)

    def move_to_next_room(self, character: Character, enter_times: int):
        LOGGER.info(f"Searching next room gate for room {self.room_id}")

        while True:
            start = time.time()
            last_coordinate = None
            while True:
                # if time.time() - start > 5:
                #     LOGGER.warning("Searching gate timeout")
                #     return

                frame = self.last_frame()
                meta = BattleMetadata(frame, self.detector)
                if meta.right_gate and meta.right_gate.is_open and meta.character:
                    break

                if not meta.character:
                    cv2.imwrite(get_capture_file(), frame)
                    self.refind_character(character)
                    continue

                if self.room_changed(frame):
                    return

                if meta.left_gate:
                    dst = (meta.left_gate.coordinate()[0] + 1500, meta.left_gate.coordinate()[1] - 50)
                    LOGGER.info(f"move from {meta.character.coordinate()} to anchor {dst}")
                    character.move_toward(meta.character.coordinate(), dst)
                    continue

                # Avoid already on gate scenario.
                if not last_coordinate:
                    character.move(225, 0.2)

                if not last_coordinate or abs(last_coordinate[1] - meta.character.coordinate()[1]) > 10:
                    character.move(90, 0.1)
                else:
                    character.move(0, 0.1)

                last_coordinate = meta.character.coordinate()

            LOGGER.info("found gate, move")
            if not character.move_toward(meta.character.coordinate(), meta.right_gate.coordinate(), self.room_changed):
                LOGGER.info("room not changed after moving, retry")
                continue

            LOGGER.info("room changed, return")

            return


class BwangaRoom3Handler(DungeonRoomHandler):
    def __init__(self, character_class, detector, last_frame, detect_room, strategy):
        super().__init__(3, character_class, detector, last_frame, detect_room, strategy)

    def move_to_next_room(self, character: Character, enter_times: int):
        LOGGER.info(f"Searching next room gate for room {self.room_id}")

        while True:
            start = time.time()
            last_coordinate = None
            while True:
                # if time.time() - start > 5:
                #     LOGGER.warning("Searching gate timeout")
                #     return

                frame = self.last_frame()
                meta = BattleMetadata(frame, self.detector)
                if meta.up_gate and meta.up_gate.is_open and meta.character:
                    break

                if not meta.character:
                    cv2.imwrite(get_capture_file(), frame)
                    self.refind_character(character)
                    continue

                if self.room_changed(frame):
                    return

                if meta.left_gate:
                    dst = (meta.left_gate.coordinate()[0] + 400, meta.left_gate.coordinate()[1])
                    LOGGER.info(f"move from {meta.character.coordinate()} to anchor {dst}")
                    character.move_toward(meta.character.coordinate(), dst)
                    continue

                # Avoid already on gate scenario.
                if not last_coordinate:
                    character.move(225, 0.2)

                if not last_coordinate or abs(last_coordinate[1] - meta.character.coordinate()[1]) > 10:
                    character.move(90, 0.1)
                else:
                    character.move(0, 0.1)

                last_coordinate = meta.character.coordinate()

            LOGGER.info("found gate, move")
            if not character.move_toward(meta.character.coordinate(), meta.up_gate.coordinate(), self.room_changed):
                LOGGER.info("room not changed after moving, retry")
                continue

            LOGGER.info("room changed, return")

            return


class BwangaRoom4Handler(DungeonRoomHandler):
    def __init__(self, character_class, detector, last_frame, detect_room, strategy):
        super().__init__(4, character_class, detector, last_frame, detect_room, strategy)

    def move_to_next_room(self, character: Character, enter_times: int):
        LOGGER.info(f"Searching next room gate for room {self.room_id}")

        while True:
            start = time.time()
            last_coordinate = None
            while True:
                # if time.time() - start > 5:
                #     LOGGER.warning("Searching gate timeout")
                #     return

                frame = self.last_frame()
                meta = BattleMetadata(frame, self.detector)
                next_gate = meta.left_gate if enter_times == 1 else meta.right_gate
                if next_gate and next_gate.is_open and meta.character:
                    break

                if not meta.character:
                    cv2.imwrite(get_capture_file(), frame)
                    self.refind_character(character)
                    continue

                if self.room_changed(frame):
                    return

                if meta.up_gate:
                    if enter_times == 1:
                        dst = (meta.up_gate.left_top[0] - 332, meta.up_gate.right_bottom[1] + 100)
                    else:
                        dst = (meta.up_gate.right_bottom[0] + 100, meta.up_gate.right_bottom[1] + 150)

                    LOGGER.info(f"move from {meta.character.coordinate()} to anchor {dst}")
                    # cv2.imwrite(get_capture_file("room_4_before_move_to_anchor"), frame)
                    character.move_toward(meta.character.coordinate(), dst)
                    # cv2.imwrite(get_capture_file("room_4_anchor"), frame)
                    continue

                # Avoid already on gate scenario.
                if not last_coordinate:
                    if enter_times == 1:
                        character.move(315, 0.2)
                    elif enter_times == 2:
                        character.move(225, 0.2)

                if not last_coordinate or abs(last_coordinate[0] - meta.character.coordinate()[0]) > 10:
                    if enter_times == 1:
                        character.move(180, 0.1)
                    elif enter_times == 2:
                        character.move(0, 0.1)
                else:
                    if enter_times == 1:
                        character.move(90, 0.1)
                    elif enter_times == 2:
                        character.move(90, 0.1)

                last_coordinate = meta.character.coordinate()

            LOGGER.info("found gate, move")

            # room_changed = False
            if enter_times == 1:
                room_changed = character.move_toward(meta.character.coordinate(), meta.left_gate.coordinate(),
                                                     self.room_changed)
            else:
                room_changed = character.move_toward(meta.character.coordinate(), meta.right_gate.coordinate(),
                                                     self.room_changed)

            if not room_changed:
                LOGGER.info("room not changed after moving, retry")
                continue

            LOGGER.info("room changed, return")

            return


class BwangaRoom5Handler(DungeonRoomHandler):
    def __init__(self, character_class, detector, last_frame, detect_room, strategy):
        super().__init__(5, character_class, detector, last_frame, detect_room, strategy)

    def move_to_next_room(self, character: Character, enter_times: int):
        LOGGER.info(f"Searching next room gate for room {self.room_id}")

        while True:
            start = time.time()
            last_coordinate = None
            while True:
                # if time.time() - start > 5:
                #     LOGGER.warning("Searching gate timeout")
                #     return

                frame = self.last_frame()
                meta = BattleMetadata(frame, self.detector)
                if meta.right_gate and meta.right_gate.is_open and meta.character:
                    break

                if not meta.character:
                    cv2.imwrite(get_capture_file(), frame)
                    self.refind_character(character)
                    continue

                if self.room_changed(frame):
                    return

                # Avoid already on gate scenario.
                if not last_coordinate:
                    character.move(180, 0.2)

                if not last_coordinate or abs(last_coordinate[1] - meta.character.coordinate()[1]) > 10:
                    character.move(90, 0.3)
                else:
                    character.move(0, 0.3)

                last_coordinate = meta.character.coordinate()

            LOGGER.info("found gate, move")
            if not character.move_toward(meta.character.coordinate(), meta.right_gate.coordinate(), self.room_changed):
                LOGGER.info("room not changed after moving, retry")
                continue

            LOGGER.info("room changed, return")

            return


class BwangaRoom6Handler(DungeonRoomHandler):
    def __init__(self, character_class, detector, last_frame, detect_room, strategy):
        super().__init__(6, character_class, detector, last_frame, detect_room, strategy)

    def move_to_next_room(self, character: Character, enter_times: int):
        LOGGER.info(f"Searching next room gate for room {self.room_id}")

        while True:
            start = time.time()
            last_coordinate = None
            while True:
                # if time.time() - start > 5:
                #     LOGGER.warning("Searching gate timeout")
                #     return

                frame = self.last_frame()
                meta = BattleMetadata(frame, self.detector)
                if meta.right_gate and meta.right_gate.is_open and meta.character:
                    break

                if not meta.character:
                    cv2.imwrite(get_capture_file(), frame)
                    self.refind_character(character)
                    continue

                if self.room_changed(frame):
                    return

                # Avoid already on gate scenario.
                if not last_coordinate:
                    character.move(180, 0.2)

                if not last_coordinate or abs(last_coordinate[1] - meta.character.coordinate()[1]) > 10:
                    character.move(90, 0.1)
                else:
                    character.move(0, 0.1)

                last_coordinate = meta.character.coordinate()

            LOGGER.info("found gate, move")
            if not character.move_toward(meta.character.coordinate(), meta.right_gate.coordinate(), self.room_changed):
                LOGGER.info("room not changed after moving, retry")
                continue

            LOGGER.info("room changed, return")

            return


class BwangaRoom7Handler(DungeonRoomHandler):
    def __init__(self, character_class, detector, last_frame, detect_room, strategy):
        super().__init__(7, character_class, detector, last_frame, detect_room, strategy)

    def move_to_next_room(self, character: Character, enter_times: int):
        LOGGER.info(f"Searching next room gate for room {self.room_id}")

        while True:
            start = time.time()
            last_coordinate = None
            while True:
                # if time.time() - start > 5:
                #     LOGGER.warning("Searching gate timeout")
                #     return

                frame = self.last_frame()
                meta = BattleMetadata(frame, self.detector)
                if meta.right_gate and meta.right_gate.is_open and meta.character:
                    break

                if not meta.character:
                    cv2.imwrite(get_capture_file(), frame)
                    self.refind_character(character)
                    continue

                if self.room_changed(frame):
                    return

                if meta.left_gate:
                    dst = (meta.left_gate.coordinate()[0] + 1500, meta.left_gate.coordinate()[1])
                    LOGGER.info(f"move from {meta.character.coordinate()} to anchor {dst}")
                    character.move_toward(meta.character.coordinate(), dst)
                    continue

                # Avoid already on gate scenario.
                if not last_coordinate:
                    character.move(225, 0.2)

                if not last_coordinate or abs(last_coordinate[1] - meta.character.coordinate()[1]) > 10:
                    character.move(90, 0.1)
                else:
                    character.move(0, 0.1)

                last_coordinate = meta.character.coordinate()

            LOGGER.info("found gate, move")
            if not character.move_toward(meta.character.coordinate(), meta.right_gate.coordinate(), self.room_changed):
                LOGGER.info("room not changed after moving, retry")
                continue

            LOGGER.info("room changed, return")

            return
