from src.app.auto_bwanga.room_handler import *
from src.lib.character.character import CharacterClass
from src.lib.character.hell_bringer import HellBringer
from src.lib.dungeon.strategy import BattleStrategy

default_battle_strategy = BattleStrategy()
default_battle_strategy.register_skill(HellBringer.Bloodlust, 10, 0)
default_battle_strategy.register_skill(HellBringer.GoreCross, 10, 0)


class Room0Handler(BwangaRoom0Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.HellBringer, default_battle_strategy)

    def pre_handler(self, enter_times, hell_bringer: HellBringer, **kwargs):
        if enter_times > 1:
            return

        hell_bringer.exec_skill(hell_bringer.derange, delay=0.5)
        # time.sleep(0.3)
        hell_bringer.exec_skill(hell_bringer.thirst, delay=0.4)
        # time.sleep(0.3)
        hell_bringer.move(345, 0.6)
        hell_bringer.exec_skill(hell_bringer.enrage)

    def post_handler(self, enter_times, hell_bringer: HellBringer, **kwargs):
        if enter_times == 1:
            hell_bringer.wait_skill_cool_down(hell_bringer.blood_sword)

        self.move_to_next_room(hell_bringer, enter_times)


class Room1Handler(BwangaRoom1Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.HellBringer, default_battle_strategy)

    def pre_handler(self, enter_times, hell_bringer: HellBringer, **kwargs):
        if enter_times > 1:
            return

        hell_bringer.move(225, 0.5)
        hell_bringer.move(0, 0.15)
        hell_bringer.exec_skill(hell_bringer.blood_sword)

    def post_handler(self, enter_times, hell_bringer: HellBringer, **kwargs):
        if enter_times == 1:
            hell_bringer.wait_skill_cool_down(hell_bringer.raging_fury)
            hell_bringer.wait_skill_cool_down(hell_bringer.extreme_overkill)

        self.move_to_next_room(hell_bringer, enter_times)


class Room2Handler(BwangaRoom2Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.HellBringer, default_battle_strategy)

    def pre_handler(self, enter_times, hell_bringer: HellBringer, **kwargs):
        if enter_times > 1:
            return

        hell_bringer.move(340, 0.6)
        hell_bringer.move(0, 0.2)
        hell_bringer.exec_skill(hell_bringer.raging_fury)
        hell_bringer.exec_skill(hell_bringer.extreme_overkill)

    def post_handler(self, enter_times, hell_bringer: HellBringer, **kwargs):
        if enter_times == 1:
            hell_bringer.wait_skill_cool_down(hell_bringer.bloody_twister)

        self.move_to_next_room(hell_bringer, enter_times)


class Room3Handler(BwangaRoom3Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.HellBringer, default_battle_strategy)

    def pre_handler(self, enter_times, hell_bringer: HellBringer, **kwargs):
        if enter_times > 1:
            return

        hell_bringer.move(345, 0.4)
        hell_bringer.exec_skill(hell_bringer.bloody_twister)

    def post_handler(self, enter_times, hell_bringer: HellBringer, **kwargs):
        if enter_times == 1:
            hell_bringer.wait_skill_cool_down(hell_bringer.enrage)

        self.move_to_next_room(hell_bringer, enter_times)


class Room4Handler(BwangaRoom4Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.HellBringer, default_battle_strategy)

    def pre_handler(self, enter_times, hell_bringer: HellBringer, **kwargs):
        if enter_times > 1:
            return

        hell_bringer.move(140, 0.7)
        hell_bringer.move(0, 0.2)
        hell_bringer.exec_skill(hell_bringer.enrage)

    def post_handler(self, enter_times, hell_bringer: HellBringer, **kwargs):
        if enter_times == 1:
            hell_bringer.wait_skill_cool_down(hell_bringer.extreme_overkill)
        elif enter_times == 2:
            hell_bringer.wait_skill_cool_down(hell_bringer.mountainous_wheel)
            hell_bringer.wait_skill_cool_down(hell_bringer.blood_sword)

        self.move_to_next_room(hell_bringer, enter_times, kwargs.get("room_5_visited", False))


