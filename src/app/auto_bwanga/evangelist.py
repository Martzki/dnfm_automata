from src.app.auto_bwanga.room_handler import *
from src.lib.character.character import CharacterClass
from src.lib.character.evangelist import Evangelist
from src.lib.dungeon.dungeon import DungeonRoomHandler
from src.lib.dungeon.strategy import BattleStrategy

default_battle_strategy = BattleStrategy()
default_battle_strategy.register_skill(Evangelist.GrandCrashingCross, 10, 0)


class Room0Handler(BwangaRoom0Handler):
    def __init__(self, detector, last_frame, detect_room):
        super().__init__(CharacterClass.Evangelist, detector, last_frame, detect_room, default_battle_strategy)

    def pre_handler(self, enter_times, evangelist: Evangelist):
        if enter_times > 1:
            return

        evangelist.move(335, 0.4)
        evangelist.exec_skill(evangelist.grand_crashing_cross)

    def post_handler(self, enter_times, evangelist: Evangelist):
        if enter_times == 1:
            evangelist.wait_skill_cool_down(evangelist.saint_wall)
            evangelist.wait_skill_cool_down(evangelist.purifying_lightning)

        self.move_to_next_room(evangelist, enter_times)


class Room1Handler(BwangaRoom1Handler):
    def __init__(self, detector, last_frame, detect_room):
        super().__init__(CharacterClass.Evangelist, detector, last_frame, detect_room, default_battle_strategy)

    def pre_handler(self, enter_times, evangelist: Evangelist):
        if enter_times > 1:
            return

        evangelist.move(270, 0.5)
        evangelist.move(0, 0.07)
        evangelist.exec_skill(evangelist.saint_wall)
        evangelist.exec_skill(evangelist.christening_light)

    def post_handler(self, enter_times, evangelist: Evangelist):
        if enter_times == 1:
            evangelist.wait_skill_cool_down(evangelist.spear_of_victory)
            evangelist.wait_skill_cool_down(evangelist.purifying_lightning)

        self.move_to_next_room(evangelist, enter_times)


class Room2Handler(BwangaRoom2Handler):
    def __init__(self, detector, last_frame, detect_room):
        super().__init__(CharacterClass.Evangelist, detector, last_frame, detect_room, default_battle_strategy)

    def pre_handler(self, enter_times, evangelist: Evangelist):
        if enter_times > 1:
            return

        evangelist.move(280, 0.3)
        evangelist.exec_skill(evangelist.spear_of_victory, delay=0.1)
        evangelist.exec_skill(evangelist.purifying_lightning)

    def post_handler(self, enter_times, evangelist: Evangelist):
        if enter_times == 1:
            evangelist.wait_skill_cool_down(evangelist.valiant_aria)

        self.move_to_next_room(evangelist, enter_times)


class Room3Handler(BwangaRoom3Handler):
    def __init__(self, detector, last_frame, detect_room):
        super().__init__(CharacterClass.Evangelist, detector, last_frame, detect_room, default_battle_strategy)

    def pre_handler(self, enter_times, evangelist: Evangelist):
        if enter_times > 1:
            return

        evangelist.move(345, 0.6)
        evangelist.exec_skill(evangelist.valiant_aria)

    def post_handler(self, enter_times, evangelist: Evangelist):
        if enter_times == 1:
            evangelist.wait_skill_cool_down(evangelist.shining_cross)

        self.move_to_next_room(evangelist, enter_times)


class Room4Handler(BwangaRoom4Handler):
    def __init__(self, detector, last_frame, detect_room):
        super().__init__(CharacterClass.Evangelist, detector, last_frame, detect_room, default_battle_strategy)

    def pre_handler(self, enter_times, evangelist: Evangelist):
        if enter_times > 1:
            return

        evangelist.move(145, 0.4)
        evangelist.move(45, 0.4)
        evangelist.exec_skill(evangelist.shining_cross)

    def post_handler(self, enter_times, evangelist: Evangelist):
        if enter_times == 1:
            evangelist.wait_skill_cool_down(evangelist.crux_of_victoria)
        elif enter_times == 2:
            evangelist.wait_skill_cool_down(evangelist.saint_wall)
            evangelist.wait_skill_cool_down(evangelist.christening_light)

        self.move_to_next_room(evangelist, enter_times)


