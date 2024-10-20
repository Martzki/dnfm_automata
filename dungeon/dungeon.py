import random
import time

from func_timeout import func_set_timeout, FunctionTimedOut

from character.character import Character
from common.log import Logger
from detector.detector import Detector
from device.device import Device
from dungeon.battle import BattleMetadata
from dungeon.strategy import BattleStrategy
from ui.ui import UIElementCtx

LOGGER = Logger(__name__).logger
DEFAULT_AREA_HEIGHT = 60
MAX_REVIVE_TIMES = 1


class DungeonReEntered(Exception):
    pass


class DungeonRoomHandler(object):
    def __init__(self, dungeon, room_id, character_class, strategy=None):
        self.dungeon = dungeon
        self.room_id = room_id
        self.character_class = character_class
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

        # Retry 1 time before re-search.
        if self.search_times % 2 != 0:
            angle_list_len = len(self.search_angle)
            scale_search_times = self.search_times // 2
            angle = self.search_angle[scale_search_times % angle_list_len]
            if character.move(angle, 0.4 + 0.4 * (scale_search_times // angle_list_len), self.room_changed):
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
        :return: None
        """
        if meta.character is None:
            LOGGER.info(f"Character not found")
            return

        vertical_only = skill.exec_limit.vertical_only
        monster, distance = meta.get_closest_monster(vertical_only)

        src = meta.character.coordinate()
        dst = monster.coordinate()
        toward_left = src[0] > dst[0]

        if toward_left:
            LOGGER.info(f"Change direction to left")
            character.move(180, 0.1)
            attack_area = {
                "left_top": {
                    "x": float('-inf') if vertical_only else src[0] - skill.exec_limit.min_distance,
                    "y": src[1] - DEFAULT_AREA_HEIGHT / 2
                },
                "right_bottom": {
                    "x": src[0],
                    "y": src[1] + DEFAULT_AREA_HEIGHT / 2
                }
            }
        else:
            LOGGER.info(f"Change direction to right")
            character.move(0, 0.1)
            attack_area = {
                "left_top": {
                    "x": src[0],
                    "y": src[1] - DEFAULT_AREA_HEIGHT / 2
                },
                "right_bottom": {
                    "x": float('inf') if vertical_only else src[0] + skill.exec_limit.min_distance,
                    "y": src[1] + DEFAULT_AREA_HEIGHT / 2
                }
            }

        monster_area = {
            "left_top": {
                "x": monster.left_top[0],
                "y": monster.right_bottom[1] - DEFAULT_AREA_HEIGHT / 2
            },
            "right_bottom": {
                "x": monster.right_bottom[0],
                "y": monster.right_bottom[1] + DEFAULT_AREA_HEIGHT / 2
            }
        }

        move_vector = {"x": 0, "y": 0}
        if attack_area["left_top"]["x"] > monster_area["right_bottom"]["x"]:
            move_vector["x"] = monster_area["right_bottom"]["x"] - attack_area["left_top"]["x"]
            if attack_area["left_top"]["y"] > monster_area["right_bottom"]["y"]:
                move_vector["y"] = monster_area["right_bottom"]["y"] - attack_area["left_top"]["y"]
            elif attack_area["right_bottom"]["y"] < monster_area["left_top"]["y"]:
                move_vector["y"] = monster_area["left_top"]["y"] - attack_area["right_bottom"]["y"]
        elif attack_area["right_bottom"]["x"] < monster_area["left_top"]["x"]:
            move_vector["x"] = monster_area["left_top"]["x"] - attack_area["right_bottom"]["x"]
            if attack_area["left_top"]["y"] > monster_area["right_bottom"]["y"]:
                move_vector["y"] = monster_area["right_bottom"]["y"] - attack_area["left_top"]["y"]
            elif attack_area["right_bottom"]["y"] < monster_area["left_top"]["y"]:
                move_vector["y"] = monster_area["left_top"]["y"] - attack_area["right_bottom"]["y"]
        elif attack_area["left_top"]["y"] > monster_area["right_bottom"]["y"]:
            move_vector["y"] = monster_area["right_bottom"]["y"] - attack_area["left_top"]["y"]
            if attack_area["left_top"]["x"] > monster_area["right_bottom"]["x"]:
                move_vector["x"] = monster_area["right_bottom"]["x"] - attack_area["left_top"]["x"]
            elif attack_area["right_bottom"]["x"] < monster_area["left_top"]["x"]:
                move_vector["x"] = monster_area["left_top"]["x"] - attack_area["right_bottom"]["x"]
        elif attack_area["right_bottom"]["y"] < monster_area["left_top"]["y"]:
            move_vector["y"] = monster_area["left_top"]["y"] - attack_area["right_bottom"]["y"]
            if attack_area["left_top"]["x"] > monster_area["right_bottom"]["x"]:
                move_vector["x"] = monster_area["right_bottom"]["x"] - attack_area["left_top"]["x"]
            elif attack_area["right_bottom"]["x"] < monster_area["left_top"]["x"]:
                move_vector["x"] = monster_area["left_top"]["x"] - attack_area["right_bottom"]["x"]
        else:
            LOGGER.info("No need to move")
            return

        dst = (
            src[0] + move_vector["x"],
            src[1] + move_vector["y"]
        )

        character.move_toward(src, dst)

    def battle(self, character, meta):
        now = time.time()
        if now - self.last_exec_skill_time > 3:
            skill = self.battle_strategy.get_next_skill(character)
            skill = skill if skill else character.attack
        else:
            skill = character.attack

        # Try to move closer.
        self.move_toward_monster(character, skill, meta)

        LOGGER.info(f"Exec skill {skill}")
        character.exec_skill(skill)

        time.sleep(0.15)

        if skill != character.attack:
            self.last_exec_skill_time = now

        if meta.character is None:
            self.re_search_dungeon(character)

    def pick_items(self, character, meta, ignore_room_change=False):
        """
        Pick found items.
        :param character: character
        :param meta: battle metadata
        :param ignore_room_change: whether ignore room change when moving or not
        :return: None
        """
        item, distance = meta.get_closest_item()
        if item is None:
            LOGGER.info("Failed to found closest item")
            return True

        if meta.character:
            LOGGER.info(f"Move toward item from {meta.character.coordinate()} to {item.coordinate()}")
            character.move_toward(
                meta.character.coordinate(),
                item.coordinate(),
                None if ignore_room_change else self.room_changed
            )
            time.sleep(0.1)
            return

        if self.re_search_dungeon(character):
            return

    def maintain_equipments(self):
        pass

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
    def __init__(self, dungeon, room_id):
        self.dungeon = dungeon
        self.room_id = room_id
        self.handler_map = {}
        self.enter_times = 0
        self.revive_times = 0

    def clear(self):
        self.enter_times = 0
        self.revive_times = 0
        for handler in self.handler_map.values():
            handler.last_exec_skill_time = time.time() - 3600

    def register_handler(self, handler):
        self.handler_map[handler.character_class] = handler

    @func_set_timeout(180)
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
    def __init__(self, device: Device, detector: Detector, ui_ctx: UIElementCtx):
        self.room_map = {}
        self.device = device
        self.detector = detector
        self.ui_ctx = ui_ctx
        self.battle_metadata = BattleMetadata()
        self.stats = {
            'last_dump_ts': time.time(),
            'inference_cnt': 0,
            'inference_time': 0
        }
        self.room_id = BattleMetadata.UnknownRoomId

    def goto_dungeon(self):
        pass

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

    def pick_cards(self, card_list=None):
        if self.ui_ctx.wait_ui_element(UIElementCtx.CategoryDungeon, "card", timeout=10) is None:
            LOGGER.error("failed to get card coordinate")
            return

        # Choose a free card arbitrarily.
        if card_list is None:
            card_list = [random.randint(0, 3)]

        for card in card_list:
            card_key = f"card_{card}"
            coordinate = self.ui_ctx.get_ui_coordinate(UIElementCtx.CategoryDungeon, card_key)
            if coordinate is None:
                continue

            LOGGER.info(f"pick card {card}")
            self.device.touch(coordinate, 0.1)

            time.sleep(0.2)

        time.sleep(0.5)

        # Touch empty area to skip picking.
        self.device.touch((100, 100), 0.1)

    def re_enter(self):
        LOGGER.info("Start to re-enter dungeon")
        self.ui_ctx.click_ui_element(UIElementCtx.CategoryDungeon, "re_enter_dungeon", double_check=True, timeout=15)

    @func_set_timeout(10)
    def wait_in_dungeon(self):
        while self.get_room() is None:
            continue

    def revive(self, room):
        try:
            self.ui_ctx.wait_ui_element(UIElementCtx.CategoryDungeon, "dead_revive")
        except FunctionTimedOut:
            LOGGER.warning("Character not dead")
            return

        # Revive.
        if room.revive_times < MAX_REVIVE_TIMES:
            room.revive_times += 1
            try:
                LOGGER.info("Character dead, try to revive")
                self.ui_ctx.click_ui_element(UIElementCtx.CategoryDungeon, "dead_revive")
            except LookupError as e:
                LOGGER.error(f"Failed to revive: {e}")
        # Back to town and re-enter dungeon.
        else:
            try:
                LOGGER.info(f"Revive times are larger than {MAX_REVIVE_TIMES}, back to town and re-enter dungeon")
                self.ui_ctx.click_ui_element(
                    UIElementCtx.CategoryDungeon,
                    "dead_back_to_town",
                    double_check=True,
                    delay=15
                )
                LOGGER.info("Back to town and re-enter dungeon")
                self.goto_dungeon()
                raise DungeonReEntered(
                    f"Revive times are larger than {MAX_REVIVE_TIMES}, back to town and re-enter dungeon"
                )
            except LookupError as e:
                LOGGER.error(f"Failed to re-enter dungeon: {e}")
