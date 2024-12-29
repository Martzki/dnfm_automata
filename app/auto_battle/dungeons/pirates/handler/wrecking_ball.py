import time

from app.auto_battle.dungeons.pirates.handler.room_handler import *
from runtime.character.character_class import CharacterClass
from dungeon.strategy import BattleStrategy
from runtime.character.wrecking_ball import WreckingBall


class DefaultBattleStrategy(BattleStrategy):
    def __init__(self):
        super().__init__()
        self.register_skill(WreckingBall.Shotgun, 10, 0)


class Room0Handler(PiratesRoom0Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.WreckingBall, DefaultBattleStrategy())

    def pre_handler(self, enter_times, wrecking_ball: WreckingBall, **kwargs):
        if enter_times > 1:
            return

        wrecking_ball.exec_skill(wrecking_ball.fire_concentrate, delay=0.5)
        wrecking_ball.exec_skill(wrecking_ball.eagle_eye, delay=0.5)
        wrecking_ball.exec_skill(wrecking_ball.laser_rifle, duration=0.1)
        wrecking_ball.move(0, 1.5)


class Room1Handler(PiratesRoom1Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.WreckingBall, DefaultBattleStrategy())

    def pre_handler(self, enter_times, wrecking_ball: WreckingBall, **kwargs):
        if enter_times > 1:
            return

        wrecking_ball.exec_skill(wrecking_ball.fm_31_grenade_launcher)


class Room2Handler(PiratesRoom2Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.WreckingBall, DefaultBattleStrategy())

    def pre_handler(self, enter_times, wrecking_ball: WreckingBall, **kwargs):
        super().pre_handler(enter_times, wrecking_ball, **kwargs)

        if enter_times > 1:
            return

        wrecking_ball.move(0, 0.6)
        wrecking_ball.exec_skill(wrecking_ball.fm_92_stinger)
        wrecking_ball.move(270, 0.3)


class Room3Handler(PiratesRoom3Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.WreckingBall, DefaultBattleStrategy())

    def pre_handler(self, enter_times, wrecking_ball: WreckingBall, **kwargs):
        if enter_times > 1:
            return

        wrecking_ball.exec_skill(wrecking_ball.laser_rifle, duration=0.1)
        wrecking_ball.move(0, 1)


class Room4Handler(PiratesRoom4Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.WreckingBall, DefaultBattleStrategy())

    def pre_handler(self, enter_times, wrecking_ball: WreckingBall, **kwargs):
        if enter_times > 1:
            return

        wrecking_ball.move(0, 0.5)
        wrecking_ball.exec_skill(wrecking_ball.quantum_bomb, swipe_angle=0, delay=1.5)
        wrecking_ball.move(0, 0.3)


class Room5Handler(PiratesRoom5Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.WreckingBall, DefaultBattleStrategy())

    def pre_handler(self, enter_times, wrecking_ball: WreckingBall, **kwargs):
        super().pre_handler(enter_times, wrecking_ball, **kwargs)

        if enter_times > 1:
            return

        wrecking_ball.move(315, 0.25)
        wrecking_ball.move(0, 0.6)
        wrecking_ball.exec_skill(wrecking_ball.fm_31_grenade_launcher)
        wrecking_ball.move(270, 0.3)


class Room6Handler(PiratesRoom6Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.WreckingBall, DefaultBattleStrategy())

    def pre_handler(self, enter_times, wrecking_ball: WreckingBall, **kwargs):
        if enter_times > 1:
            return

        wrecking_ball.exec_skill(wrecking_ball.railgun)
        wrecking_ball.move(0, 1)


class Room7Handler(PiratesRoom7Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.WreckingBall, DefaultBattleStrategy())


class Room8Handler(PiratesRoom8Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.WreckingBall, DefaultBattleStrategy())


class Room9Handler(PiratesRoom9Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.WreckingBall, DefaultBattleStrategy())


class Room10Handler(PiratesRoom10Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.WreckingBall, DefaultBattleStrategy())


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
