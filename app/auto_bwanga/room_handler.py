from character.character import Character
from common.log import Logger
from common.util import timeout
from dungeon.dungeon import DungeonRoomHandler
from ui.ui import UIElementCtx

LOGGER = Logger(__name__).logger


class BwangaRoom0Handler(DungeonRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 0, character_class, strategy)

    @timeout(30)
    def move_to_next_room(self, character: Character, enter_times: int):
        LOGGER.info(f"Searching next room gate for room {self.room_id}")

        while True:
            retry_times = 0
            last_coordinate = None
            while True:
                meta = self.dungeon.get_battle_metadata()
                if meta.down_gate and meta.down_gate.is_open and meta.character:
                    break

                if self.room_changed():
                    return

                if not meta.character:
                    if self.re_search_dungeon(character):
                        return
                    continue

                if meta.up_gate:
                    dst = (meta.up_gate.right_bottom[0] + 240, meta.up_gate.right_bottom[1] + 474)
                    LOGGER.info(f"move from {meta.character.coordinate()} to anchor {dst}")
                    if character.move_toward(meta.character.coordinate(), dst, self.room_changed):
                        return
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

            LOGGER.info("found gate, move")
            if not character.move_toward(meta.character.coordinate(), meta.down_gate.coordinate(), self.room_changed):
                LOGGER.info("room not changed after moving, retry")
                continue

            LOGGER.info("room changed, return")

            return


