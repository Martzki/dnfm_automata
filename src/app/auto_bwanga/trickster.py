from src.app.auto_bwanga.room_handler import *
from src.lib.character.character import CharacterClass
from src.lib.character.trickster import Trickster
from src.lib.dungeon.dungeon import DungeonRoomHandler
from src.lib.dungeon.strategy import BattleStrategy

default_battle_strategy = BattleStrategy()
default_battle_strategy.register_skill(Trickster.EnhancedMagicMissile, 10, 0)


class Room0Handler(BwangaRoom0Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Trickster, default_battle_strategy)

    def pre_handler(self, enter_times, trickster: Trickster, **kwargs):
        if enter_times > 1:
            return

        trickster.exec_skill(trickster.lollipop, delay=0.3)
        trickster.exec_skill(trickster.showtime)
        trickster.move(335, 0.45)
        trickster.exec_skill(trickster.cheeky_doll_shururu, delay=0.75)
        trickster.exec_skill(trickster.cheeky_doll_shururu)

    def post_handler(self, enter_times, trickster: Trickster, **kwargs):
        if enter_times == 1:
            trickster.wait_skill_cool_down(trickster.lava_potion_no_9)

        self.move_to_next_room(trickster, enter_times)


class Room1Handler(BwangaRoom1Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Trickster, default_battle_strategy)

    def pre_handler(self, enter_times, trickster: Trickster, **kwargs):
        if enter_times > 1:
            return

        trickster.move(270, 0.5)
        trickster.move(0, 0.07)
        trickster.exec_skill(trickster.lava_potion_no_9)

    def post_handler(self, enter_times, trickster: Trickster, **kwargs):
        if enter_times == 1:
            trickster.wait_skill_cool_down(trickster.acid_rain)

        self.move_to_next_room(trickster, enter_times)


class Room2Handler(BwangaRoom2Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Trickster, default_battle_strategy)

    def pre_handler(self, enter_times, trickster: Trickster, **kwargs):
        if enter_times > 1:
            return

        trickster.move(280, 0.3)
        trickster.exec_skill(trickster.acid_rain)

    def post_handler(self, enter_times, trickster: Trickster, **kwargs):
        if enter_times == 1:
            trickster.wait_skill_cool_down(trickster.gravitas)

        self.move_to_next_room(trickster, enter_times)


class Room3Handler(BwangaRoom3Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Trickster, default_battle_strategy)

    def pre_handler(self, enter_times, trickster: Trickster, **kwargs):
        if enter_times > 1:
            return

        trickster.move(345, 0.6)
        trickster.exec_skill(trickster.gravitas)

    def post_handler(self, enter_times, trickster: Trickster, **kwargs):
        if enter_times == 1:
            trickster.wait_skill_cool_down(trickster.lava_potion_no_9)

        self.move_to_next_room(trickster, enter_times)


class Room4Handler(BwangaRoom4Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Trickster, default_battle_strategy)

    def pre_handler(self, enter_times, trickster: Trickster, **kwargs):
        if enter_times > 1:
            return

        trickster.move(145, 0.4)
        trickster.move(0, 0.1)
        trickster.exec_skill(trickster.lava_potion_no_9)

    def post_handler(self, enter_times, trickster: Trickster, **kwargs):
        if enter_times == 1:
            trickster.wait_skill_cool_down(trickster.fusion_craft)
        elif enter_times == 2:
            trickster.wait_skill_cool_down(trickster.cheeky_doll_shururu)

        self.move_to_next_room(trickster, enter_times, kwargs.get("room_5_visited", False))


class Room5Handler(BwangaRoom5Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Trickster, default_battle_strategy)

    def pre_handler(self, enter_times, trickster: Trickster, **kwargs):
        if enter_times > 1:
            return

        trickster.move(250, 0.4)
        trickster.exec_skill(trickster.fusion_craft, delay=8)
        trickster.move(180, 0.4)

    def post_handler(self, enter_times, trickster: Trickster, **kwargs):
        self.move_to_next_room(trickster, enter_times)


class Room6Handler(BwangaRoom6Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Trickster, default_battle_strategy)

    def pre_handler(self, enter_times, trickster: Trickster, **kwargs):
        if enter_times > 1:
            return

        trickster.move(0, 0.5)
        trickster.move(270, 0.2)
        trickster.exec_skill(trickster.cheeky_doll_shururu, delay=0.75)
        trickster.exec_skill(trickster.cheeky_doll_shururu)

    def post_handler(self, enter_times, trickster: Trickster, **kwargs):
        if enter_times == 1:
            trickster.wait_skill_cool_down(trickster.lava_potion_no_9)

        self.move_to_next_room(trickster, enter_times)


class Room7Handler(BwangaRoom7Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Trickster, default_battle_strategy)

    def pre_handler(self, enter_times, trickster: Trickster, **kwargs):
        if enter_times > 1:
            return

        trickster.move(345, 0.3)
        trickster.exec_skill(trickster.lava_potion_no_9)

    def post_handler(self, enter_times, trickster: Trickster, **kwargs):
        if enter_times == 1:
            trickster.wait_skill_cool_down(trickster.gravitas)

        self.move_to_next_room(trickster, enter_times)


class Room8Handler(BwangaRoom8Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Trickster, default_battle_strategy)

    def pre_handler(self, enter_times, trickster: Trickster, **kwargs):
        if enter_times > 1:
            return

        trickster.move(0, 0.5)
        trickster.exec_skill(trickster.gravitas)
        trickster.exec_skill(trickster.acid_rain)
        trickster.exec_skill(trickster.snow_man)


class Room9Handler(BwangaRoom9Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Trickster, default_battle_strategy)

    def pre_handler(self, enter_times, trickster: Trickster, **kwargs):
        pass

    def post_handler(self, enter_times, trickster: Trickster, **kwargs):
        self.move_to_next_room(trickster, enter_times)


class Room10Handler(BwangaRoom10Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Trickster, default_battle_strategy)

    def pre_handler(self, enter_times, trickster: Trickster, **kwargs):
        pass

    def post_handler(self, enter_times, trickster: Trickster, **kwargs):
        self.move_to_next_room(trickster, enter_times)


class Room11Handler(BwangaRoom11Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Trickster, default_battle_strategy)

    def pre_handler(self, enter_times, trickster: Trickster, **kwargs):
        pass

    def post_handler(self, enter_times, trickster: Trickster, **kwargs):
        self.move_to_next_room(trickster, enter_times)


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
