from app.auto_bwanga.room_handler import *
from character.character import CharacterClass
from character.evangelist import Evangelist
from dungeon.strategy import BattleStrategy

default_battle_strategy = BattleStrategy()


# default_battle_strategy.register_skill(Evangelist., 10, 0)


class Room0Handler(BwangaRoom0Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Evangelist, default_battle_strategy)

    def pre_handler(self, enter_times, evangelist: Evangelist, **kwargs):
        if enter_times > 1:
            return

        evangelist.move(335, 0.45)
        evangelist.exec_skill(evangelist.grand_crashing_cross)

    def post_handler(self, enter_times, evangelist: Evangelist, **kwargs):
        if enter_times == 1:
            evangelist.wait_skill_cool_down(evangelist.saint_wall)
            evangelist.wait_skill_cool_down(evangelist.purifying_lightning)

        self.move_to_next_room(evangelist, enter_times)


class Room1Handler(BwangaRoom1Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Evangelist, default_battle_strategy)

    def pre_handler(self, enter_times, evangelist: Evangelist, **kwargs):
        if enter_times > 1:
            return

        evangelist.move(270, 0.5)
        evangelist.move(0, 0.07)
        evangelist.exec_skill(evangelist.saint_wall)
        evangelist.exec_skill(evangelist.christening_light)

    def post_handler(self, enter_times, evangelist: Evangelist, **kwargs):
        if enter_times == 1:
            evangelist.wait_skill_cool_down(evangelist.spear_of_victory)
            evangelist.wait_skill_cool_down(evangelist.purifying_lightning)

        self.move_to_next_room(evangelist, enter_times)


class Room2Handler(BwangaRoom2Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Evangelist, default_battle_strategy)

    def pre_handler(self, enter_times, evangelist: Evangelist, **kwargs):
        if enter_times > 1:
            return

        evangelist.move(280, 0.35)
        evangelist.exec_skill(evangelist.spear_of_victory, delay=0.25)
        evangelist.exec_skill(evangelist.purifying_lightning)

    def post_handler(self, enter_times, evangelist: Evangelist, **kwargs):
        if enter_times == 1:
            evangelist.wait_skill_cool_down(evangelist.valiant_aria)

        self.move_to_next_room(evangelist, enter_times)


class Room3Handler(BwangaRoom3Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Evangelist, default_battle_strategy)

    def pre_handler(self, enter_times, evangelist: Evangelist, **kwargs):
        if enter_times > 1:
            return

        evangelist.move(345, 0.6)
        evangelist.exec_skill(evangelist.valiant_aria)

    def post_handler(self, enter_times, evangelist: Evangelist, **kwargs):
        if enter_times == 1:
            evangelist.wait_skill_cool_down(evangelist.shining_cross)

        self.move_to_next_room(evangelist, enter_times)


class Room4Handler(BwangaRoom4Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Evangelist, default_battle_strategy)

    def pre_handler(self, enter_times, evangelist: Evangelist, **kwargs):
        super().pre_handler(enter_times, evangelist, **kwargs)

        if enter_times > 1:
            return

        evangelist.move(145, 0.4)
        evangelist.move(45, 0.4)
        evangelist.exec_skill(evangelist.shining_cross)

    def post_handler(self, enter_times, evangelist: Evangelist, **kwargs):
        if enter_times == 1:
            evangelist.wait_skill_cool_down(evangelist.crux_of_victoria)
        elif enter_times == 2:
            evangelist.wait_skill_cool_down(evangelist.saint_wall)
            evangelist.wait_skill_cool_down(evangelist.christening_light)

        self.move_to_next_room(evangelist, enter_times, kwargs.get("room_5_visited", False))


class Room5Handler(BwangaRoom5Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Evangelist, default_battle_strategy)

    def pre_handler(self, enter_times, evangelist: Evangelist, **kwargs):
        if enter_times > 1:
            return

        evangelist.move(270, 0.5)
        evangelist.exec_skill(evangelist.crux_of_victoria, delay=7)

    def post_handler(self, enter_times, evangelist: Evangelist, **kwargs):
        self.move_to_next_room(evangelist, enter_times)


class Room6Handler(BwangaRoom6Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Evangelist, default_battle_strategy)

    def pre_handler(self, enter_times, evangelist: Evangelist, **kwargs):
        if enter_times > 1:
            return

        evangelist.move(0, 0.5)
        evangelist.move(270, 0.2)
        evangelist.exec_skill(evangelist.saint_wall)
        evangelist.exec_skill(evangelist.christening_light)

    def post_handler(self, enter_times, evangelist: Evangelist, **kwargs):
        if enter_times == 1:
            evangelist.wait_skill_cool_down(evangelist.purifying_lightning)

        self.move_to_next_room(evangelist, enter_times, kwargs.get("room_5_visited", False))


class Room7Handler(BwangaRoom7Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Evangelist, default_battle_strategy)

    def pre_handler(self, enter_times, character: Evangelist, **kwargs):
        if enter_times > 1:
            return

        character.move(270, 0.15)
        character.move(0, 0.1)
        character.exec_skill(character.purifying_lightning)

    def post_handler(self, enter_times, evangelist: Evangelist, **kwargs):
        if enter_times == 1:
            evangelist.wait_skill_cool_down(evangelist.grand_crashing_cross)
            evangelist.wait_skill_cool_down(evangelist.shining_cross)

        self.move_to_next_room(evangelist, enter_times)


class Room8Handler(BwangaRoom8Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Evangelist, default_battle_strategy)

    def pre_handler(self, enter_times, evangelist: Evangelist, **kwargs):
        if enter_times > 1:
            return

        evangelist.move(0, 0.5)
        evangelist.exec_skill(evangelist.grand_crashing_cross, delay=0.15)
        evangelist.exec_skill(evangelist.shining_cross)


class Room9Handler(BwangaRoom9Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Evangelist, default_battle_strategy)

    def pre_handler(self, enter_times, evangelist: Evangelist, **kwargs):
        pass

    def post_handler(self, enter_times, evangelist: Evangelist, **kwargs):
        self.move_to_next_room(evangelist, enter_times)


class Room10Handler(BwangaRoom10Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Evangelist, default_battle_strategy)

    def pre_handler(self, enter_times, evangelist: Evangelist, **kwargs):
        pass

    def post_handler(self, enter_times, evangelist: Evangelist, **kwargs):
        self.move_to_next_room(evangelist, enter_times)


class Room11Handler(BwangaRoom11Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Evangelist, default_battle_strategy)

    def pre_handler(self, enter_times, evangelist: Evangelist, **kwargs):
        pass

    def post_handler(self, enter_times, evangelist: Evangelist, **kwargs):
        self.move_to_next_room(evangelist, enter_times)


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
