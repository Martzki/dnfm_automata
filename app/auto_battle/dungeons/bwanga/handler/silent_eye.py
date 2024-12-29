import time

from app.auto_battle.dungeons.bwanga.handler.room_handler import *
from dungeon.strategy import BattleStrategy
from runtime.character.character_class import CharacterClass
from runtime.character.silent_eye import SilentEye


class DefaultBattleStrategy(BattleStrategy):
    def __init__(self):
        super().__init__()
        self.register_skill(SilentEye.WaveRadiation, 10, 0)


class Room0Handler(BwangaRoom0Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.SilentEye, DefaultBattleStrategy())

    def pre_handler(self, enter_times, silent_eye: SilentEye, **kwargs):
        if enter_times > 1:
            return

        silent_eye.exec_skill(silent_eye.murderous_wave)
        silent_eye.move(335, 0.45)
        silent_eye.exec_skill(silent_eye.ice_wave_sword)

    def post_handler(self, enter_times, silent_eye: SilentEye, **kwargs):
        if enter_times == 1:
            silent_eye.wait_skill_cool_down(silent_eye.ground_quaker)

        super().post_handler(enter_times, silent_eye, **kwargs)


class Room1Handler(BwangaRoom1Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.SilentEye, DefaultBattleStrategy())

    def pre_handler(self, enter_times, silent_eye: SilentEye, **kwargs):
        if enter_times > 1:
            return

        silent_eye.move(270, 0.5)
        silent_eye.move(0, 0.07)
        silent_eye.exec_skill(silent_eye.ground_quaker)
        silent_eye.exec_skill(silent_eye.attack, 2.5)

    def post_handler(self, enter_times, silent_eye: SilentEye, **kwargs):
        if enter_times == 1:
            silent_eye.wait_skill_cool_down(silent_eye.spirit_crescent)

        super().post_handler(enter_times, silent_eye, **kwargs)


class Room2Handler(BwangaRoom2Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.SilentEye, DefaultBattleStrategy())

    def pre_handler(self, enter_times, silent_eye: SilentEye, **kwargs):
        if enter_times > 1:
            return

        silent_eye.move(280, 0.4)
        silent_eye.exec_skill(silent_eye.spirit_crescent)
        silent_eye.exec_skill(silent_eye.ice_wave_sword)

    def post_handler(self, enter_times, silent_eye: SilentEye, **kwargs):
        if enter_times == 1:
            silent_eye.wait_skill_cool_down(silent_eye.deadly_enticer)

        super().post_handler(enter_times, silent_eye, **kwargs)


class Room3Handler(BwangaRoom3Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.SilentEye, DefaultBattleStrategy())

    def pre_handler(self, enter_times, silent_eye: SilentEye, **kwargs):
        if enter_times > 1:
            return

        silent_eye.move(345, 0.6)
        silent_eye.exec_skill(silent_eye.deadly_enticer, delay=1)
        silent_eye.exec_skill(silent_eye.deadly_enticer)

    def post_handler(self, enter_times, silent_eye: SilentEye, **kwargs):
        if enter_times == 1:
            silent_eye.wait_skill_cool_down(silent_eye.wave_eye)

        super().post_handler(enter_times, silent_eye, **kwargs)


class Room4Handler(BwangaRoom4Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.SilentEye, DefaultBattleStrategy())

    def pre_handler(self, enter_times, silent_eye: SilentEye, **kwargs):
        super().pre_handler(enter_times, silent_eye, **kwargs)

        if enter_times > 1:
            return

        silent_eye.move(145, 0.85)
        silent_eye.move(180, 0.4)
        time.sleep(0.1)
        silent_eye.move(0, 0.15)
        silent_eye.exec_skill(silent_eye.fire_wave_sword, delay=0.25)
        silent_eye.exec_skill(silent_eye.spirit_crescent)
        silent_eye.exec_skill(silent_eye.wave_radiation)

    def post_handler(self, enter_times, silent_eye: SilentEye, **kwargs):
        room_5_visited = 5 in kwargs.get('visited_room_list', [])
        if not room_5_visited:
            silent_eye.wait_skill_cool_down(silent_eye.wave_radiation)
            silent_eye.wait_skill_cool_down(silent_eye.agni_pentacle)
            silent_eye.exec_skill(silent_eye.wave_eye)
        else:
            silent_eye.wait_skill_cool_down(silent_eye.ground_quaker)

        super().post_handler(enter_times, silent_eye, **kwargs)


class Room5Handler(BwangaRoom5Handler):
    def __init__(self, dungeon):
        strategy = DefaultBattleStrategy()
        strategy.register_skill(SilentEye.AgniPentacle, 15, 0)
        super().__init__(dungeon, CharacterClass.SilentEye, strategy)

    def pre_handler(self, enter_times, silent_eye: SilentEye, **kwargs):
        if enter_times > 1:
            return

        silent_eye.move(220, 0.9)
        silent_eye.move(180, 0.15)
        silent_eye.exec_skill(silent_eye.attack, duration=0.5)
        silent_eye.exec_skill(silent_eye.wave_radiation)
        silent_eye.move(15, 0.8)
        silent_eye.exec_skill(silent_eye.agni_pentacle)

        super().pre_handler(enter_times, silent_eye, **kwargs)


class Room6Handler(BwangaRoom6Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.SilentEye, DefaultBattleStrategy())

    def pre_handler(self, enter_times, silent_eye: SilentEye, **kwargs):
        if enter_times > 1:
            return

        silent_eye.move(300, 0.4)
        silent_eye.move(0, 0.25)
        silent_eye.exec_skill(silent_eye.ground_quaker)
        silent_eye.exec_skill(silent_eye.attack, 3)

    def post_handler(self, enter_times, silent_eye: SilentEye, **kwargs):
        if enter_times == 1:
            silent_eye.wait_skill_cool_down(silent_eye.deadly_enticer)

        super().post_handler(enter_times, silent_eye, **kwargs)


class Room7Handler(BwangaRoom7Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.SilentEye, DefaultBattleStrategy())

    def pre_handler(self, enter_times, character: SilentEye, **kwargs):
        super().pre_handler(enter_times, character, **kwargs)
        if enter_times > 1:
            return

        character.move(345, 0.65)
        character.exec_skill(character.deadly_enticer, delay=0.25)
        character.exec_skill(character.deadly_enticer)

    def post_handler(self, enter_times, silent_eye: SilentEye, **kwargs):
        if enter_times == 1:
            silent_eye.wait_skill_cool_down(silent_eye.ice_wave_sword)
            silent_eye.wait_skill_cool_down(silent_eye.fire_wave_sword)
            silent_eye.wait_skill_cool_down(silent_eye.ghost_orb)

        super().post_handler(enter_times, silent_eye, **kwargs)


class Room8Handler(BwangaRoom8Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.SilentEye, DefaultBattleStrategy())

    def pre_handler(self, enter_times, silent_eye: SilentEye, **kwargs):
        if enter_times > 1:
            return

        silent_eye.move(0, 0.7)
        silent_eye.exec_skill(silent_eye.ice_wave_sword)
        silent_eye.exec_skill(silent_eye.fire_wave_sword)
        silent_eye.exec_skill(silent_eye.ghost_orb)
        silent_eye.move(0, 1)
        silent_eye.exec_skill(silent_eye.wave_radiation)


class Room9Handler(BwangaRoom9Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.SilentEye, DefaultBattleStrategy())


class Room10Handler(BwangaRoom10Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.SilentEye, DefaultBattleStrategy())


class Room11Handler(BwangaRoom11Handler):
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
        Room11Handler(dungeon),
    ]
