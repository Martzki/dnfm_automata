import time

from app.auto_battle.dungeons.bwanga.handler.room_handler import *
from runtime.character.character_class import CharacterClass
from runtime.character.noblesse import Noblesse
from dungeon.strategy import BattleStrategy


class DefaultBattleStrategy(BattleStrategy):
    def __init__(self):
        super().__init__()
        self.register_skill(Noblesse.SwiftSword, 10, 0)
        self.register_skill(Noblesse.IllusionSword, 20, 0)
        self.register_skill(Noblesse.TossingSlash, 30, 0)


class Room0Handler(BwangaRoom0Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Noblesse, DefaultBattleStrategy())

    def pre_handler(self, enter_times, noblesse: Noblesse, **kwargs):
        if enter_times > 1:
            return

        noblesse.exec_skill(noblesse.elemental_shift, swipe_angle=90)
        noblesse.exec_skill(noblesse.sentiment_du_fer_critical)
        noblesse.move(335, 0.5)
        time.sleep(0.35)
        noblesse.move(0, 0.4)
        noblesse.exec_skill(noblesse.illusion_sword, delay=0.3)
        noblesse.exec_skill(noblesse.ascent)

    def post_handler(self, enter_times, noblesse: Noblesse, **kwargs):
        if enter_times == 1:
            noblesse.wait_skill_cool_down(noblesse.arcane_sword_blast)

        super().post_handler(enter_times, noblesse, **kwargs)


class Room1Handler(BwangaRoom1Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Noblesse, DefaultBattleStrategy())

    def pre_handler(self, enter_times, noblesse: Noblesse, **kwargs):
        if enter_times > 1:
            return

        noblesse.move(250, 0.5)
        noblesse.move(0, 0.07)
        noblesse.exec_skill(noblesse.arcane_sword_blast)

    def post_handler(self, enter_times, noblesse: Noblesse, **kwargs):
        if enter_times == 1:
            noblesse.wait_skill_cool_down(noblesse.illusion_sword)
            noblesse.wait_skill_cool_down(noblesse.ascent)

        super().post_handler(enter_times, noblesse, **kwargs)


class Room2Handler(BwangaRoom2Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Noblesse, DefaultBattleStrategy())

    def pre_handler(self, enter_times, noblesse: Noblesse, **kwargs):
        if enter_times > 1:
            return

        noblesse.move(270, 0.4)
        time.sleep(0.2)
        noblesse.exec_skill(noblesse.illusion_sword)
        noblesse.exec_skill(noblesse.ascent)

    def post_handler(self, enter_times, noblesse: Noblesse, **kwargs):
        if enter_times == 1:
            noblesse.wait_skill_cool_down(noblesse.crescent)

        super().post_handler(enter_times, noblesse, **kwargs)


class Room3Handler(BwangaRoom3Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Noblesse, DefaultBattleStrategy())

    def pre_handler(self, enter_times, noblesse: Noblesse, **kwargs):
        if enter_times > 1:
            return

        noblesse.move(345, 0.4)
        noblesse.exec_skill(noblesse.crescent)

    def post_handler(self, enter_times, noblesse: Noblesse, **kwargs):
        if enter_times == 1:
            noblesse.wait_skill_cool_down(noblesse.flash)

        super().post_handler(enter_times, noblesse, **kwargs)


class Room4Handler(BwangaRoom4Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Noblesse, DefaultBattleStrategy())

    def pre_handler(self, enter_times, noblesse: Noblesse, **kwargs):
        super().pre_handler(enter_times, noblesse, **kwargs)

        if enter_times > 1:
            return

        noblesse.move(155, 0.6)
        noblesse.move(180, 0.45)
        time.sleep(0.1)
        noblesse.move(0, 0.2)
        noblesse.exec_skill(noblesse.flash)

    def post_handler(self, enter_times, noblesse: Noblesse, **kwargs):
        room_5_visited = 5 in kwargs.get('visited_room_list', [])
        if not room_5_visited:
            noblesse.wait_skill_cool_down(noblesse.ultimate_slayer_technique_spacetime_cutter)
        else:
            noblesse.wait_skill_cool_down(noblesse.arcane_sword_blast)

        super().post_handler(enter_times, noblesse, **kwargs)


class Room5Handler(BwangaRoom5Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Noblesse, DefaultBattleStrategy())

    def pre_handler(self, enter_times, noblesse: Noblesse, **kwargs):
        if enter_times > 1:
            return

        noblesse.exec_skill(noblesse.ultimate_slayer_technique_spacetime_cutter)
        noblesse.move(180, 0.5)

        super().pre_handler(enter_times, noblesse, **kwargs)


class Room6Handler(BwangaRoom6Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Noblesse, DefaultBattleStrategy())

    def pre_handler(self, enter_times, noblesse: Noblesse, **kwargs):
        if enter_times > 1:
            return

        noblesse.move(270, 0.4)
        noblesse.exec_skill(noblesse.arcane_sword_blast)

    def post_handler(self, enter_times, noblesse: Noblesse, **kwargs):
        if enter_times == 1:
            noblesse.wait_skill_cool_down(noblesse.crescent)

        super().post_handler(enter_times, noblesse, **kwargs)


class Room7Handler(BwangaRoom7Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Noblesse, DefaultBattleStrategy())

    def pre_handler(self, enter_times, noblesse: Noblesse, **kwargs):
        super().pre_handler(enter_times, noblesse, **kwargs)
        if enter_times > 1:
            return

        noblesse.move(345, 0.5)
        noblesse.exec_skill(noblesse.crescent, duration=0.7, delay=0.5)

    def post_handler(self, enter_times, noblesse: Noblesse, **kwargs):
        if enter_times == 1:
            noblesse.wait_skill_cool_down(noblesse.swift_demon_slash)

        super().post_handler(enter_times, noblesse, **kwargs)


class Room8Handler(BwangaRoom8Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Noblesse, DefaultBattleStrategy())

    def pre_handler(self, enter_times, noblesse: Noblesse, **kwargs):
        if enter_times > 1:
            return

        noblesse.move(0, 0.5)
        noblesse.exec_skill(noblesse.swift_demon_slash)


class Room9Handler(BwangaRoom9Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Noblesse, DefaultBattleStrategy())


class Room10Handler(BwangaRoom10Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Noblesse, DefaultBattleStrategy())


class Room11Handler(BwangaRoom11Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Noblesse, DefaultBattleStrategy())


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
