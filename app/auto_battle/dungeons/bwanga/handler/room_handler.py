from func_timeout import func_set_timeout, FunctionTimedOut

from character.character import Character
from common.log import Logger
from common.util import timeout_handler
from dungeon.battle import Gate
from dungeon.dungeon import DungeonRoomHandler, DungeonFinished
from runtime.ui import ui_elements

LOGGER = Logger(__name__).logger


class BwangaRoom0Handler(DungeonRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 0, character_class, strategy)

    @func_set_timeout(30)
    def move_to_next_room(self, character: Character):
        super().move_to_next_room(character, Gate.DirectionDown, Gate.DirectionUp, anchor_vector=(240, 470))

    def post_handler(self, enter_times, character: Character, **kwargs):
        fatigue_points = self.dungeon.get_fatigue_points()
        if fatigue_points <= 0 or fatigue_points > character.reserve_fatigue_points:
            self.move_to_next_room(character)
            return

        LOGGER.info(
            f"Current fatigue points: {fatigue_points} is not greater than "
            f"{character.reserve_fatigue_points}, back to town"
        )

        self.dungeon.back_to_town()


class BwangaRoom1Handler(DungeonRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 1, character_class, strategy)

    @func_set_timeout(30)
    def move_to_next_room(self, character: Character):
        super().move_to_next_room(character, Gate.DirectionRight, Gate.DirectionUp, anchor_vector=(400, 100))

    def post_handler(self, enter_times, character: Character, **kwargs):
        fatigue_points = self.dungeon.get_fatigue_points()
        if 0 < fatigue_points <= character.reserve_fatigue_points:
            LOGGER.info(
                f"Current fatigue points: {fatigue_points} is not greater than "
                f"{character.reserve_fatigue_points}, back to town"
            )

            self.dungeon.back_to_town()
        elif fatigue_points == 1:
            self.dungeon.re_enter()
        else:
            self.move_to_next_room(character)


class BwangaRoom2Handler(DungeonRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 2, character_class, strategy)

    @func_set_timeout(30)
    def move_to_next_room(self, character: Character, direction):
        if direction == Gate.DirectionRight:
            super().move_to_next_room(character, Gate.DirectionRight, Gate.DirectionLeft, anchor_vector=(1500, -50))
        else:
            super().move_to_next_room(character, Gate.DirectionLeft, Gate.DirectionRight, anchor_vector=(-1200, 100))

    def post_handler(self, enter_times, character: Character, **kwargs):
        fatigue_points = self.dungeon.get_fatigue_points()
        visited_room_list = kwargs.get('visited_room_list', [])
        if 0 < fatigue_points <= character.reserve_fatigue_points:
            LOGGER.info(
                f"Current fatigue points: {fatigue_points} is not greater than "
                f"{character.reserve_fatigue_points}, back to town"
            )

            self.dungeon.back_to_town()
        elif fatigue_points == 1:
            self.dungeon.re_enter()
        elif fatigue_points == 0 and 1 not in visited_room_list:
            self.move_to_next_room(character, Gate.DirectionLeft)
        else:
            self.move_to_next_room(character, Gate.DirectionRight)


class BwangaRoom3Handler(DungeonRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 3, character_class, strategy)

    @func_set_timeout(30)
    def move_to_next_room(self, character: Character, direction):
        if direction == Gate.DirectionUp:
            super().move_to_next_room(character, Gate.DirectionUp, Gate.DirectionLeft, anchor_vector=(700, 0))
        else:
            super().move_to_next_room(character, Gate.DirectionLeft, Gate.DirectionUp, anchor_vector=(-500, 0))

    def post_handler(self, enter_times, character: Character, **kwargs):
        fatigue_points = self.dungeon.get_fatigue_points()
        visited_room_list = kwargs.get('visited_room_list', [])
        if 0 < fatigue_points <= character.reserve_fatigue_points:
            LOGGER.info(
                f"Current fatigue points: {fatigue_points} is not greater than "
                f"{character.reserve_fatigue_points}, back to town"
            )

            self.dungeon.back_to_town()
        elif fatigue_points == 1:
            self.dungeon.re_enter()
        elif fatigue_points == 0 and 2 not in visited_room_list:
            self.move_to_next_room(character, Gate.DirectionLeft)
        else:
            self.move_to_next_room(character, Gate.DirectionUp)


