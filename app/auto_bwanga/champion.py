import time

from app.auto_bwanga.room_handler import *
from character.character import CharacterClass
from character.champion import Champion
from dungeon.strategy import BattleStrategy


class DefaultBattleStrategy(BattleStrategy):
    def __init__(self):
        super().__init__()
        self.register_skill(Champion.BoneCrusher, 10, 0)


class Room0Handler(BwangaRoom0Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Champion, DefaultBattleStrategy())

    def pre_handler(self, enter_times, champion: Champion, **kwargs):
        if enter_times > 1:
            return

        champion.exec_skill(champion.power_fist)
        champion.move(335, 0.45)
        time.sleep(0.1)
        champion.move(0, 0.5)
        champion.exec_skill(champion.seismic_crash)

    def post_handler(self, enter_times, champion: Champion, **kwargs):
        if enter_times == 1:
            champion.wait_skill_cool_down(champion.continuous_strike)

        super().post_handler(enter_times, champion, **kwargs)


class Room1Handler(BwangaRoom1Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Champion, DefaultBattleStrategy())

    def pre_handler(self, enter_times, champion: Champion, **kwargs):
        if enter_times > 1:
            return

        champion.move(270, 0.5)
        champion.move(0, 0.07)
        champion.exec_skill(champion.continuous_strike, delay=0.2)
        champion.exec_skill(champion.continuous_strike, delay=0.2)
        champion.exec_skill(champion.continuous_strike, delay=0.2)
        champion.exec_skill(champion.continuous_strike, delay=0.2)

    def post_handler(self, enter_times, champion: Champion, **kwargs):
        if enter_times == 1:
            champion.wait_skill_cool_down(champion.seismic_crash)

        super().post_handler(enter_times, champion, **kwargs)


class Room2Handler(BwangaRoom2Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Champion, DefaultBattleStrategy())

    def pre_handler(self, enter_times, champion: Champion, **kwargs):
        if enter_times > 1:
            return

        champion.move(340, 0.6)
        champion.move(0, 0.1)
        time.sleep(0.25)
        champion.exec_skill(champion.seismic_crash)

    def post_handler(self, enter_times, champion: Champion, **kwargs):
        if enter_times == 1:
            champion.wait_skill_cool_down(champion.lightning_dance)

        super().post_handler(enter_times, champion, **kwargs)


class Room3Handler(BwangaRoom3Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Champion, DefaultBattleStrategy())

    def pre_handler(self, enter_times, champion: Champion, **kwargs):
        if enter_times > 1:
            return

        champion.move(0, 0.2)
        champion.exec_skill(champion.lightning_dance, delay=2)

    def post_handler(self, enter_times, champion: Champion, **kwargs):
        if enter_times == 1:
            champion.wait_skill_cool_down(champion.seismic_crash)
            champion.wait_skill_cool_down(champion.mountain_pusher)

        super().post_handler(enter_times, champion, **kwargs)


class Room4Handler(BwangaRoom4Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Champion, DefaultBattleStrategy())

    def pre_handler(self, enter_times, champion: Champion, **kwargs):
        super().pre_handler(enter_times, champion, **kwargs)

        if enter_times > 1:
            return

        champion.move(45, 0.6)
        champion.move(180, 0.15)
        champion.exec_skill(champion.seismic_crash, delay=0.2)
        champion.move(180, 0.1)
        champion.exec_skill(champion.attack, duration=1)
        champion.move(180, 0.7)
        champion.exec_skill(champion.mountain_pusher, delay=0.15)
        champion.exec_skill(champion.attack, duration=1)

    def post_handler(self, enter_times, champion: Champion, **kwargs):
        room_5_visited = kwargs.get("room_5_visited", False)
        if not room_5_visited:
            champion.wait_skill_cool_down(champion.beat_drive)
            champion.wait_skill_cool_down(champion.kihop_low_kick)
        else:
            champion.wait_skill_cool_down(champion.seismic_crash)

        super().post_handler(enter_times, champion, **kwargs)


class Room5Handler(BwangaRoom5Handler):
    def __init__(self, dungeon):
        strategy = DefaultBattleStrategy()
        strategy.register_skill(Champion.SeismicCrash, 10, 0)
        strategy.register_skill(Champion.BoneCrusher, 20, 0)
        super().__init__(dungeon, CharacterClass.Champion, strategy)

    def pre_handler(self, enter_times, champion: Champion, **kwargs):
        if enter_times > 1:
            return

        champion.exec_skill(champion.super_armor, delay=0.3)
        champion.move(280, 1.8)
        champion.move(180, 0.1)
        champion.exec_skill(champion.beat_drive, delay=0.15)
        champion.move(90, 0.25)
        time.sleep(2.5)
        champion.exec_skill(champion.continuous_strike, delay=0.2)
        champion.exec_skill(champion.continuous_strike, delay=0.2)
        champion.exec_skill(champion.continuous_strike, delay=0.2)
        champion.exec_skill(champion.continuous_strike, delay=0.2)

        super().pre_handler(enter_times, champion, **kwargs)


class Room6Handler(BwangaRoom6Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Champion, DefaultBattleStrategy())

    def pre_handler(self, enter_times, champion: Champion, **kwargs):
        if enter_times > 1:
            return

        champion.move(315, 0.35)
        champion.move(0, 0.6)
        champion.exec_skill(champion.seismic_crash, delay=0.35)
        champion.move(180, 0.15)
        champion.exec_skill(champion.attack, duration=1.5)

    def post_handler(self, enter_times, champion: Champion, **kwargs):
        if enter_times == 1:
            champion.wait_skill_cool_down(champion.lightning_dance)

        super().post_handler(enter_times, champion, **kwargs)


class Room7Handler(BwangaRoom7Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Champion, DefaultBattleStrategy())

    def pre_handler(self, enter_times, character: Champion, **kwargs):
        if enter_times > 1:
            return

        character.move(0, 0.5)
        character.exec_skill(character.lightning_dance, delay=2)

    def post_handler(self, enter_times, champion: Champion, **kwargs):
        if enter_times == 1:
            champion.wait_skill_cool_down(champion.rising_fist)

        super().post_handler(enter_times, champion, **kwargs)


class Room8Handler(BwangaRoom8Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Champion, DefaultBattleStrategy())

    def pre_handler(self, enter_times, champion: Champion, **kwargs):
        if enter_times > 1:
            return

        champion.move(0, 0.7)
        champion.exec_skill(champion.rising_fist, delay=1)
        champion.exec_skill(champion.mountain_pusher)


class Room9Handler(BwangaRoom9Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Champion, DefaultBattleStrategy())


class Room10Handler(BwangaRoom10Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Champion, DefaultBattleStrategy())


class Room11Handler(BwangaRoom11Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Champion, DefaultBattleStrategy())


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
