import time

from func_timeout import func_set_timeout, FunctionTimedOut

from character.character import Character
from common.log import Logger
from common.util import timeout_handler
from dungeon.battle import Gate
from dungeon.dungeon import DungeonRoomHandler, DungeonFinished
from runtime.ui import ui_elements

LOGGER = Logger(__name__).logger


class PiratesRoomHandler(DungeonRoomHandler):
    def __init__(self, dungeon, room_id, character_class, strategy=None):
        super().__init__(dungeon, room_id, character_class, strategy)
        self.search_angle = (0, 180)


class PiratesRoom0Handler(PiratesRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 0, character_class, strategy)

    @func_set_timeout(30)
    def move_to_next_room(self, character: Character):
        super().move_to_next_room(character, Gate.DirectionRight)

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


class PiratesRoom1Handler(PiratesRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 1, character_class, strategy)

    @func_set_timeout(30)
    def move_to_next_room(self, character: Character):
        super().move_to_next_room(character, Gate.DirectionRight, Gate.DirectionLeft, anchor_vector=(1000, 200))

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


class PiratesRoom2Handler(PiratesRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 2, character_class, strategy)

    def pre_handler(self, enter_times, character: Character, **kwargs):
        visited_room_list = kwargs.get('visited_room_list', [])
        if len(visited_room_list) > 0 and visited_room_list[-1] == 7:
            character.move(340, 0.5)

    @func_set_timeout(30)
    def move_to_next_room(self, character: Character, direction):
        if direction == Gate.DirectionRight:
            super().move_to_next_room(character, Gate.DirectionRight, Gate.DirectionUp, anchor_vector=(400, 200))
        else:
            super().move_to_next_room(character, Gate.DirectionUp, Gate.DirectionLeft, anchor_vector=(500, 0))

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
        elif fatigue_points == 0 and 7 not in visited_room_list:
            self.move_to_next_room(character, Gate.DirectionUp)
        else:
            self.move_to_next_room(character, Gate.DirectionRight)


class PiratesRoom3Handler(PiratesRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 3, character_class, strategy)

    @func_set_timeout(30)
    def move_to_next_room(self, character: Character):
        super().move_to_next_room(character, Gate.DirectionRight, Gate.DirectionLeft, anchor_vector=(1000, 200))

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
        else:
            self.move_to_next_room(character)


class PiratesRoom4Handler(PiratesRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 4, character_class, strategy)

    @func_set_timeout(30)
    def move_to_next_room(self, character: Character):
        super().move_to_next_room(character, Gate.DirectionRight, Gate.DirectionLeft, anchor_vector=(1000, -200))

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
        else:
            self.move_to_next_room(character)


class PiratesRoom5Handler(PiratesRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 5, character_class, strategy)

    def pre_handler(self, enter_times, character: Character, **kwargs):
        visited_room_list = kwargs.get('visited_room_list', [])
        if len(visited_room_list) > 0 and visited_room_list[-1] == 9:
            character.move(340, 0.3)
            time.sleep(1)

    @func_set_timeout(30)
    def move_to_next_room(self, character: Character, direction):
        if direction == Gate.DirectionUp:
            super().move_to_next_room(character, Gate.DirectionUp, Gate.DirectionLeft, anchor_vector=(500, 0))
        else:
            super().move_to_next_room(character, Gate.DirectionRight, Gate.DirectionUp, anchor_vector=(500, 200))

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
        elif fatigue_points == 0 and 9 not in visited_room_list:
            self.move_to_next_room(character, Gate.DirectionUp)
        else:
            self.move_to_next_room(character, Gate.DirectionRight)


class PiratesRoom6Handler(PiratesRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 6, character_class, strategy)

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


class PiratesRoom7Handler(PiratesRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 7, character_class, strategy)

    @func_set_timeout(30)
    def move_to_next_room(self, character: Character, direction):
        if direction == Gate.DirectionLeft:
            super().move_to_next_room(character, Gate.DirectionLeft, Gate.DirectionDown, anchor_vector=(0, -300))
        else:
            super().move_to_next_room(character, Gate.DirectionDown, Gate.DirectionLeft, anchor_vector=(500, 200))

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
        elif fatigue_points == 0 and 8 not in visited_room_list:
            self.move_to_next_room(character, Gate.DirectionLeft)
        else:
            self.move_to_next_room(character, Gate.DirectionDown)


class PiratesRoom8Handler(PiratesRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 8, character_class, strategy)

    @func_set_timeout(30)
    def move_to_next_room(self, character: Character):
        super().move_to_next_room(character, Gate.DirectionRight)

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
        else:
            self.move_to_next_room(character)


class PiratesRoom9Handler(PiratesRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 9, character_class, strategy)

    @func_set_timeout(30)
    def move_to_next_room(self, character: Character, direction):
        if direction == Gate.DirectionDown:
            super().move_to_next_room(character, Gate.DirectionDown, Gate.DirectionRight, anchor_vector=(-500, 0))
        else:
            super().move_to_next_room(character, Gate.DirectionRight, Gate.DirectionDown, anchor_vector=(300, -200))

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
            self.move_to_next_room(character, Gate.DirectionRight)
        else:
            self.move_to_next_room(character, Gate.DirectionDown)


class PiratesRoom10Handler(PiratesRoomHandler):
    def __init__(self, dungeon, character_class, strategy):
        super().__init__(dungeon, 10, character_class, strategy)

    @func_set_timeout(30)
    def move_to_next_room(self, character: Character):
        super().move_to_next_room(character, Gate.DirectionLeft)

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
