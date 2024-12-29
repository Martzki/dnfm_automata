import time
from pathlib import Path

import cv2
from func_timeout import FunctionTimedOut

from common.log import Logger
from runtime.ui import ui_elements

LOGGER = Logger(__name__).logger


class UIElement(object):
    CategoryCharacter = "character"
    CategoryCommon = "common"
    CategoryDungeon = "dungeon"
    CategorySkill = "skill"

    def __init__(self, coordinate=None, key_img_list=None, key_text_list=None):
        assert coordinate or key_img_list or key_text_list, \
            f"Invalid arguments: {coordinate}, {key_img_list}, {key_text_list}"

        self.coordinate = tuple(coordinate) if isinstance(coordinate, list) and len(coordinate) == 2 else None
        self.raw_key_img_list = key_img_list
        self.key_img_list = []
        if key_img_list:
            for key_img in key_img_list:
                LOGGER.debug(f"add key img {key_img}")
                self.key_img_list.append(cv2.imread(str(key_img)))
        self.key_text_list = key_text_list if key_text_list else []

    def __repr__(self):
        return f"coordinate({self.coordinate}, {self.raw_key_img_list}, {self.key_text_list})"


class UIElementCtx(object):
    def __init__(self, device, detector, base_dir='.'):
        self.ui_element_map = {}
        self.base_dir = Path(base_dir)
        self.device = device
        self.detector = detector

    def register_ui_element(self, key, ui_element):
        LOGGER.debug(f"register {key} {ui_element}")
        self.ui_element_map[key] = ui_element

    def register_dynamic_ui_elements(self, path, prefix):
        element_map = {}
        for each in path.glob("*.png"):
            element_name = each.name.split('.')[0]
            if element_name not in element_map:
                element_map[element_name] = {"key_img_list": []}
            element_map[element_name]["key_img_list"].append(each)

        for each in element_map.keys():
            self.register_ui_element(
                f"{prefix}.{each}",
                UIElement(key_img_list=element_map[each]["key_img_list"])
            )

    def load(self, conf, base_dir=None):
        if base_dir is None:
            base_dir = self.base_dir

        for category in [getattr(UIElement, c) for c in vars(UIElement).keys() if not c.startswith("__")]:
            # Register static elements.
            if category in conf:
                for each in conf[category]:
                    coordinate = conf[category][each]
                    self.register_ui_element(f"{category}.{each}", UIElement(coordinate=coordinate))

            # Register dynamic elements.
            self.register_dynamic_ui_elements(base_dir / category, category)

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
        return self.get_coordinate(f"{UIElement.CategorySkill}.{character_class}.{name}", conf_thres=0.65)

    def get_ui_coordinate(self, key, use_cache=True, conf_thres=0.85):
        return self.get_coordinate(f"{key}", use_cache, conf_thres=conf_thres)

    def wait_ui_element(self, key, timeout=10):
        start = time.time()
        while True:
            if time.time() - start > timeout:
                raise FunctionTimedOut(f"Waiting UI element: {key} timeout")

            coordinate = self.get_ui_coordinate(key, use_cache=False)
            if coordinate is not None:
                return coordinate

    def double_check(self):
        try:
            check_box = self.wait_ui_element(ui_elements.Common.CheckBox, timeout=2)
            self.device.touch(check_box, 0.1)
            time.sleep(0.5)
        except FunctionTimedOut:
            # Some double check doesn't have checkbox.
            pass

        try:
            confirm = self.wait_ui_element(ui_elements.Common.Confirm, timeout=2)
            self.device.touch(confirm, 0.1)
            time.sleep(0.5)
        except FunctionTimedOut:
            return

    def click_ui_element(self, key, double_check=False, timeout=10, delay=0.5):
        try:
            element = self.wait_ui_element(key, timeout)
            self.device.touch(element, 0.1)
        except FunctionTimedOut as e:
            raise LookupError(f"Failed to get coordinate of {key}: {e}")

        if double_check:
            self.double_check()

        time.sleep(delay)
