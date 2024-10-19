import glob
import time

import cv2
from func_timeout import FunctionTimedOut

from common.log import Logger

LOGGER = Logger(__name__).logger


class CoordinateType(object):
    Fixed = 0
    Match = 1
    Ocr = 2


class CoordinateCategory(object):
    Skill = "skill"
    UI = "ui"


class UIElement(object):
    def __init__(self, coordinate=None, key_img_list=None, key_text_list=None):
        assert coordinate or key_img_list or key_text_list, \
            f"Invalid arguments: {coordinate}, {key_img_list}, {key_text_list}"

        self.coordinate = tuple(coordinate) if isinstance(coordinate, list) and len(coordinate) == 2 else None
        self.key_img_list = []
        if key_img_list:
            for key_img in key_img_list:
                for each in glob.glob(key_img):
                    LOGGER.debug("add key img {}".format(each))
                    self.key_img_list.append(cv2.imread(each))
        self.key_text_list = key_text_list if key_text_list else []

    def __repr__(self):
        return f"coordinate({self.coordinate}, {len(self.key_img_list)}, {self.key_text_list})"


class UIElementCtx(object):
    CategoryBase = "base"
    CategoryCharacter = "character"
    CategoryDungeon = "dungeon"
    CategorySkill = "skill"

    def __init__(self, device, detector):
        self.ui_element_map = {}
        self.device = device
        self.detector = detector

    def register_ui_element(self, key, ui_element):
        self.ui_element_map[key] = ui_element

    def load(self, conf):
        for category in [UIElementCtx.CategoryBase, UIElementCtx.CategoryCharacter, UIElementCtx.CategoryDungeon]:
            if category not in conf:
                continue

            for each in conf[category]:
                element = conf[category][each]
                self.register_ui_element(f"ui.{category}.{each}",
                                         UIElement(element.get("coordinate"), element.get("key_img"),
                                                   element.get("key_text")))

        if UIElementCtx.CategorySkill in conf:
            for character_class in conf[UIElementCtx.CategorySkill]:
                for each in conf[UIElementCtx.CategorySkill][character_class]:
                    skill = conf[UIElementCtx.CategorySkill][character_class][each]
                    self.register_ui_element(f"ui.{UIElementCtx.CategorySkill}.{character_class}.{each}",
                                             UIElement(skill.get("coordinate"), skill.get("key_img"),
                                                       skill.get("key_text")))

    def get_coordinate(self, key, use_cache=True, conf_thres=0.65):
        if key not in self.ui_element_map:
            return None

        element = self.ui_element_map[key]
        if use_cache and element.coordinate is not None:
            return element.coordinate

        coordinate = None
        if element.key_img_list:
            result = self.detector.img_match(self.device.last_frame(), element.key_img_list)
            if result.confidence > conf_thres:
                coordinate = result.center
        elif element.key_text_list:
            coordinate = self.detector.ocr_match(self.device.last_frame(), element.key_text_list)

        self.ui_element_map[key].coordinate = coordinate

        return coordinate

    def get_skill_coordinate(self, character_class, name):
        return self.get_coordinate(f"ui.{UIElementCtx.CategorySkill}.{character_class}.{name}", conf_thres=0.65)

    def get_ui_coordinate(self, category, key, use_cache=True, conf_thres=0.85):
        return self.get_coordinate(f"ui.{category}.{key}", use_cache, conf_thres=conf_thres)

    def wait_ui_element(self, category, name, timeout=10):
        start = time.time()
        while True:
            if time.time() - start > timeout:
                raise FunctionTimedOut(f"Waiting UI element: ui.{category}.{name} timeout")

            coordinate = self.get_ui_coordinate(category, name, use_cache=False)
            if coordinate is not None:
                return coordinate

    def double_check(self):
        try:
            check_box = self.wait_ui_element(UIElementCtx.CategoryBase, "check_box", timeout=2)
            self.device.touch(check_box, 0.1)
            time.sleep(0.5)
        except FunctionTimedOut:
            return

        try:
            confirm = self.wait_ui_element(UIElementCtx.CategoryBase, "confirm")
            self.device.touch(confirm, 0.1)
            time.sleep(0.5)
        except FunctionTimedOut:
            return

    def click_ui_element(self, category, name, double_check=False, timeout=10, delay=0.5):
        try:
            element = self.wait_ui_element(category, name, timeout)
            self.device.touch(element, 0.1)
            time.sleep(delay)
        except FunctionTimedOut as e:
            raise LookupError(f"Failed to get coordinate of {category} {name}: {e}")

        if double_check:
            self.double_check()