class Room5Handler(BwangaRoom5Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.HellBringer, default_battle_strategy)

    def pre_handler(self, enter_times, hell_bringer: HellBringer, **kwargs):
        if enter_times > 1:
            return

        hell_bringer.move(270, 0.3)
        hell_bringer.exec_skill(hell_bringer.extreme_overkill)

    def post_handler(self, enter_times, hell_bringer: HellBringer, **kwargs):
        self.move_to_next_room(hell_bringer, enter_times)


class Room6Handler(BwangaRoom6Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.HellBringer, default_battle_strategy)

    def pre_handler(self, enter_times, hell_bringer: HellBringer, **kwargs):
        if enter_times > 1:
            return

        hell_bringer.move(270, 0.3)
        # hell_bringer.move(270, 0.2)
        hell_bringer.exec_skill(hell_bringer.mountainous_wheel)
        hell_bringer.exec_skill(hell_bringer.attack, 1.5)
        hell_bringer.exec_skill(hell_bringer.blood_sword)

    def post_handler(self, enter_times, hell_bringer: HellBringer, **kwargs):
        if enter_times == 1:
            hell_bringer.wait_skill_cool_down(hell_bringer.enrage)

        self.move_to_next_room(hell_bringer, enter_times)


class Room7Handler(BwangaRoom7Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.HellBringer, default_battle_strategy)

    def pre_handler(self, enter_times, hell_bringer: HellBringer, **kwargs):
        if enter_times > 1:
            return

        hell_bringer.move(345, 0.3)
        hell_bringer.move(0, 0.1)
        hell_bringer.exec_skill(hell_bringer.enrage)

    def post_handler(self, enter_times, hell_bringer: HellBringer, **kwargs):
        if enter_times == 1:
            hell_bringer.wait_skill_cool_down(hell_bringer.outrage_break)

        self.move_to_next_room(hell_bringer, enter_times)


class Room8Handler(BwangaRoom8Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.HellBringer, default_battle_strategy)

    def pre_handler(self, enter_times, hell_bringer: HellBringer, **kwargs):
        if enter_times > 1:
            return

        hell_bringer.move(0, 0.2)
        hell_bringer.exec_skill(hell_bringer.outrage_break)
        hell_bringer.move(0, 0.1)
        hell_bringer.exec_skill(hell_bringer.attack, 3)


class Room9Handler(BwangaRoom9Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.HellBringer, default_battle_strategy)

    def pre_handler(self, enter_times, hell_bringer: HellBringer, **kwargs):
        pass

    def post_handler(self, enter_times, hell_bringer: HellBringer, **kwargs):
        self.move_to_next_room(hell_bringer, enter_times)


class Room10Handler(BwangaRoom10Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.HellBringer, default_battle_strategy)

    def pre_handler(self, enter_times, hell_bringer: HellBringer, **kwargs):
        pass

    def post_handler(self, enter_times, hell_bringer: HellBringer, **kwargs):
        self.move_to_next_room(hell_bringer, enter_times)


class Room11Handler(BwangaRoom11Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.HellBringer, default_battle_strategy)

    def pre_handler(self, enter_times, hell_bringer: HellBringer, **kwargs):
        pass

    def post_handler(self, enter_times, hell_bringer: HellBringer, **kwargs):
        self.move_to_next_room(hell_bringer, enter_times)


def init_handlers(dungeon):
    return [
        Room0Handler(dungeon),
        Room1Handler(dungeon),
        Room2Handler(dungeon),
        Room3Handler(dungeon),
        Room4Handler(dungeon),
        Room5Handler(dungeon),
        Room6Handler(dungeon),
        Room7Handler(dungeon),
        Room8Handler(dungeon),
        Room9Handler(dungeon),
        Room10Handler(dungeon),
        Room11Handler(dungeon),
    ]
