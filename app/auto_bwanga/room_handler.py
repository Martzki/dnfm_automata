from func_timeout import func_set_timeout, FunctionTimedOut

from character.character import Character
from common.log import Logger
from common.util import timeout_handler
from dungeon.battle import Gate
from dungeon.dungeon import DungeonRoomHandler, DungeonFinished
from ui.ui import UIElementCtx

LOGGER = Logger(__name__).logger


class BwangaRoom0Handler(DungeonRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 0, character_class, strategy)

    @func_set_timeout(30)
    def move_to_next_room(self, character: Character):
        super().move_to_next_room(character, Gate.DirectionDown, Gate.DirectionUp, anchor_vector=(240, 470))


class BwangaRoom1Handler(DungeonRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 1, character_class, strategy)

    @func_set_timeout(30)
    def move_to_next_room(self, character: Character):
        super().move_to_next_room(character, Gate.DirectionRight, Gate.DirectionUp, anchor_vector=(400, 100))


class BwangaRoom2Handler(DungeonRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 2, character_class, strategy)

    @func_set_timeout(30)
    def move_to_next_room(self, character: Character):
        super().move_to_next_room(character, Gate.DirectionRight, Gate.DirectionLeft, anchor_vector=(1500, -50))


class BwangaRoom3Handler(DungeonRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 3, character_class, strategy)

    @func_set_timeout(30)
    def move_to_next_room(self, character: Character):
        super().move_to_next_room(character, Gate.DirectionUp, Gate.DirectionLeft, anchor_vector=(700, 0))


class BwangaRoom4Handler(DungeonRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 4, character_class, strategy)

    def pre_handler(self, enter_times, character: Character, **kwargs):
        last_room_id = kwargs.get("last_room_id", -1)
        if last_room_id == 5:
            character.move(340, 0.8)

    @func_set_timeout(30)
    def move_to_next_room(self, character: Character, room_5_visited: bool):
        if not room_5_visited:
            super().move_to_next_room(character, Gate.DirectionLeft, Gate.DirectionUp, anchor_vector=(-500, 150))
        else:
            super().move_to_next_room(character, Gate.DirectionRight, Gate.DirectionUp, anchor_vector=(100, 400))


class BwangaRoom5Handler(DungeonRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 5, character_class, strategy)

    def pre_handler(self, enter_times, character: Character, **kwargs):
        if enter_times > 1:
            return

        character.move(225, 0.8)
        try:
            self.re_pick_items(character)
        except FunctionTimedOut:
            pass

    @func_set_timeout(30)
    def move_to_next_room(self, character: Character):
        super().move_to_next_room(character, Gate.DirectionRight)


class BwangaRoom6Handler(DungeonRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 6, character_class, strategy)

    @func_set_timeout(30)
    def move_to_next_room(self, character: Character, room_5_visited: bool):
        if not room_5_visited:
            super().move_to_next_room(character, Gate.DirectionLeft, Gate.DirectionRight, anchor_vector=(-200, 0))
        else:
            super().move_to_next_room(character, Gate.DirectionRight, Gate.DirectionLeft, anchor_vector=(200, 0))


class BwangaRoom7Handler(DungeonRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 7, character_class, strategy)

    @func_set_timeout(30)
    def move_to_next_room(self, character: Character, room_5_visited: bool):
        if not room_5_visited:
            super().move_to_next_room(character, Gate.DirectionLeft, Gate.DirectionRight, anchor_vector=(-1200, 0))
        else:
            super().move_to_next_room(character, Gate.DirectionRight, Gate.DirectionLeft, anchor_vector=(1200, 0))


class BwangaRoom8Handler(DungeonRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 8, character_class, strategy)

    def post_handler(self, enter_times, character: Character, **kwargs):
        self.dungeon.pick_cards()

        self.dungeon.ui_ctx.wait_ui_element(UIElementCtx.CategoryDungeon, "re_enter_dungeon", timeout=15)

        try:
            self.re_pick_items(character)
        except FunctionTimedOut as e:
            timeout_handler(e, LOGGER.warning, self.dungeon.device.last_frame)

        fatigue_points = self.dungeon.get_fatigue_points()
        LOGGER.info(f"Current fatigue_points: {fatigue_points}")

        if fatigue_points != 0:
            self.dungeon.re_enter()
        else:
            self.dungeon.ui_ctx.click_ui_element(UIElementCtx.CategoryDungeon, "exit_dungeon",
                                                 timeout=5, delay=10)
            raise DungeonFinished()


class BwangaRoom9Handler(DungeonRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 9, character_class, strategy)

    @func_set_timeout(30)
    def move_to_next_room(self, character: Character):
        super().move_to_next_room(character, Gate.DirectionDown, Gate.DirectionLeft, anchor_vector=(1500, 300))


class BwangaRoom10Handler(DungeonRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 10, character_class, strategy)

    @func_set_timeout(30)
    def move_to_next_room(self, character: Character):
        super().move_to_next_room(character, Gate.DirectionRight, Gate.DirectionLeft, anchor_vector=(1500, 0))


class BwangaRoom11Handler(DungeonRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 11, character_class, strategy)

    @func_set_timeout(30)
    def move_to_next_room(self, character: Character):
        super().move_to_next_room(character, Gate.DirectionRight, Gate.DirectionDown, anchor_vector=(200, -700))