class BwangaRoom4Handler(DungeonRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 4, character_class, strategy)

    def pre_handler(self, enter_times, character: Character, **kwargs):
        visited_room_list = kwargs.get('visited_room_list', [])
        if len(visited_room_list) > 0 and visited_room_list[-1] == 5:
            character.move(340, 0.8)

    @func_set_timeout(30)
    def move_to_next_room(self, character: Character, direction):
        if direction == Gate.DirectionLeft:
            super().move_to_next_room(character, Gate.DirectionLeft, Gate.DirectionUp, anchor_vector=(-500, 150))
        elif direction == Gate.DirectionRight:
            super().move_to_next_room(character, Gate.DirectionRight, Gate.DirectionUp, anchor_vector=(400, 150))
        elif direction == Gate.DirectionUp:
            super().move_to_next_room(character, Gate.DirectionUp, Gate.DirectionLeft, anchor_vector=(500, 0))
        else:
            super().move_to_next_room(character, Gate.DirectionDown, Gate.DirectionLeft, anchor_vector=(500, 00))

    def post_handler(self, enter_times, character: Character, **kwargs):
        fatigue_points = self.dungeon.get_fatigue_points()
        visited_room_list = kwargs.get('visited_room_list', [])
        if 0 < fatigue_points <= character.reserve_fatigue_points:
            LOGGER.info(
                f"Current fatigue points: {fatigue_points} is not greater than "
                f"{character.reserve_fatigue_points}, back to town"
            )

            self.dungeon.back_to_town()
        elif fatigue_points == 1:
            self.dungeon.re_enter()
        elif 5 not in visited_room_list:
            self.move_to_next_room(character, Gate.DirectionLeft)
        elif fatigue_points == 0 or (fatigue_points == 5 and character.reserve_fatigue_points == 0):
            if 3 not in visited_room_list:
                self.move_to_next_room(character, Gate.DirectionDown)
            elif 9 not in visited_room_list:
                self.move_to_next_room(character, Gate.DirectionUp)
            else:
                self.move_to_next_room(character, Gate.DirectionRight)
        else:
            self.move_to_next_room(character, Gate.DirectionRight)


class BwangaRoom5Handler(DungeonRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 5, character_class, strategy)

    def pre_handler(self, enter_times, character: Character, **kwargs):
        if enter_times > 1:
            return

        character.move(225, 0.6)
        try:
            self.re_pick_items(character)
        except FunctionTimedOut:
            pass

    @func_set_timeout(30)
    def move_to_next_room(self, character: Character):
        super().move_to_next_room(character, Gate.DirectionRight)

    def post_handler(self, enter_times, character: Character, **kwargs):
        fatigue_points = self.dungeon.get_fatigue_points()
        if 0 < fatigue_points <= character.reserve_fatigue_points:
            LOGGER.info(
                f"Current fatigue points: {fatigue_points} is not greater than "
                f"{character.reserve_fatigue_points}, back to town"
            )

            self.dungeon.back_to_town()
        elif fatigue_points == 1:
            self.dungeon.re_enter()
        else:
            self.move_to_next_room(character)


class BwangaRoom6Handler(DungeonRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 6, character_class, strategy)

    @func_set_timeout(30)
    def move_to_next_room(self, character: Character, direction):
        if direction == Gate.DirectionRight:
            super().move_to_next_room(character, Gate.DirectionRight, Gate.DirectionLeft, anchor_vector=(200, 0))
        else:
            super().move_to_next_room(character, Gate.DirectionLeft, Gate.DirectionRight, anchor_vector=(-200, 0))

    def post_handler(self, enter_times, character: Character, **kwargs):
        fatigue_points = self.dungeon.get_fatigue_points()
        visited_room_list = kwargs.get('visited_room_list', [])
        if 0 < fatigue_points <= character.reserve_fatigue_points:
            LOGGER.info(
                f"Current fatigue points: {fatigue_points} is not greater than "
                f"{character.reserve_fatigue_points}, back to town"
            )

            self.dungeon.back_to_town()
        elif fatigue_points == 1:
            self.dungeon.re_enter()
        elif 5 not in visited_room_list:
            self.move_to_next_room(character, Gate.DirectionLeft)
        else:
            self.move_to_next_room(character, Gate.DirectionRight)


class BwangaRoom7Handler(DungeonRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 7, character_class, strategy)

    @func_set_timeout(30)
    def move_to_next_room(self, character: Character, direction):
        if direction == Gate.DirectionRight:
            super().move_to_next_room(character, Gate.DirectionRight, Gate.DirectionLeft, anchor_vector=(1200, 0))
        else:
            super().move_to_next_room(character, Gate.DirectionLeft, Gate.DirectionRight, anchor_vector=(-1200, 0))

    def pre_handler(self, enter_times, character: Character, **kwargs):
        if self.room_id in kwargs.get('visited_room_list', []):
            character.move(0, 1)

    def post_handler(self, enter_times, character: Character, **kwargs):
        fatigue_points = self.dungeon.get_fatigue_points()
        visited_room_list = kwargs.get('visited_room_list', [])
        if 0 < fatigue_points <= character.reserve_fatigue_points:
            LOGGER.info(
                f"Current fatigue points: {fatigue_points} is not greater than "
                f"{character.reserve_fatigue_points}, back to town"
            )

            self.dungeon.back_to_town()
        elif fatigue_points == 1:
            self.dungeon.re_enter()
        elif 5 not in visited_room_list:
            self.move_to_next_room(character, Gate.DirectionLeft)
        else:
            self.move_to_next_room(character, Gate.DirectionRight)


