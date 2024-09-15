import glob

import cv2

from src.common.log import Logger

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
        if coordinate is None:
            assert key_img_list or key_text_list, "Key img list and key text list can't be both empty"
            self.coordinate = None
            self.key_img_list = []

            for key_img in key_img_list:
                for each in glob.glob(key_img):
                    LOGGER.debug("add key img {}".format(each))
                    self.key_img_list.append(cv2.imread(each))

            self.key_text_list = key_text_list if key_text_list else []
        else:
            assert isinstance(coordinate, list) and len(coordinate) == 2, "Invalid coordinate {}".format(coordinate)
            self.coordinate = tuple(coordinate)
            self.key_img_list = []
            self.key_text_list = []

    def __repr__(self):
        return f"coordinate{self.coordinate}"


class UIElementCtx(object):
    def __init__(self, device, detector):
        self.ui_element_map = {}
        self.device = device
        self.detector = detector

    def register_ui_element(self, key, ui_element):
        self.ui_element_map[key] = ui_element

    def load(self, conf):
        if "base" in conf:
            for each in conf["base"]:
                element = conf["base"][each]
                self.register_ui_element("ui.base.{}".format(each),
                                         UIElement(element.get("coordinate"), element.get("key_img"),
                                                   element.get("key_text")))

        if "skill" in conf:
            for character_class in conf["skill"]:
                for each in conf["skill"][character_class]:
                    skill = conf["skill"][character_class][each]
                    self.register_ui_element("ui.skill.{}.{}".format(character_class, each),
                                             UIElement(skill.get("coordinate"), skill.get("key_img"),
                                                       skill.get("key_text")))

    def get_coordinate(self, key):
        if key not in self.ui_element_map:
            return None

        element = self.ui_element_map[key]
        if element.coordinate is not None:
            return element.coordinate

        coordinate = None
        if element.key_img_list:
            result = self.detector.img_match(self.device.last_frame(), element.key_img_list)
            if result.confidence > 0:
                coordinate = result.center
        elif element.key_text_list:
            coordinate = self.detector.ocr_match(self.device.last_frame(), element.key_text_list)

        self.ui_element_map[key].coordinate = coordinate

        return coordinate

    def get_skill_coordinate(self, character_class, name):
        return self.get_coordinate("ui.skill.{}.".format(character_class) + name)

    def get_ui_coordinate(self, name):
        return self.get_coordinate("ui.base." + name)