class Room5Handler(BwangaRoom5Handler):
    def __init__(self, detector, last_frame, detect_room):
        super().__init__(CharacterClass.Evangelist, detector, last_frame, detect_room, default_battle_strategy)

    def pre_handler(self, enter_times, evangelist: Evangelist):
        if enter_times == 1:
            evangelist.exec_skill(evangelist.crux_of_victoria)

    def post_handler(self, enter_times, evangelist: Evangelist):
        self.move_to_next_room(evangelist, enter_times)


class Room6Handler(BwangaRoom6Handler):
    def __init__(self, detector, last_frame, detect_room):
        super().__init__(CharacterClass.Evangelist, detector, last_frame, detect_room, default_battle_strategy)

    def pre_handler(self, enter_times, evangelist: Evangelist):
        if enter_times > 1:
            return

        evangelist.move(0, 0.5)
        evangelist.move(270, 0.2)
        evangelist.exec_skill(evangelist.saint_wall)
        evangelist.exec_skill(evangelist.christening_light)

    def post_handler(self, enter_times, evangelist: Evangelist):
        if enter_times == 1:
            evangelist.wait_skill_cool_down(evangelist.purifying_lightning)

        self.move_to_next_room(evangelist, enter_times)


class Room7Handler(BwangaRoom7Handler):
    def __init__(self, detector, last_frame, detect_room):
        super().__init__(CharacterClass.Evangelist, detector, last_frame, detect_room, default_battle_strategy)

    def pre_handler(self, enter_times, character: Evangelist):
        if enter_times > 1:
            return

        character.move(270, 0.15)
        character.move(0, 0.1)
        character.exec_skill(character.purifying_lightning)

    def post_handler(self, enter_times, evangelist: Evangelist):
        if enter_times == 1:
            evangelist.wait_skill_cool_down(evangelist.grand_crashing_cross)
            evangelist.wait_skill_cool_down(evangelist.shining_cross)

        self.move_to_next_room(evangelist, enter_times)


class Room8Handler(DungeonRoomHandler):
    def __init__(self, detector, last_frame, detect_room):
        super().__init__(8, CharacterClass.Evangelist, detector, last_frame, detect_room, default_battle_strategy)

    def pre_handler(self, enter_times, evangelist: Evangelist):
        if enter_times > 1:
            return

        evangelist.move(0, 0.5)
        evangelist.exec_skill(evangelist.grand_crashing_cross)
        evangelist.exec_skill(evangelist.shining_cross)

    def post_handler(self, enter_times, character: Evangelist):
        pass


# class Room9Handler(DungeonRoomHandler):
#     def __init__(self):
#         super().__init__(9, CharacterClass.Evangelist, default_battle_strategy)
#
#     def pre_handler(self, last_frame, evangelist: Evangelist):
#         evangelist.move(0, 10)
#         evangelist.exec_skill(evangelist.grand_crashing_cross)
#         evangelist.exec_skill(evangelist.shining_cross)
#
#     def post_handler(self, last_frame, character: Evangelist):
#         self.maintain_equipments()


def init_handlers(detector, last_frame, detect_room):
    return [
        Room0Handler(detector, last_frame, detect_room),
        Room1Handler(detector, last_frame, detect_room),
        Room2Handler(detector, last_frame, detect_room),
        Room3Handler(detector, last_frame, detect_room),
        Room4Handler(detector, last_frame, detect_room),
        Room5Handler(detector, last_frame, detect_room),
        Room6Handler(detector, last_frame, detect_room),
        Room7Handler(detector, last_frame, detect_room),
        Room8Handler(detector, last_frame, detect_room),
        # Room9Handler()
    ]
