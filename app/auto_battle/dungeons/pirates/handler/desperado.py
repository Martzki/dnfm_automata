from app.auto_battle.dungeons.pirates.handler.room_handler import *
from dungeon.strategy import BattleStrategy
from runtime.character.character_class import CharacterClass
from runtime.character.desperado import Desperado


class DefaultBattleStrategy(BattleStrategy):
    def __init__(self):
        super().__init__()
        self.register_skill(Desperado.Windmill, 10, 0)


class Room0Handler(PiratesRoom0Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Desperado, DefaultBattleStrategy())

    def pre_handler(self, enter_times, desperado: Desperado, **kwargs):
        if enter_times > 1:
            return

        desperado.exec_skill(desperado.silver_bullet, delay=0.5)
        desperado.exec_skill(desperado.death_by_revolver, delay=0.5)
        desperado.move(0, 0.6)
        desperado.move(180, 0.15)
        desperado.exec_skill(desperado.western_fire)


class Room1Handler(PiratesRoom1Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Desperado, DefaultBattleStrategy())

    def pre_handler(self, enter_times, desperado: Desperado, **kwargs):
        if enter_times > 1:
            return

        desperado.move(0, 0.5)
        desperado.exec_skill(desperado.headshot)


class Room2Handler(PiratesRoom2Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Desperado, DefaultBattleStrategy())

    def pre_handler(self, enter_times, desperado: Desperado, **kwargs):
        super().pre_handler(enter_times, desperado, **kwargs)

        if enter_times > 1:
            return

        desperado.move(0, 0.6)
        desperado.move(180, 0.15)
        desperado.exec_skill(desperado.western_fire)


class Room3Handler(PiratesRoom3Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Desperado, DefaultBattleStrategy())

    def pre_handler(self, enter_times, desperado: Desperado, **kwargs):
        if enter_times > 1:
            return

        desperado.move(0, 0.75)
        desperado.exec_skill(desperado.headshot)


class Room4Handler(PiratesRoom4Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Desperado, DefaultBattleStrategy())

    def pre_handler(self, enter_times, desperado: Desperado, **kwargs):
        if enter_times > 1:
            return

        desperado.move(0, 0.4)
        desperado.exec_skill(desperado.death_hawk)
        desperado.exec_skill(desperado.attack, duration=2)


class Room5Handler(PiratesRoom5Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Desperado, DefaultBattleStrategy())

    def pre_handler(self, enter_times, desperado: Desperado, **kwargs):
        super().pre_handler(enter_times, desperado, **kwargs)

        if enter_times > 1:
            return

        desperado.move(315, 0.5)
        desperado.exec_skill(desperado.headshot)


class Room6Handler(PiratesRoom6Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Desperado, DefaultBattleStrategy())

    def pre_handler(self, enter_times, desperado: Desperado, **kwargs):
        if enter_times > 1:
            return

        desperado.move(0, 1)
        desperado.exec_skill(desperado.deadly_approach)


class Room7Handler(PiratesRoom7Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Desperado, DefaultBattleStrategy())


class Room8Handler(PiratesRoom8Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Desperado, DefaultBattleStrategy())


class Room9Handler(PiratesRoom9Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Desperado, DefaultBattleStrategy())


class Room10Handler(PiratesRoom10Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Desperado, DefaultBattleStrategy())


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
