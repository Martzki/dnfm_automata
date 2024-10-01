import time

import cv2

from src.common.log import Logger
from src.lib.character.character import Character
from src.lib.detector.detector import Detector
from src.lib.device.device import Device
from src.lib.dungeon.battle import BattleMetadata
from src.lib.dungeon.strategy import BattleStrategy

LOGGER = Logger(__name__).logger


class DungeonRoomHandler(object):
    def __init__(self, dungeon, room_id, character_class, strategy=None):
        self.dungeon = dungeon
        self.room_id = room_id
        self.character_class = character_class
        self.finish_img = cv2.imread('res/scenario/base/dungeon_finish.png')
        self.re_enter_img = cv2.imread('res/scenario/base/re_enter.png')
        self.search_angle = (20, 270, 160, 270)
        self.search_times = 0
        self.last_search_time = time.time()
        self.last_exec_skill_time = time.time()
        self.battle_strategy = strategy if strategy else BattleStrategy()

    def room_changed(self):
        room_id = self.dungeon.get_battle_metadata().room_id
        if room_id != self.room_id:
            LOGGER.info(f"Room changed from {self.room_id} to {room_id}")
        return room_id != self.room_id

    def re_search_dungeon(self, character):
        LOGGER.info("re-search dungeon")
        if time.time() - self.last_search_time > 3:
            self.search_times = 0

        angle = self.search_angle[self.search_times % 4]
        if character.move(angle, 0.4 + 0.4 * (self.search_times // 4), self.room_changed):
            return True

        self.search_times += 1
        self.last_search_time = time.time()

        return False

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
            return

        if self.re_search_dungeon(character):
            return

    def maintain_equipments(self):
        pass

    def dungeon_is_finished(self):
        frame = self.dungeon.get_battle_metadata().frame
        result = self.dungeon.detector.img_match(frame, [self.finish_img])
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
            if self.room_changed():
                return True

            meta = self.dungeon.get_battle_metadata()

            # Find monster and battle.
            if meta.has_monster():
                LOGGER.info("Found monster")
                self.battle(character, meta)
            # Find items and pick then.
            elif meta.has_item():
                LOGGER.info("Found item")
                self.pick_items(character, meta)
            elif self.dungeon_is_finished():
                LOGGER.info("Dungeon finished")
                break
            # Open gate found, break.
            elif meta.has_open_gate():
                LOGGER.info("Found open gate, break")
                break
            # Search open gate.
            else:
                LOGGER.info("Search open gate")
                if self.re_search_dungeon(character):
                    return True

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
    def __init__(self, dungeon, room_id, scenario):
        self.dungeon = dungeon
        self.room_id = room_id
        self.scenario = scenario
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
    def __init__(self, device: Device, detector: Detector):
        self.room_map = {}
        self.device = device
        self.detector = detector
        self.battle_metadata = BattleMetadata()
        self.stats = {
            'last_dump_ts': time.time(),
            'inference_cnt': 0,
            'inference_time': 0
        }
        self.room_id = BattleMetadata.UnknownRoomId

    def clear(self):
        for room in self.room_map.values():
            room.clear()

    def register_room(self, room):
        self.room_map[room.room_id] = room

    def get_battle_metadata(self):
        start = time.time()
        frame = self.device.last_frame()
        meta = BattleMetadata(frame, self.detector)
        now = time.time()
        self.stats['inference_cnt'] += 1
        self.stats['inference_time'] += now - start

        if now - self.stats['last_dump_ts'] > 60:
            LOGGER.info(
                f"last 1 minute {self.stats['inference_cnt']} frame inferenced, fps: {self.stats['inference_cnt'] / self.stats['inference_time']}")
            self.stats['last_dump_ts'] = now
            self.stats['inference_cnt'] = 0
            self.stats['inference_time'] = 0

        return meta

    def get_room(self):
        frame = self.device.last_frame()
        meta = BattleMetadata(frame, self.detector)
        return self.room_map.get(meta.room_id, None)
