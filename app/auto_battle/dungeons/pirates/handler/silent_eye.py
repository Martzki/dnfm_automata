from app.auto_battle.dungeons.pirates.handler.room_handler import *
from dungeon.strategy import BattleStrategy
from runtime.character.character_class import CharacterClass
from runtime.character.silent_eye import SilentEye


class DefaultBattleStrategy(BattleStrategy):
    def __init__(self):
        super().__init__()
        self.register_skill(SilentEye.WaveRadiation, 10, 0)


class Room0Handler(PiratesRoom0Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.SilentEye, DefaultBattleStrategy())

    def pre_handler(self, enter_times, silent_eye: SilentEye, **kwargs):
        if enter_times > 1:
            return

        silent_eye.exec_skill(silent_eye.murderous_wave, delay=0.5)
        silent_eye.move(0, 0.4)
        silent_eye.exec_skill(silent_eye.ice_wave_sword)


class Room1Handler(PiratesRoom1Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.SilentEye, DefaultBattleStrategy())

    def pre_handler(self, enter_times, silent_eye: SilentEye, **kwargs):
        if enter_times > 1:
            return

        silent_eye.move(0, 0.35)
        silent_eye.exec_skill(silent_eye.fire_wave_sword)


class Room2Handler(PiratesRoom2Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.SilentEye, DefaultBattleStrategy())

    def pre_handler(self, enter_times, silent_eye: SilentEye, **kwargs):
        super().pre_handler(enter_times, silent_eye, **kwargs)

        if enter_times > 1:
            return

        silent_eye.move(0, 1.15)
        silent_eye.exec_skill(silent_eye.spirit_crescent)


class Room3Handler(PiratesRoom3Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.SilentEye, DefaultBattleStrategy())

    def pre_handler(self, enter_times, silent_eye: SilentEye, **kwargs):
        if enter_times > 1:
            return

        silent_eye.move(0, 1.25)
        silent_eye.exec_skill(silent_eye.deadly_enticer, delay=1)
        silent_eye.exec_skill(silent_eye.deadly_enticer)


class Room4Handler(PiratesRoom4Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.SilentEye, DefaultBattleStrategy())

    def pre_handler(self, enter_times, silent_eye: SilentEye, **kwargs):
        if enter_times > 1:
            return

        silent_eye.exec_skill(silent_eye.ice_wave_sword)
        silent_eye.move(0, 1)


class Room5Handler(PiratesRoom5Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.SilentEye, DefaultBattleStrategy())

    def pre_handler(self, enter_times, silent_eye: SilentEye, **kwargs):
        super().pre_handler(enter_times, silent_eye, **kwargs)

        if enter_times > 1:
            return

        silent_eye.move(315, 0.25)
        silent_eye.move(0, 0.6)
        silent_eye.exec_skill(silent_eye.spirit_crescent)


class Room6Handler(PiratesRoom6Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.SilentEye, DefaultBattleStrategy())

    def pre_handler(self, enter_times, silent_eye: SilentEye, **kwargs):
        if enter_times > 1:
            return

        silent_eye.move(0, 0.35)
        silent_eye.exec_skill(silent_eye.asura_spirit_slash)


class Room7Handler(PiratesRoom7Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.SilentEye, DefaultBattleStrategy())


class Room8Handler(PiratesRoom8Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.SilentEye, DefaultBattleStrategy())


class Room9Handler(PiratesRoom9Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.SilentEye, DefaultBattleStrategy())


class Room10Handler(PiratesRoom10Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.SilentEye, DefaultBattleStrategy())


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
