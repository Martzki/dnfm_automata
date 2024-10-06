import math

from src.common.log import Logger

LOGGER = Logger(__name__).logger


class BattleObjectCategory(object):
    Character = 0
    Item = 1
    OpenLeftGate = 2
    OpenRightGate = 3
    OpenUpGate = 4
    OpenDownGate = 5
    CloseLeftGate = 6
    CloseRightGate = 7
    CloseUpGate = 8
    CloseDownGate = 9
    MonsterPriority0 = 10
    MonsterPriority1 = 11
    MonsterPriority2 = 12
    MonsterPriority3 = 13
    DungeonMapRoom0 = 14
    DungeonMapRoom1 = 15
    DungeonMapRoom2 = 16
    DungeonMapRoom3 = 17
    DungeonMapRoom4 = 18
    DungeonMapRoom5 = 19
    DungeonMapRoom6 = 20
    DungeonMapRoom7 = 21
    DungeonMapRoom8 = 22
    DungeonMapRoom9 = 23
    DungeonMapRoom10 = 24
    DungeonMapRoom11 = 25
    DungeonMapRoom12 = 26
    DungeonMapRoom13 = 27
    DungeonMapRoom14 = 28
    DungeonMapRoom15 = 29
    DungeonMapRoom16 = 30
    DungeonMapRoom17 = 31
    DungeonMapRoom18 = 32
    DungeonMapRoom19 = 33
    DungeonMapRoom20 = 34


class BattleObject(object):
    def __init__(self, left_top: tuple, right_bottom: tuple):
        self.left_top = left_top
        self.right_bottom = right_bottom

    def coordinate(self):
        return (self.left_top[0] + self.right_bottom[0]) / 2, self.right_bottom[1]

    def center(self):
        return (self.left_top[0] + self.right_bottom[0]) / 2, (self.left_top[1] + self.right_bottom[1]) / 2

    def left_center(self):
        return self.left_top[0], (self.left_top[1] + self.right_bottom[1]) / 2

    def right_center(self):
        return self.right_bottom[0], (self.left_top[1] + self.right_bottom[1]) / 2

    def up_center(self):
        return (self.left_top[0] + self.right_bottom[0]) / 2, self.left_top[1]

    def down_center(self):
        return (self.left_top[0] + self.right_bottom[0]) / 2, self.left_top[1]


class Character(BattleObject):
    pass


class Item(BattleObject):
    pass


class Gate(BattleObject):
    DirectionLeft = 0
    DirectionRight = 1
    DirectionUp = 2
    DirectionDown = 3

    def __init__(self, left_top, right_bottom, direction, is_open=True):
        super().__init__(left_top, right_bottom)
        self.direction = direction
        self.is_open = is_open

    def __repr__(self):
        return f"Gate({self.direction}, {self.is_open})"


class Monster(BattleObject):
    def __init__(self, left_top, right_bottom, priority):
        super().__init__(left_top, right_bottom)
        self.priority = priority


