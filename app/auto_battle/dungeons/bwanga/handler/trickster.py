from app.auto_battle.dungeons.bwanga.handler.room_handler import *
from dungeon.strategy import BattleStrategy
from runtime.character.character_class import CharacterClass
from runtime.character.trickster import Trickster

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

        super().post_handler(enter_times, trickster, **kwargs)


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

        super().post_handler(enter_times, trickster, **kwargs)


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

        super().post_handler(enter_times, trickster, **kwargs)


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

        super().post_handler(enter_times, trickster, **kwargs)


class Room4Handler(BwangaRoom4Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Trickster, default_battle_strategy)

    def pre_handler(self, enter_times, trickster: Trickster, **kwargs):
        super().pre_handler(enter_times, trickster, **kwargs)

        if enter_times > 1:
            return

        trickster.move(145, 0.4)
        trickster.move(0, 0.1)
        trickster.exec_skill(trickster.lava_potion_no_9)

    def post_handler(self, enter_times, trickster: Trickster, **kwargs):
        room_5_visited = 5 in kwargs.get('visited_room_list', [])
        if not room_5_visited:
            trickster.wait_skill_cool_down(trickster.fusion_craft)
        else:
            trickster.wait_skill_cool_down(trickster.cheeky_doll_shururu)

        super().post_handler(enter_times, trickster, **kwargs)


class Room5Handler(BwangaRoom5Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Trickster, default_battle_strategy)

    def pre_handler(self, enter_times, trickster: Trickster, **kwargs):
        if enter_times > 1:
            return

        trickster.move(250, 0.4)
        trickster.exec_skill(trickster.fusion_craft, delay=8.5)

        super().pre_handler(enter_times, trickster, **kwargs)


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

        super().post_handler(enter_times, trickster, **kwargs)


class Room7Handler(BwangaRoom7Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Trickster, default_battle_strategy)

    def pre_handler(self, enter_times, trickster: Trickster, **kwargs):
        super().pre_handler(enter_times, trickster, **kwargs)
        if enter_times > 1:
            return

        trickster.move(345, 0.3)
        trickster.exec_skill(trickster.lava_potion_no_9)

    def post_handler(self, enter_times, trickster: Trickster, **kwargs):
        if enter_times == 1:
            trickster.wait_skill_cool_down(trickster.gravitas)

        super().post_handler(enter_times, trickster, **kwargs)


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


class Room10Handler(BwangaRoom10Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Trickster, default_battle_strategy)


class Room11Handler(BwangaRoom11Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Trickster, default_battle_strategy)


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
