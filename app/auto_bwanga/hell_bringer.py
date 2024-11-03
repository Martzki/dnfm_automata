from app.auto_bwanga.room_handler import *
from character.character import CharacterClass
from character.hell_bringer import HellBringer
from dungeon.strategy import BattleStrategy

default_battle_strategy = BattleStrategy()
default_battle_strategy.register_skill(HellBringer.Bloodlust, 10, 0)
default_battle_strategy.register_skill(HellBringer.GoreCross, 10, 0)


class Room0Handler(BwangaRoom0Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.HellBringer, default_battle_strategy)

    def pre_handler(self, enter_times, hell_bringer: HellBringer, **kwargs):
        if enter_times > 1:
            return

        hell_bringer.exec_skill(hell_bringer.derange, delay=0.3)
        hell_bringer.exec_skill(hell_bringer.thirst, delay=1)
        hell_bringer.move(345, 0.6)
        hell_bringer.exec_skill(hell_bringer.enrage)

    def post_handler(self, enter_times, hell_bringer: HellBringer, **kwargs):
        if enter_times == 1:
            hell_bringer.wait_skill_cool_down(hell_bringer.blood_sword)

        super().post_handler(enter_times, hell_bringer, **kwargs)


class Room1Handler(BwangaRoom1Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.HellBringer, default_battle_strategy)

    def pre_handler(self, enter_times, hell_bringer: HellBringer, **kwargs):
        if enter_times > 1:
            return

        hell_bringer.move(225, 0.5)
        hell_bringer.move(0, 0.2)
        hell_bringer.exec_skill(hell_bringer.blood_sword)

    def post_handler(self, enter_times, hell_bringer: HellBringer, **kwargs):
        if enter_times == 1:
            hell_bringer.wait_skill_cool_down(hell_bringer.raging_fury)
            hell_bringer.wait_skill_cool_down(hell_bringer.extreme_overkill)

        super().post_handler(enter_times, hell_bringer, **kwargs)


class Room2Handler(BwangaRoom2Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.HellBringer, default_battle_strategy)

    def pre_handler(self, enter_times, hell_bringer: HellBringer, **kwargs):
        if enter_times > 1:
            return

        hell_bringer.move(340, 0.6)
        hell_bringer.move(0, 0.1)
        hell_bringer.exec_skill(hell_bringer.raging_fury, delay=0.5)
        hell_bringer.exec_skill(hell_bringer.extreme_overkill)

    def post_handler(self, enter_times, hell_bringer: HellBringer, **kwargs):
        if enter_times == 1:
            hell_bringer.wait_skill_cool_down(hell_bringer.bloody_twister)

        super().post_handler(enter_times, hell_bringer, **kwargs)


class Room3Handler(BwangaRoom3Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.HellBringer, default_battle_strategy)

    def pre_handler(self, enter_times, hell_bringer: HellBringer, **kwargs):
        if enter_times > 1:
            return

        hell_bringer.move(345, 0.25)
        hell_bringer.exec_skill(hell_bringer.bloody_twister)

    def post_handler(self, enter_times, hell_bringer: HellBringer, **kwargs):
        if enter_times == 1:
            hell_bringer.wait_skill_cool_down(hell_bringer.enrage)

        super().post_handler(enter_times, hell_bringer, **kwargs)


class Room4Handler(BwangaRoom4Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.HellBringer, default_battle_strategy)

    def pre_handler(self, enter_times, hell_bringer: HellBringer, **kwargs):
        super().pre_handler(enter_times, hell_bringer, **kwargs)

        if enter_times > 1:
            return

        hell_bringer.move(140, 0.55)
        hell_bringer.move(0, 0.2)
        hell_bringer.exec_skill(hell_bringer.enrage)

    def post_handler(self, enter_times, hell_bringer: HellBringer, **kwargs):
        room_5_visited = kwargs.get("room_5_visited", False)
        if not room_5_visited:
            hell_bringer.wait_skill_cool_down(hell_bringer.extreme_overkill)
        else:
            hell_bringer.wait_skill_cool_down(hell_bringer.mountainous_wheel)
            hell_bringer.wait_skill_cool_down(hell_bringer.blood_sword)

        super().post_handler(enter_times, hell_bringer, **kwargs)


class Room5Handler(BwangaRoom5Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.HellBringer, default_battle_strategy)

    def pre_handler(self, enter_times, hell_bringer: HellBringer, **kwargs):
        if enter_times > 1:
            return

        hell_bringer.move(270, 0.3)
        hell_bringer.exec_skill(hell_bringer.extreme_overkill, delay=2.5)

        super().pre_handler(enter_times, hell_bringer, **kwargs)


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

        super().post_handler(enter_times, hell_bringer, **kwargs)


class Room7Handler(BwangaRoom7Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.HellBringer, default_battle_strategy)

    def pre_handler(self, enter_times, hell_bringer: HellBringer, **kwargs):
        if enter_times > 1:
            return

        hell_bringer.move(345, 0.3)
        hell_bringer.move(0, 0.15)
        hell_bringer.exec_skill(hell_bringer.enrage)

    def post_handler(self, enter_times, hell_bringer: HellBringer, **kwargs):
        if enter_times == 1:
            hell_bringer.wait_skill_cool_down(hell_bringer.outrage_break)

        super().post_handler(enter_times, hell_bringer, **kwargs)


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


class Room10Handler(BwangaRoom10Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.HellBringer, default_battle_strategy)


class Room11Handler(BwangaRoom11Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.HellBringer, default_battle_strategy)


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
