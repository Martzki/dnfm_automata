import cv2
import numpy as np


class DungeonMapRoom(object):
    LeftRoomIndex = 3
    RightRoomIndex = 5
    UpRoomIndex = 1
    DownRoomIndex = 7
    HasGateThreshold = 10
    HasLeftGate = 0x1
    HasRightGate = 0x2
    HasUpGate = 0x4
    HasDownGate = 0x8

    def __init__(self, room_img):
        self.gate_width, self.gate_height = room_img.shape[1] // 3, room_img.shape[0] // 3
        self.is_empty = cv2.countNonZero(room_img) == 0
        self.has_left_gate = cv2.countNonZero(
            self.get_gate_img(room_img, DungeonMapRoom.LeftRoomIndex)) > DungeonMapRoom.HasGateThreshold
        self.has_right_gate = cv2.countNonZero(
            self.get_gate_img(room_img, DungeonMapRoom.RightRoomIndex)) > DungeonMapRoom.HasGateThreshold
        self.has_up_gate = cv2.countNonZero(
            self.get_gate_img(room_img, DungeonMapRoom.UpRoomIndex)) > DungeonMapRoom.HasGateThreshold
        self.has_down_gate = cv2.countNonZero(
            self.get_gate_img(room_img, DungeonMapRoom.DownRoomIndex)) > DungeonMapRoom.HasGateThreshold
        self.gate_mask = 0
        if self.has_left_gate:
            self.gate_mask |= DungeonMapRoom.HasLeftGate
        if self.has_right_gate:
            self.gate_mask |= DungeonMapRoom.HasRightGate
        if self.has_up_gate:
            self.gate_mask |= DungeonMapRoom.HasUpGate
        if self.has_down_gate:
            self.gate_mask |= DungeonMapRoom.HasDownGate

    def get_gate_img(self, room_img, index):
        """
        This function returns specific gate img.
        :param room_img: image of a room
        :param index: index of a 3 x 3 matrix, e.g. up gate: 1, left gate: 3
        :return: gate image
        """
        return room_img[index // 3 * self.gate_height: (index // 3 + 1) * self.gate_height,
               (index % 3) * self.gate_width: (index % 3 + 1) * self.gate_width]


class DungeonMap(object):
    CenterRoomIndex = 4
    LeftRoomIndex = 3
    RightRoomIndex = 5
    UpRoomIndex = 1
    DownRoomIndex = 7

    def __init__(self, map_img):
        try:
            hsv = cv2.cvtColor(map_img, cv2.COLOR_BGR2HSV)

            lower = np.array([0, 0, 170], dtype=np.uint8)
            upper = np.array([180, 255, 255], dtype=np.uint8)
            mask = cv2.inRange(hsv, lower, upper)
            color_only = cv2.bitwise_and(map_img, map_img, mask=mask)
            all_room_img = cv2.cvtColor(color_only, cv2.COLOR_BGR2GRAY)

            lower = np.array([17, 90, 170], dtype=np.uint8)
            upper = np.array([25, 150, 255], dtype=np.uint8)
            mask = cv2.inRange(hsv, lower, upper)
            yellow_only = cv2.bitwise_and(map_img, map_img, mask=mask)
            visited_room_img = cv2.cvtColor(yellow_only, cv2.COLOR_BGR2GRAY)

            self.valid = cv2.countNonZero(visited_room_img) > 0
            if self.valid:
                self.room_width, self.room_height = map_img.shape[1] // 3, map_img.shape[0] // 3
                self.room_matrix = self.get_room_matrix(all_room_img)
                self.center_room = DungeonMapRoom(self.get_room_img(visited_room_img, DungeonMap.CenterRoomIndex))
                self.left_room = DungeonMapRoom(self.get_room_img(visited_room_img, DungeonMap.LeftRoomIndex))
                self.right_room = DungeonMapRoom(self.get_room_img(visited_room_img, DungeonMap.RightRoomIndex))
                self.up_room = DungeonMapRoom(self.get_room_img(visited_room_img, DungeonMap.UpRoomIndex))
                self.down_room = DungeonMapRoom(self.get_room_img(visited_room_img, DungeonMap.DownRoomIndex))
                self.room_mask = self.get_room_mask(all_room_img)
        except cv2.error:
            self.valid = False

    def get_room_img(self, map_img, index):
        """
        This function returns specific room img.
        :param map_img: image of a room
        :param index: index of a 3 x 3 matrix, e.g. up room: 1, left room: 3
        :return: room image
        """
        return map_img[index // 3 * self.room_height: (index // 3 + 1) * self.room_height,
               (index % 3) * self.room_width: (index % 3 + 1) * self.room_width]

    def get_room_mask(self, map_img):
        room_mask = 0
        for i in range(9):
            room_img = self.get_room_img(map_img, i)
            if cv2.countNonZero(room_img) > 0:
                room_mask |= 1 << i

        return room_mask

    def get_room_matrix(self, map_img):
        room_matrix = []
        for i in range(9):
            room_matrix.append(DungeonMapRoom(self.get_room_img(map_img, i)))

        return room_matrix


def get_map_img(frame):
    try:
        map = frame[41:218, 2195:2366]
        return map
        hsv = cv2.cvtColor(map, cv2.COLOR_BGR2HSV)
        lower = np.array([17, 90, 170], dtype=np.uint8)
        upper = np.array([25, 150, 255], dtype=np.uint8)
        mask = cv2.inRange(hsv, lower, upper)
        yellow_only = cv2.bitwise_and(map, map, mask=mask)

        return cv2.cvtColor(yellow_only, cv2.COLOR_BGR2GRAY)
    except cv2.error:
        return None
