import time

from src.app.auto_bwanga.room_handler import *
from src.lib.character.character import CharacterClass
from src.lib.character.wrecking_ball import WreckingBall
from src.lib.dungeon.strategy import BattleStrategy


class DefaultBattleStrategy(BattleStrategy):
    def __init__(self):
        super().__init__()
        self.register_skill(WreckingBall.Shotgun, 10, 0)
        self.register_skill(WreckingBall.SteyrAMR, 20, 0)


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

        self.move_to_next_room(wrecking_ball, enter_times)


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

        self.move_to_next_room(wrecking_ball, enter_times)


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

        self.move_to_next_room(wrecking_ball, enter_times)


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

        self.move_to_next_room(wrecking_ball, enter_times)


class Room4Handler(BwangaRoom4Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.WreckingBall, DefaultBattleStrategy())

    def pre_handler(self, enter_times, wrecking_ball: WreckingBall, **kwargs):
        if enter_times > 1:
            return

        wrecking_ball.move(155, 0.6)
        wrecking_ball.move(180, 0.35)
        time.sleep(0.1)
        wrecking_ball.move(0, 0.2)
        wrecking_ball.exec_skill(wrecking_ball.fm_92_stinger)

    def post_handler(self, enter_times, wrecking_ball: WreckingBall, **kwargs):
        room_5_visited = kwargs.get("room_5_visited", False)
        if not room_5_visited:
            wrecking_ball.wait_skill_cool_down(wrecking_ball.quantum_bomb)
            wrecking_ball.wait_skill_cool_down(wrecking_ball.x_1_extruder)
        else:
            wrecking_ball.wait_skill_cool_down(wrecking_ball.laser_rifle)

        self.move_to_next_room(wrecking_ball, enter_times, room_5_visited)


class Room5Handler(BwangaRoom5Handler):
    def __init__(self, dungeon):
        strategy = DefaultBattleStrategy()
        strategy.register_skill(WreckingBall.SatelliteBeam, 0)
        super().__init__(dungeon, CharacterClass.WreckingBall, strategy)

    def pre_handler(self, enter_times, wrecking_ball: WreckingBall, **kwargs):
        if enter_times > 1:
            return

        wrecking_ball.exec_skill(wrecking_ball.quantum_bomb, swipe_angle=225, delay=0.5)
        wrecking_ball.exec_skill(wrecking_ball.x_1_extruder, duration=1.5, delay=1.5)
        wrecking_ball.move(180, 0.5)

    def post_handler(self, enter_times, wrecking_ball: WreckingBall, **kwargs):
        self.move_to_next_room(wrecking_ball, enter_times)


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

        self.move_to_next_room(wrecking_ball, enter_times)


class Room7Handler(BwangaRoom7Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.WreckingBall, DefaultBattleStrategy())

    def pre_handler(self, enter_times, wrecking_ball: WreckingBall, **kwargs):
        if enter_times > 1:
            return

        time.sleep(0.8)
        wrecking_ball.exec_skill(wrecking_ball.fm_31_grenade_launcher, delay=0.8)
        wrecking_ball.exec_skill(wrecking_ball.steyr_amr)

    def post_handler(self, enter_times, wrecking_ball: WreckingBall, **kwargs):
        if enter_times == 1:
            wrecking_ball.wait_skill_cool_down(wrecking_ball.destroyer_90_bunker_bomb)
            wrecking_ball.wait_skill_cool_down(wrecking_ball.fm_92_stinger)

        self.move_to_next_room(wrecking_ball, enter_times)


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

    def pre_handler(self, enter_times, wrecking_ball: WreckingBall, **kwargs):
        pass

    def post_handler(self, enter_times, wrecking_ball: WreckingBall, **kwargs):
        self.move_to_next_room(wrecking_ball, enter_times)


class Room10Handler(BwangaRoom10Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.WreckingBall, DefaultBattleStrategy())

    def pre_handler(self, enter_times, wrecking_ball: WreckingBall, **kwargs):
        pass

    def post_handler(self, enter_times, wrecking_ball: WreckingBall, **kwargs):
        self.move_to_next_room(wrecking_ball, enter_times)


class Room11Handler(BwangaRoom11Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.WreckingBall, DefaultBattleStrategy())

    def pre_handler(self, enter_times, wrecking_ball: WreckingBall, **kwargs):
        pass

    def post_handler(self, enter_times, wrecking_ball: WreckingBall, **kwargs):
        self.move_to_next_room(wrecking_ball, enter_times)


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
