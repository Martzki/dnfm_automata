import time

from app.auto_battle.dungeons.pirates.handler.room_handler import *
from runtime.character.character_class import CharacterClass
from dungeon.strategy import BattleStrategy
from runtime.character.grand_master import GrandMaster


class Room0Handler(PiratesRoom0Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.GrandMaster, None)

    def pre_handler(self, enter_times, desperado: GrandMaster, **kwargs):
        if enter_times > 1:
            return

        desperado.exec_skill(desperado.overdrive, delay=0.5)
        desperado.move(0, 0.6)
        desperado.exec_skill(desperado.charge_crash)


class Room1Handler(PiratesRoom1Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.GrandMaster, None)

    def pre_handler(self, enter_times, desperado: GrandMaster, **kwargs):
        if enter_times > 1:
            return

        desperado.move(0, 0.7)
        desperado.exec_skill(desperado.continuous_slash)


class Room2Handler(PiratesRoom2Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.GrandMaster, None)

    def pre_handler(self, enter_times, desperado: GrandMaster, **kwargs):
        super().pre_handler(enter_times, desperado, **kwargs)

        if enter_times > 1:
            return

        desperado.move(0, 1)
        desperado.exec_skill(desperado.charge_burst)


class Room3Handler(PiratesRoom3Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.GrandMaster, None)

    def pre_handler(self, enter_times, desperado: GrandMaster, **kwargs):
        if enter_times > 1:
            return

        desperado.move(0, 1)
        desperado.exec_skill(desperado.charge_crash)


class Room4Handler(PiratesRoom4Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.GrandMaster, None)

    def pre_handler(self, enter_times, desperado: GrandMaster, **kwargs):
        if enter_times > 1:
            return

        desperado.exec_skill(desperado.flowing_stance_swift, duration=0.8, delay=0.25)
        desperado.exec_skill(desperado.draw_sword)


class Room5Handler(PiratesRoom5Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.GrandMaster, None)

    def pre_handler(self, enter_times, desperado: GrandMaster, **kwargs):
        super().pre_handler(enter_times, desperado, **kwargs)

        if enter_times > 1:
            return

        desperado.move(315, 0.25)
        desperado.move(0, 0.6)
        desperado.exec_skill(desperado.continuous_slash)


class Room6Handler(PiratesRoom6Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.GrandMaster, None)

    def pre_handler(self, enter_times, desperado: GrandMaster, **kwargs):
        if enter_times > 1:
            return

        desperado.move(0, 1)
        desperado.exec_skill(desperado.illusion_sword_dance)


class Room7Handler(PiratesRoom7Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.GrandMaster, None)


class Room8Handler(PiratesRoom8Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.GrandMaster, None)


class Room9Handler(PiratesRoom9Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.GrandMaster, None)


class Room10Handler(PiratesRoom10Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.GrandMaster, None)


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
    ]