class BattleMetadata(object):
    UnknownRoomId = -1

    def __init__(self, frame=None, detector=None):
        self.character = None
        self.frame = frame
        self.items = []
        self.monsters_priority_0 = []
        self.monsters_priority_1 = []
        self.monsters_priority_2 = []
        self.monsters_priority_3 = []
        self.left_gate = None
        self.right_gate = None
        self.up_gate = None
        self.down_gate = None
        self.room_id = BattleMetadata.UnknownRoomId
        self.room_confidence = 0

        if frame is None or detector is None:
            return

        result = detector.inference(frame)
        for obj in result:
            if obj.category == BattleObjectCategory.Character:
                self.character = Character(obj.left_top, obj.right_bottom)
            elif obj.category == BattleObjectCategory.Item:
                self.items.append(Item(obj.left_top, obj.right_bottom))
            elif obj.category == BattleObjectCategory.OpenLeftGate:
                self.left_gate = Gate(obj.left_top, obj.right_bottom, Gate.DirectionLeft, True)
            elif obj.category == BattleObjectCategory.OpenRightGate:
                self.right_gate = Gate(obj.left_top, obj.right_bottom, Gate.DirectionRight, True)
            elif obj.category == BattleObjectCategory.OpenUpGate:
                self.up_gate = Gate(obj.left_top, obj.right_bottom, Gate.DirectionUp, True)
            elif obj.category == BattleObjectCategory.OpenDownGate:
                self.down_gate = Gate(obj.left_top, obj.right_bottom, Gate.DirectionDown, True)
            elif obj.category == BattleObjectCategory.CloseLeftGate:
                self.left_gate = Gate(obj.left_top, obj.right_bottom, Gate.DirectionLeft, False)
            elif obj.category == BattleObjectCategory.CloseRightGate:
                self.right_gate = Gate(obj.left_top, obj.right_bottom, Gate.DirectionRight, False)
            elif obj.category == BattleObjectCategory.CloseUpGate:
                self.up_gate = Gate(obj.left_top, obj.right_bottom, Gate.DirectionUp, False)
            elif obj.category == BattleObjectCategory.CloseDownGate:
                self.down_gate = Gate(obj.left_top, obj.right_bottom, Gate.DirectionDown, False)
            elif obj.category == BattleObjectCategory.MonsterPriority0:
                self.monsters_priority_0.append(Monster(obj.left_top, obj.right_bottom, 0))
            elif obj.category == BattleObjectCategory.MonsterPriority1:
                self.monsters_priority_1.append(Monster(obj.left_top, obj.right_bottom, 1))
            elif obj.category == BattleObjectCategory.MonsterPriority2:
                self.monsters_priority_2.append(Monster(obj.left_top, obj.right_bottom, 2))
            elif obj.category == BattleObjectCategory.MonsterPriority3:
                self.monsters_priority_3.append(Monster(obj.left_top, obj.right_bottom, 3))
            elif (BattleObjectCategory.DungeonMapRoom0 <= obj.category <= BattleObjectCategory.DungeonMapRoom20 and
                  obj.confidence > self.room_confidence):
                self.room_id = obj.category - BattleObjectCategory.DungeonMapRoom0
                self.room_confidence = obj.confidence
            else:
                LOGGER.error(f"Unknown category: {obj.category}")

    def __repr__(self):
        has_character = self.character is not None
        has_item = self.has_item()
        has_monster = self.has_monster()
        has_left_gate = self.left_gate and self.left_gate.is_open
        has_right_gate = self.right_gate and self.right_gate.is_open
        has_up_gate = self.up_gate and self.up_gate.is_open
        has_down_gate = self.down_gate and self.down_gate.is_open
        return f"meta(room_id: {self.room_id}, has_character: {has_character}, has_monster: {has_monster}, has_item: {has_item}, has_left_gate: {has_left_gate}, has_right_gate: {has_right_gate}, has_up_gate: {has_up_gate}, has_down_gate: {has_down_gate})"

    def has_monster(self):
        return len(self.monsters_priority_0) or len(self.monsters_priority_1) or len(self.monsters_priority_2) or len(
            self.monsters_priority_3)

    def has_item(self):
        return len(self.items) > 0

    def has_open_gate(self):
        return (self.left_gate and self.left_gate.is_open) or (self.right_gate and self.right_gate.is_open) or (
                self.up_gate and self.up_gate.is_open) or (self.down_gate and self.down_gate.is_open)

    @staticmethod
    def get_distance(src, dst, vertical_only=False):
        if vertical_only:
            return abs(src[1] - dst[1])
        else:
            return math.sqrt((src[0] - dst[0]) ** 2 + (src[1] - dst[1]) ** 2)

    @staticmethod
    def get_move_duration(distance, vertical_only=False):
        return distance / (600.0 if vertical_only else 1000.0)

    @staticmethod
    def get_rad(src, dst):
        return math.atan2(src[1] - dst[1], dst[0] - src[0])

    def get_closest_target(self, get_monster=False, get_item=False, vertical_only=False):
        target_list = []
        if get_monster:
            if len(self.monsters_priority_3) > 0:
                target_list = self.monsters_priority_3
            elif len(self.monsters_priority_2) > 0:
                target_list = self.monsters_priority_2
            elif len(self.monsters_priority_1) > 0:
                target_list = self.monsters_priority_1
            elif len(self.monsters_priority_0) > 0:
                target_list = self.monsters_priority_0
        elif get_item:
            target_list = self.items

        closest_target = None
        closest_distance = 0
        for target in target_list:
            # Character is not detected.
            if self.character is None:
                return target, 0

            distance = BattleMetadata.get_distance(self.character.coordinate(), target.coordinate(), vertical_only)
            if not closest_target or distance < closest_distance:
                closest_distance = distance
                closest_target = target

        return closest_target, closest_distance

    def get_closest_monster(self, vertical_only=False):
        return self.get_closest_target(get_monster=True, vertical_only=vertical_only)

    def get_closest_item(self):
        return self.get_closest_target(get_item=True, vertical_only=False)