class BwangaRoom1Handler(DungeonRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 1, character_class, strategy)

    @timeout(30)
    def move_to_next_room(self, character: Character, enter_times: int):
        LOGGER.info(f"Searching next room gate for room {self.room_id}")

        while True:
            last_coordinate = None
            while True:
                meta = self.dungeon.get_battle_metadata()
                if meta.right_gate and meta.right_gate.is_open and meta.character:
                    break

                if not meta.character:
                    if self.re_search_dungeon(character):
                        return
                    continue

                if self.room_changed():
                    return

                if meta.up_gate:
                    dst = (meta.up_gate.coordinate()[0] + 400, meta.up_gate.coordinate()[1] + 100)
                    LOGGER.info(f"move from {meta.character.coordinate()} to anchor {dst}")
                    if character.move_toward(meta.character.coordinate(), dst, self.room_changed):
                        return
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
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 2, character_class, strategy)

    @timeout(30)
    def move_to_next_room(self, character: Character, enter_times: int):
        LOGGER.info(f"Searching next room gate for room {self.room_id}")

        while True:
            last_coordinate = None
            while True:
                meta = self.dungeon.get_battle_metadata()
                if meta.right_gate and meta.right_gate.is_open and meta.character:
                    break

                if not meta.character:
                    if self.re_search_dungeon(character):
                        return
                    continue

                if self.room_changed():
                    return

                if meta.left_gate:
                    dst = (meta.left_gate.coordinate()[0] + 1500, meta.left_gate.coordinate()[1] - 50)
                    LOGGER.info(f"move from {meta.character.coordinate()} to anchor {dst}")
                    if character.move_toward(meta.character.coordinate(), dst, self.room_changed):
                        return
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
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 3, character_class, strategy)

    @timeout(30)
    def move_to_next_room(self, character: Character, enter_times: int):
        LOGGER.info(f"Searching next room gate for room {self.room_id}")

        while True:
            last_coordinate = None
            while True:
                meta = self.dungeon.get_battle_metadata()
                if meta.up_gate and meta.up_gate.is_open and meta.character:
                    break

                if not meta.character:
                    if self.re_search_dungeon(character):
                        return
                    continue

                if self.room_changed():
                    return

                if meta.left_gate:
                    dst = (meta.left_gate.coordinate()[0] + 700, meta.left_gate.coordinate()[1])
                    LOGGER.info(f"move from {meta.character.coordinate()} to anchor {dst}")
                    if character.move_toward(meta.character.coordinate(), dst, self.room_changed):
                        return
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
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 4, character_class, strategy)

    def pre_handler(self, enter_times, character: Character, **kwargs):
        last_room_id = kwargs.get("last_room_id", -1)
        if last_room_id == 5:
            character.move(340, 1)

    @timeout(30)
    def move_to_next_room(self, character: Character, enter_times: int, room_5_visited: bool):
        LOGGER.info(f"Searching next room gate for room {self.room_id}")

        while True:
            last_coordinate = None
            while True:
                meta = self.dungeon.get_battle_metadata()
                next_gate = meta.right_gate if room_5_visited else meta.left_gate
                if next_gate and next_gate.is_open and meta.character:
                    break

                if not meta.character:
                    if self.re_search_dungeon(character):
                        return
                    continue

                if self.room_changed():
                    return

                if meta.up_gate:
                    if not room_5_visited:
                        dst = (meta.up_gate.left_top[0] - 500, meta.up_gate.right_bottom[1] + 150)
                    else:
                        dst = (meta.up_gate.right_bottom[0] + 100, meta.up_gate.right_bottom[1] + 400)

                    LOGGER.info(f"move from {meta.character.coordinate()} to anchor {dst}")
                    if character.move_toward(meta.character.coordinate(), dst, self.room_changed):
                        return
                    continue

                # Avoid already on gate scenario.
                if not last_coordinate:
                    if not room_5_visited:
                        character.move(315, 0.2)
                    else:
                        character.move(225, 0.2)

                if not last_coordinate or abs(last_coordinate[0] - meta.character.coordinate()[0]) > 10:
                    if not room_5_visited:
                        character.move(180, 0.1)
                    else:
                        character.move(0, 0.1)
                else:
                    if not room_5_visited:
                        character.move(90, 0.1)
                    else:
                        character.move(90, 0.1)

                last_coordinate = meta.character.coordinate()

            LOGGER.info("found gate, move")

            if not room_5_visited:
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
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 5, character_class, strategy)

    @timeout(30)
    def move_to_next_room(self, character: Character, enter_times: int):
        LOGGER.info(f"Searching next room gate for room {self.room_id}")

        while True:
            last_coordinate = None
            while True:
                meta = self.dungeon.get_battle_metadata()
                if meta.right_gate and meta.right_gate.is_open and meta.character:
                    break

                if not meta.character:
                    if self.re_search_dungeon(character):
                        return
                    continue

                if self.room_changed():
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
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 6, character_class, strategy)

    @timeout(30)
    def move_to_next_room(self, character: Character, enter_times: int, room_5_visited: bool):
        LOGGER.info(f"Searching next room gate for room {self.room_id}")

        while True:
            while True:
                meta = self.dungeon.get_battle_metadata()
                next_gate = meta.right_gate if room_5_visited else meta.left_gate
                if next_gate and next_gate.is_open and meta.character:
                    break

                if self.re_search_dungeon(character):
                    return

            LOGGER.info("found gate, move")
            if not character.move_toward(meta.character.coordinate(), next_gate.coordinate(), self.room_changed):
                LOGGER.info("room not changed after moving, retry")
                continue

            LOGGER.info("room changed, return")

            return


class BwangaRoom7Handler(DungeonRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 7, character_class, strategy)

    @timeout(30)
    def move_to_next_room(self, character: Character, enter_times: int):
        LOGGER.info(f"Searching next room gate for room {self.room_id}")

        while True:
            last_coordinate = None
            while True:
                meta = self.dungeon.get_battle_metadata()
                if meta.right_gate and meta.right_gate.is_open and meta.character:
                    break

                if not meta.character:
                    if self.re_search_dungeon(character):
                        return
                    continue

                if self.room_changed():
                    return

                if meta.left_gate:
                    dst = (meta.left_gate.coordinate()[0] + 1500, meta.left_gate.coordinate()[1])
                    LOGGER.info(f"move from {meta.character.coordinate()} to anchor {dst}")
                    if character.move_toward(meta.character.coordinate(), dst, self.room_changed):
                        return
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


