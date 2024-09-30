import time

import cv2

from src.common.log import Logger
from src.lib.character.character import Character
from src.lib.dungeon.battle import BattleMetadata
from src.lib.dungeon.strategy import BattleStrategy

LOGGER = Logger(__name__).logger


class DungeonRoomHandler(object):
    def __init__(self, room_id, character_class, detector, last_frame, detect_room, strategy=None):
        self.room_id = room_id
        self.character_class = character_class
        self.detector = detector
        self.detect_room = detect_room
        self.last_frame = last_frame
        self.finish_img = cv2.imread('res/scenario/base/dungeon_finish.png')
        self.in_dungeon_img = cv2.imread('res/scenario/base/in_dungeon_2.png')
        self.re_enter_img = cv2.imread('res/scenario/base/re_enter.png')
        self.search_angle = (20, 270, 160, 270)
        self.search_times = 0
        self.last_search_time = time.time()
        self.last_exec_skill_time = time.time()
        self.battle_strategy = strategy if strategy else BattleStrategy()

    def room_changed(self, frame=None):
        frame = self.last_frame() if frame is None else frame
        room = self.detect_room(frame)
        if not room:
            LOGGER.warning(f"Room is not detected.")
            return True

        if room.room_id == self.room_id:
            return False

        LOGGER.info(f"Room changed from {self.room_id} to {room.room_id}")

        return True

    def re_search_dungeon(self, character):
        if time.time() - self.last_search_time > 3:
            self.search_times = 0

        angle = self.search_angle[self.search_times % 4]
        character.move(angle, 0.4 + 0.4 * (self.search_times // 4))
        self.search_times += 1
        self.last_search_time = time.time()


    def move_toward_monster(self, character, skill, meta):
        """
        Try to move toward the closest monster.
        :param character: character under control
        :param skill: skill to execute
        :param meta: DungeonMetadata
        :return: True if monster is too far away from character else False
        """
        if meta.character is None:
            LOGGER.info(f"Character not found")
            return False

        monster, distance = meta.get_closest_monster(skill.exec_limit.vertical_only)

        LOGGER.info(f"Change direction")
        character.move_with_rad(BattleMetadata.get_rad(meta.character.coordinate(), monster.coordinate()), 0.15)

        move_threshold = 0.3
        if skill.exec_limit.min_distance < distance:
            duration = BattleMetadata.get_move_duration(distance)
            move_duration = move_threshold if duration > move_threshold else duration
            LOGGER.info(f"Move toward monster with {move_duration}")
            character.move_with_rad(BattleMetadata.get_rad(meta.character.coordinate(), monster.coordinate()),
                                    move_duration)
            return duration > move_threshold
        else:
            vertical_diff = meta.character.coordinate()[1] - monster.coordinate()[1]
            if abs(vertical_diff) > 100:
                character.move(90 if vertical_diff > 0 else 270, 0.2)



        return False

    def battle(self, character, meta):
        now = time.time()
        if now - self.last_exec_skill_time > 3:
            skill = self.battle_strategy.get_next_skill(character)
            skill = skill if skill else character.attack
        else:
            skill = character.attack

        # Need move closer.
        if self.move_toward_monster(character, skill, meta):
            return

        LOGGER.info(f"Exec skill {skill}")
        character.exec_skill(skill)

        time.sleep(0.15)

        if skill != character.attack:
            self.last_exec_skill_time = now

    def pick_items(self, character, meta):
        """
        Pick found items.
        :param character: character
        :param meta: battle metadata
        :return: Need re
        """
        item, distance = meta.get_closest_item()
        if item is None:
            LOGGER.info("Failed to found closest item")
            return True

        if meta.character:
            LOGGER.info(f"Move toward item from {meta.character.coordinate()} to {item.coordinate()}")
            character.move_toward(meta.character.coordinate(), item.coordinate(), self.room_changed)
        else:
            self.re_search_dungeon(character)

    def maintain_equipments(self):
        pass

    def dungeon_is_finished(self, frame):
        result = self.detector.img_match(frame, [self.finish_img])
        return result.confidence > 0.9

    def pre_handler(self, enter_times, character: Character, **kwargs):
        """
        Do something before auto battle.
        e.g. Move to somewhere and execute some skill.
        :param enter_times: the time entering this room
        :param character: character under control
        :return: None
        """
        pass

    def handler(self, enter_times, character, **kwargs):
        """
        Kill all monsters and pick all items in this dungeon.
        :param character: character under control
        :param enter_times: the times entering this room
        :return: room changed or not
        """

        while True:
            frame = self.last_frame()
            if self.room_changed(frame):
                return True

            meta = BattleMetadata(frame, self.detector)

            # Find monster and battle.
            if meta.has_monster():
                LOGGER.info("Found monster")
                self.battle(character, meta)
            # Find items and pick then.
            elif meta.has_item():
                LOGGER.info("Found item")
                self.pick_items(character, meta)
            elif self.dungeon_is_finished(frame):
                LOGGER.info("Dungeon finished")
                break
            # Open gate found, break.
            elif meta.has_open_gate():
                LOGGER.info("Found open gate, break")
                break
            # Search open gate.
            else:
                LOGGER.info("Search open gate")
                self.re_search_dungeon(character)
                # if search_left < 3:
                #     search_left += 1
                #     character.move(180, 0.5)
                # elif search_right == 0:
                #     character.move(0, 1.5)
                # elif search_right < 3:
                #     search_right += 1
                #     character.move(0, 0.5)

        return False

    def post_handler(self, enter_times, character: Character, **kwargs):
        """
        Do something after battle and all items picked.
        e.g. Goto next room, sell items, etc.
        :param enter_times: the times entering this room
        :param character: character under control
        :return: None
        """
        pass


class DungeonRoom(object):
    def __init__(self, dungeon, room_id, scenario, detector):
        self.dungeon = dungeon
        self.room_id = room_id
        self.scenario = scenario
        self.detector = detector
        self.handler_map = {}
        self.enter_times = 0

    def clear(self):
        self.enter_times = 0
        for handler in self.handler_map.values():
            handler.last_exec_skill_time = time.time() - 3600

    def register_handler(self, handler):
        self.handler_map[handler.character_class] = handler

    def exec(self, character, **kwargs):
        assert character.character_class in self.handler_map, "Handler of class {} is not registered".format(
            character.character_class)
        self.enter_times += 1

        handler = self.handler_map[character.character_class]
        handler.pre_handler(self.enter_times, character, **kwargs)
        if handler.handler(self.enter_times, character, **kwargs) and self.room_id != 8:
            LOGGER.info("room changed, break")
            return
        handler.post_handler(self.enter_times, character, **kwargs)


class Dungeon(object):
    def __init__(self, detector):
        self.room_map = {}
        self.detector = detector

    def clear(self):
        for room in self.room_map.values():
            room.clear()

    def register_room(self, room):
        self.room_map[room.room_id] = room

    def detect_room(self, frame):
        pass
