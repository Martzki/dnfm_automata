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
        self.search_angle_index = 0
        if strategy is None:
            self.battle_strategy = BattleStrategy()

    def room_changed(self, frame=None):
        frame = self.last_frame() if frame is None else frame
        result = self.detector.img_match(frame, [self.in_dungeon_img])
        if result.confidence < 0.9:
            return True

        room = self.detect_room(frame)
        if not room:
            LOGGER.warning(f"Room is not detected.")
            return False

        if room.room_id == self.room_id:
            return False

        LOGGER.info(f"Room changed from {self.room_id} to {room.room_id}")

        return True

    def refind_character(self, character):
        angle = self.search_angle[self.search_angle_index % 4]
        character.move(angle, 0.2)
        self.search_angle_index += 1

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

        if skill.exec_limit.min_distance < distance:
            duration = BattleMetadata.get_move_duration(distance)
            move_duration = 1 if duration > 1 else duration
            LOGGER.info(f"Move toward monster with {move_duration}")
            character.move_with_rad(BattleMetadata.get_rad(meta.character.coordinate(), monster.coordinate()),
                                    move_duration)
            return duration > 1
        else:
            LOGGER.info(f"Change direction")
            character.move_with_rad(BattleMetadata.get_rad(meta.character.coordinate(), monster.coordinate()), 0.1)

        return False

    def battle(self, character, meta):
        # skill_strategy = self.battle_strategy.get_next_skill()
        # skill = skill_strategy.skill if skill_strategy else character.skill_attack
        skill = character.attack

        # Need attach before execute skill.
        # if skill_strategy and skill_strategy.pre_attack_duration:
        #     # Need move closer.
        #     if self.move_toward_monster(character, character.skill_attack, meta):
        #         return
        #
        #     character.attack(skill.pre_attack_duration)

        # Need move closer.
        if self.move_toward_monster(character, skill, meta):
            return

        LOGGER.info(f"Exec skill {skill}")
        character.exec_skill(skill, 0.8)

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
            self.refind_character(character)

    def maintain_equipments(self):
        pass

    def dungeon_is_finished(self, frame):
        result = self.detector.img_match(frame, [self.finish_img])
        return result.confidence > 0.9

    def pre_handler(self, enter_times, character: Character):
        """
        Do something before auto battle.
        e.g. Move to somewhere and execute some skill.
        :param enter_times: the time entering this room
        :param character: character under control
        :return: None
        """
        pass

    def handler(self, enter_times, character):
        """
        Kill all monsters and pick all items in this dungeon.
        :param character: character under control
        :param enter_times: the times entering this room
        :return: room changed or not
        """
        if enter_times > 1:
            return False

        search_left = 0
        search_right = 0

        while True:
            frame = self.last_frame()
            if self.room_changed(frame):
                return True

            meta = BattleMetadata(frame, self.detector)

            # Find monster and battle.
            if meta.has_monster():
                LOGGER.info("Found monster")
                # time.sleep(1)
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
                if search_left < 3:
                    search_left += 1
                    character.move(180, 0.5)
                elif search_right == 0:
                    character.move(0, 1.5)
                elif search_right < 3:
                    search_right += 1
                    character.move(0, 0.5)

        return False

    def post_handler(self, enter_times, character: Character):
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

    def register_handler(self, handler):
        self.handler_map[handler.character_class] = handler

    def exec(self, character):
        assert character.character_class in self.handler_map, "Handler of class {} is not registered".format(
            character.character_class)
        self.enter_times += 1

        handler = self.handler_map[character.character_class]
        handler.pre_handler(self.enter_times, character)
        if handler.handler(self.enter_times, character) and self.room_id != 8:
            LOGGER.info("room changed, break")
            return
        handler.post_handler(self.enter_times, character)


class DungeonCtx(object):
    def __init__(self, detector):
        self.room_list = []
        self.detector = detector

    def clear(self):
        for room in self.room_list:
            room.clear()

    def register_room(self, room):
        self.room_list.append(room)

    def detect_room(self, frame):
        map_img = frame[
                  39: 220,
                  2162: 2400,
                  ]

        best_match_room = None
        best_match_confidence = 0
        match_dst = []
        match_shape = []
        for room in self.room_list:
            result = room.scenario.detect(self.detector, map_img)
            if result and result.confidence > best_match_confidence:
                best_match_room = room
                best_match_confidence = result.confidence
                match_dst.append(result.dst)
                match_shape.append(result.shape)

        # for i in range(len(match_dst)):
        #     shape = match_shape[i]
        #     top_left = match_dst[i]
        #     t_height, t_width = shape[0], shape[1]
        #     bottom_right = (top_left[0] + t_width, top_left[1] + t_height)
        #     debug = cv2.rectangle(map_img, top_left, bottom_right, (0, 255, 0), 2)
        #     cv2.imwrite("match_result_{}.png".format(i), debug)
        #     i += 1

        if best_match_room:
            LOGGER.debug(f"Get room {best_match_room.room_id} with confidence {best_match_confidence}")

        return best_match_room