class BwangaRoom8Handler(DungeonRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 8, character_class, strategy)

    @timeout(30)
    def post_handler(self, enter_times, character: Character, **kwargs):
        self.dungeon.pick_cards()

        self.dungeon.ui_ctx.wait_ui_element(UIElementCtx.CategoryDungeon, "re_enter_dungeon", timeout=15)

        # Pick up left items.
        while True:
            meta = self.dungeon.get_battle_metadata()

            if not meta.has_item():
                break

            self.pick_items(character, meta, ignore_room_change=True)

        self.dungeon.re_enter()


class BwangaRoom9Handler(DungeonRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 9, character_class, strategy)

    @timeout(30)
    def move_to_next_room(self, character: Character, enter_times: int):
        LOGGER.info(f"Searching next room gate for room {self.room_id}")

        while True:
            last_coordinate = None
            while True:
                meta = self.dungeon.get_battle_metadata()
                if meta.down_gate and meta.down_gate.is_open and meta.character:
                    break

                if not meta.character:
                    if self.re_search_dungeon(character):
                        return
                    continue

                if self.room_changed():
                    return

                if meta.left_gate:
                    dst = (meta.left_gate.coordinate()[0] + 1500, meta.left_gate.coordinate()[1] + 300)
                    LOGGER.info(f"move from {meta.character.coordinate()} to anchor {dst}")
                    if character.move_toward(meta.character.coordinate(), dst, self.room_changed):
                        return
                    continue

                # Avoid already on gate scenario.
                if not last_coordinate:
                    character.move(90, 0.2)

                if not last_coordinate or abs(last_coordinate[0] - meta.character.coordinate()[0]) > 10:
                    character.move(0, 0.1)
                else:
                    character.move(270, 0.1)

                last_coordinate = meta.character.coordinate()

            LOGGER.info("found gate, move")
            if not character.move_toward(meta.character.coordinate(), meta.down_gate.coordinate(), self.room_changed):
                LOGGER.info("room not changed after moving, retry")
                continue

            LOGGER.info("room changed, return")

            return


class BwangaRoom10Handler(DungeonRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 10, character_class, strategy)

    @timeout(30)
    def move_to_next_room(self, character: Character, enter_times: int):
        LOGGER.info(f"Searching next room gate for room {self.room_id}")

        while True:
            last_coordinate = None
            while True:
                meta = self.dungeon.get_battle_metadata()
                if meta.right_gate and meta.right_gate.is_open and meta.character:
                    break

                if not meta.character:
                    if self.re_search_dungeon(character):
                        return
                    continue

                if self.room_changed():
                    return

                if meta.left_gate:
                    dst = (meta.left_gate.coordinate()[0] + 1500, meta.left_gate.coordinate()[1])
                    LOGGER.info(f"move from {meta.character.coordinate()} to anchor {dst}")
                    if character.move_toward(meta.character.coordinate(), dst, self.room_changed):
                        return
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


class BwangaRoom11Handler(DungeonRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 11, character_class, strategy)

    @timeout(30)
    def move_to_next_room(self, character: Character, enter_times: int):
        LOGGER.info(f"Searching next room gate for room {self.room_id}")

        while True:
            last_coordinate = None
            while True:
                meta = self.dungeon.get_battle_metadata()
                if meta.right_gate and meta.right_gate.is_open and meta.character:
                    break

                if not meta.character:
                    if self.re_search_dungeon(character):
                        return
                    continue

                if self.room_changed():
                    return

                if meta.down_gate:
                    dst = (meta.down_gate.coordinate()[0], 0)
                    LOGGER.info(f"move from {meta.character.coordinate()} to anchor {dst}")
                    if character.move_toward(meta.character.coordinate(), dst, self.room_changed):
                        return
                    character.move(0, 0.5)
                    continue

                # Avoid already on gate scenario.
                if not last_coordinate:
                    character.move(225, 0.2)

                if not last_coordinate or abs(last_coordinate[0] - meta.character.coordinate()[0]) > 10:
                    character.move(0, 0.1)
                else:
                    character.move(90, 0.1)

                last_coordinate = meta.character.coordinate()

            LOGGER.info("found gate, move")
            if not character.move_toward(meta.character.coordinate(), meta.right_gate.coordinate(), self.room_changed):
                LOGGER.info("room not changed after moving, retry")
                continue

            LOGGER.info("room changed, return")

            return
