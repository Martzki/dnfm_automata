from app.auto_battle.dungeons.pirates.handler.room_handler import *
from dungeon.strategy import BattleStrategy
from runtime.character.character_class import CharacterClass
from runtime.character.evangelist import Evangelist


class DefaultBattleStrategy(BattleStrategy):
    def __init__(self):
        super().__init__()
        self.register_skill(Evangelist.PureLight, 10, 0)


class Room0Handler(PiratesRoom0Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Evangelist, DefaultBattleStrategy())

    def pre_handler(self, enter_times, evangelist: Evangelist, **kwargs):
        if enter_times > 1:
            return

        evangelist.move(0, 0.5)
        evangelist.exec_skill(evangelist.christening_light)
        evangelist.move(0, 0.5)


class Room1Handler(PiratesRoom1Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Evangelist, DefaultBattleStrategy())

    def pre_handler(self, enter_times, evangelist: Evangelist, **kwargs):
        if enter_times > 1:
            return

        evangelist.move(0, 0.5)
        evangelist.exec_skill(evangelist.saint_wall)


class Room2Handler(PiratesRoom2Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Evangelist, DefaultBattleStrategy())

    def pre_handler(self, enter_times, evangelist: Evangelist, **kwargs):
        super().pre_handler(enter_times, evangelist, **kwargs)

        if enter_times > 1:
            return

        evangelist.move(0, 0.5)
        evangelist.exec_skill(evangelist.purifying_lightning, delay=1)
        evangelist.move(340, 0.5)


class Room3Handler(PiratesRoom3Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Evangelist, DefaultBattleStrategy())

    def pre_handler(self, enter_times, evangelist: Evangelist, **kwargs):
        if enter_times > 1:
            return

        evangelist.move(0, 1.25)
        evangelist.exec_skill(evangelist.shining_cross)


class Room4Handler(PiratesRoom4Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Evangelist, DefaultBattleStrategy())

    def pre_handler(self, enter_times, evangelist: Evangelist, **kwargs):
        if enter_times > 1:
            return

        evangelist.exec_skill(evangelist.holy_circlet)
        evangelist.move(0, 1)


class Room5Handler(PiratesRoom5Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Evangelist, DefaultBattleStrategy())

    def pre_handler(self, enter_times, evangelist: Evangelist, **kwargs):
        super().pre_handler(enter_times, evangelist, **kwargs)

        if enter_times > 1:
            return

        evangelist.move(315, 0.25)
        evangelist.move(0, 0.6)
        evangelist.exec_skill(evangelist.repentant_smash)


class Room6Handler(PiratesRoom6Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Evangelist, DefaultBattleStrategy())

    def pre_handler(self, enter_times, evangelist: Evangelist, **kwargs):
        if enter_times > 1:
            return

        evangelist.move(0, 0.3)
        evangelist.exec_skill(evangelist.grand_crashing_cross)


class Room7Handler(PiratesRoom7Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Evangelist, DefaultBattleStrategy())


class Room8Handler(PiratesRoom8Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Evangelist, DefaultBattleStrategy())


class Room9Handler(PiratesRoom9Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Evangelist, DefaultBattleStrategy())


class Room10Handler(PiratesRoom10Handler):
    def __init__(self, dungeon):
        super().__init__(dungeon, CharacterClass.Evangelist, DefaultBattleStrategy())


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