class BwangaRoom8Handler(DungeonRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 8, character_class, strategy)

    def post_handler(self, enter_times, character: Character, **kwargs):
        self.dungeon.pick_cards()

        self.dungeon.ui_ctx.wait_ui_element(ui_elements.Dungeon.ContinueBattle, timeout=15)

        try:
            self.re_pick_items(character)
        except FunctionTimedOut as e:
            timeout_handler(e, LOGGER.warning, self.dungeon.device.last_frame)

        fatigue_points = self.dungeon.get_fatigue_points()
        LOGGER.info(f"Current fatigue_points: {fatigue_points}")

        if fatigue_points > character.reserve_fatigue_points or fatigue_points < 0:
            if kwargs.get('repair_equipments', False):
                self.dungeon.repair_equipments(in_dungeon=True)
                self.dungeon.return_to_dungeon_scenario()
            self.dungeon.continue_battle()
        else:
            self.dungeon.ui_ctx.click_ui_element(ui_elements.Dungeon.ExitDungeon,
                                                 timeout=5, delay=10)
            raise DungeonFinished()


class BwangaRoom9Handler(DungeonRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 9, character_class, strategy)

    @func_set_timeout(30)
    def move_to_next_room(self, character: Character, direction):
        if direction == Gate.DirectionDown:
            super().move_to_next_room(character, Gate.DirectionDown, Gate.DirectionLeft, anchor_vector=(1500, 300))
        else:
            super().move_to_next_room(character, Gate.DirectionLeft, Gate.DirectionDown, anchor_vector=(-1000, -500))

    def pre_handler(self, enter_times, character: Character, **kwargs):
        visited_room_list = kwargs.get('visited_room_list', [])
        if len(visited_room_list) < 1:
            return

        last_room = visited_room_list[-1]
        if last_room == 4:
            character.move(90, 0.5)
        elif last_room == 10 and self.room_id in visited_room_list:
            character.move(340, 1)

    def post_handler(self, enter_times, character: Character, **kwargs):
        fatigue_points = self.dungeon.get_fatigue_points()
        visited_room_list = kwargs.get('visited_room_list', [])
        if 0 < fatigue_points <= character.reserve_fatigue_points:
            LOGGER.info(
                f"Current fatigue points: {fatigue_points} is not greater than "
                f"{character.reserve_fatigue_points}, back to town"
            )

            self.dungeon.back_to_town()
        elif fatigue_points == 1:
            self.dungeon.re_enter()
        elif fatigue_points == 0 and 10 not in visited_room_list:
            self.move_to_next_room(character, Gate.DirectionLeft)
        else:
            self.move_to_next_room(character, Gate.DirectionDown)


class BwangaRoom10Handler(DungeonRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 10, character_class, strategy)

    @func_set_timeout(30)
    def move_to_next_room(self, character: Character, direction):
        if direction == Gate.DirectionRight:
            super().move_to_next_room(character, Gate.DirectionRight, Gate.DirectionLeft, anchor_vector=(1500, 0))
        else:
            super().move_to_next_room(character, Gate.DirectionLeft, Gate.DirectionRight, anchor_vector=(-1500, 0))

    def pre_handler(self, enter_times, character: Character, **kwargs):
        visited_room_list = kwargs.get('visited_room_list', [])
        if len(visited_room_list) < 1 or self.room_id not in visited_room_list:
            return

        last_room = visited_room_list[-1]
        character.move(0 if last_room == 11 else 180, 1)

    def post_handler(self, enter_times, character: Character, **kwargs):
        fatigue_points = self.dungeon.get_fatigue_points()
        visited_room_list = kwargs.get('visited_room_list', [])
        if 0 < fatigue_points <= character.reserve_fatigue_points:
            LOGGER.info(
                f"Current fatigue points: {fatigue_points} is not greater than "
                f"{character.reserve_fatigue_points}, back to town"
            )

            self.dungeon.back_to_town()
        elif fatigue_points == 1:
            self.dungeon.re_enter()
        elif fatigue_points == 0 and 11 not in visited_room_list:
            self.move_to_next_room(character, Gate.DirectionLeft)
        else:
            self.move_to_next_room(character, Gate.DirectionRight)


class BwangaRoom11Handler(DungeonRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 11, character_class, strategy)

    @func_set_timeout(30)
    def move_to_next_room(self, character: Character):
        super().move_to_next_room(character, Gate.DirectionRight, Gate.DirectionDown, anchor_vector=(200, -700))

    def post_handler(self, enter_times, character: Character, **kwargs):
        fatigue_points = self.dungeon.get_fatigue_points()
        if 0 < fatigue_points <= character.reserve_fatigue_points:
            LOGGER.info(
                f"Current fatigue points: {fatigue_points} is not greater than "
                f"{character.reserve_fatigue_points}, back to town"
            )

            self.dungeon.back_to_town()
        elif fatigue_points == 1:
            self.dungeon.re_enter()
        else:
            self.move_to_next_room(character)
