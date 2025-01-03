import time

from app.auto_battle.dungeons.bwanga.handler.room_handler import *
from dungeon.strategy import BattleStrategy
from runtime.character.character_class import CharacterClass
from runtime.character.wrecking_ball import WreckingBall


class DefaultBattleStrategy(BattleStrategy):
    def __init__(self):
        super().__init__()
        self.register_skill(WreckingBall.Shotgun, 10, 0)
        self.register_skill(WreckingBall.SteyrAmr, 20, 0)


class Room0Handler(BwangaRoom0Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.WreckingBall, DefaultBattleStrategy())

    def pre_handler(self, enter_times, wrecking_ball: WreckingBall, **kwargs):
        if enter_times > 1:
            return

        wrecking_ball.exec_skill(wrecking_ball.eagle_eye, delay=0.3)
        wrecking_ball.exec_skill(wrecking_ball.fire_concentrate)
        wrecking_ball.move(335, 0.45)
        time.sleep(0.35)
        wrecking_ball.exec_skill(wrecking_ball.laser_rifle, 0.1)

    def post_handler(self, enter_times, wrecking_ball: WreckingBall, **kwargs):
        if enter_times == 1:
            wrecking_ball.wait_skill_cool_down(wrecking_ball.destroyer_90_bunker_bomb)

        super().post_handler(enter_times, wrecking_ball, **kwargs)


class Room1Handler(BwangaRoom1Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.WreckingBall, DefaultBattleStrategy())

    def pre_handler(self, enter_times, wrecking_ball: WreckingBall, **kwargs):
        if enter_times > 1:
            return

        wrecking_ball.move(250, 0.5)
        wrecking_ball.move(0, 0.07)
        wrecking_ball.exec_skill(wrecking_ball.destroyer_90_bunker_bomb)

    def post_handler(self, enter_times, wrecking_ball: WreckingBall, **kwargs):
        if enter_times == 1:
            wrecking_ball.wait_skill_cool_down(wrecking_ball.fm_31_grenade_launcher)

        super().post_handler(enter_times, wrecking_ball, **kwargs)


class Room2Handler(BwangaRoom2Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.WreckingBall, DefaultBattleStrategy())

    def pre_handler(self, enter_times, wrecking_ball: WreckingBall, **kwargs):
        if enter_times > 1:
            return

        time.sleep(0.5)
        wrecking_ball.exec_skill(wrecking_ball.fm_31_grenade_launcher)

    def post_handler(self, enter_times, wrecking_ball: WreckingBall, **kwargs):
        if enter_times == 1:
            wrecking_ball.wait_skill_cool_down(wrecking_ball.laser_rifle)

        super().post_handler(enter_times, wrecking_ball, **kwargs)


class Room3Handler(BwangaRoom3Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.WreckingBall, DefaultBattleStrategy())

    def pre_handler(self, enter_times, wrecking_ball: WreckingBall, **kwargs):
        if enter_times > 1:
            return

        wrecking_ball.move(270, 0.25)
        wrecking_ball.exec_skill(wrecking_ball.laser_rifle, duration=0.1, delay=0.3)
        wrecking_ball.move(75, 0.2)
        wrecking_ball.exec_skill(wrecking_ball.shotgun)

    def post_handler(self, enter_times, wrecking_ball: WreckingBall, **kwargs):
        if enter_times == 1:
            wrecking_ball.wait_skill_cool_down(wrecking_ball.fm_92_stinger)

        super().post_handler(enter_times, wrecking_ball, **kwargs)


class Room4Handler(BwangaRoom4Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.WreckingBall, DefaultBattleStrategy())

    def pre_handler(self, enter_times, wrecking_ball: WreckingBall, **kwargs):
        super().pre_handler(enter_times, wrecking_ball, **kwargs)

        if enter_times > 1:
            return

        wrecking_ball.move(155, 0.6)
        wrecking_ball.move(180, 0.35)
        time.sleep(0.1)
        wrecking_ball.move(0, 0.2)
        wrecking_ball.exec_skill(wrecking_ball.fm_92_stinger)

    def post_handler(self, enter_times, wrecking_ball: WreckingBall, **kwargs):
        room_5_visited = 5 in kwargs.get('visited_room_list', [])
        if not room_5_visited:
            wrecking_ball.wait_skill_cool_down(wrecking_ball.quantum_bomb)
            wrecking_ball.wait_skill_cool_down(wrecking_ball.x_1_extruder)
        else:
            wrecking_ball.wait_skill_cool_down(wrecking_ball.laser_rifle)

        super().post_handler(enter_times, wrecking_ball, **kwargs)


class Room5Handler(BwangaRoom5Handler):
    def __init__(self, dungeon):
        strategy = DefaultBattleStrategy()
        strategy.register_skill(WreckingBall.SatelliteBeam, 0)
        super().__init__(dungeon, CharacterClass.WreckingBall, strategy)

    def pre_handler(self, enter_times, wrecking_ball: WreckingBall, **kwargs):
        if enter_times > 1:
            return

        wrecking_ball.exec_skill(wrecking_ball.quantum_bomb, swipe_angle=225, delay=0.5)
        wrecking_ball.exec_skill(wrecking_ball.x_1_extruder, duration=1.5, delay=2)

        super().pre_handler(enter_times, wrecking_ball, **kwargs)


class Room6Handler(BwangaRoom6Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.WreckingBall, DefaultBattleStrategy())

    def pre_handler(self, enter_times, wrecking_ball: WreckingBall, **kwargs):
        if enter_times > 1:
            return

        wrecking_ball.move(270, 0.4)
        wrecking_ball.exec_skill(wrecking_ball.laser_rifle)

    def post_handler(self, enter_times, wrecking_ball: WreckingBall, **kwargs):
        if enter_times == 1:
            wrecking_ball.wait_skill_cool_down(wrecking_ball.fm_31_grenade_launcher)

        super().post_handler(enter_times, wrecking_ball, **kwargs)


class Room7Handler(BwangaRoom7Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.WreckingBall, DefaultBattleStrategy())

    def pre_handler(self, enter_times, wrecking_ball: WreckingBall, **kwargs):
        super().pre_handler(enter_times, wrecking_ball, **kwargs)
        if enter_times > 1:
            return

        time.sleep(0.8)
        wrecking_ball.exec_skill(wrecking_ball.fm_31_grenade_launcher, delay=0.8)
        wrecking_ball.exec_skill(wrecking_ball.steyr_amr)

    def post_handler(self, enter_times, wrecking_ball: WreckingBall, **kwargs):
        if enter_times == 1:
            wrecking_ball.wait_skill_cool_down(wrecking_ball.destroyer_90_bunker_bomb)
            wrecking_ball.wait_skill_cool_down(wrecking_ball.fm_92_stinger)

        super().post_handler(enter_times, wrecking_ball, **kwargs)


class Room8Handler(BwangaRoom8Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.WreckingBall, DefaultBattleStrategy())

    def pre_handler(self, enter_times, wrecking_ball: WreckingBall, **kwargs):
        if enter_times > 1:
            return

        wrecking_ball.move(0, 0.5)
        wrecking_ball.exec_skill(wrecking_ball.destroyer_90_bunker_bomb, delay=0.5)
        wrecking_ball.exec_skill(wrecking_ball.fm_92_stinger)


class Room9Handler(BwangaRoom9Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.WreckingBall, DefaultBattleStrategy())


class Room10Handler(BwangaRoom10Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.WreckingBall, DefaultBattleStrategy())


class Room11Handler(BwangaRoom11Handler):
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
        Room11Handler(dungeon),
    ]
