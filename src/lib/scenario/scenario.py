import glob

import cv2

from src.common.log import Logger

LOGGER = Logger(__name__).logger


class Scenario(object):
    def __init__(self, name, key_img_list=None, key_text_list=None):
        assert key_img_list or key_text_list, "img and text can't be both empty"
        self.name = name
        if key_img_list is None:
            key_img_list = []
        if key_text_list is None:
            key_text_list = []
        self.key_img_list = []
        for key_img in key_img_list:
            for each in glob.glob(key_img):
                LOGGER.debug("add key img {}".format(each))
                self.key_img_list.append(cv2.imread(each))
        self.key_text_list = key_text_list

    def detect(self, detector, frame):
        # return detector.img_match(frame, self.key_img_list) or detector.ocr_match(frame, self.key_text_list)
        return detector.img_match(frame, self.key_img_list)


class ScenarioCtx(object):
    def __init__(self, detector):
        self.scenario_list = []
        self.detector = detector

    def load(self, conf):
        for scenario in conf:
            key_img = cv2.imread(scenario["key_img"]) if "key_img" in scenario else None
            key_text = scenario["key_text"] if "key_text" in scenario else None
            self.register_scenario(Scenario(scenario["name"], key_img, key_text))

    def register_scenario(self, scenario):
        self.scenario_list.append(scenario)

    def detect_scenario(self, frame):
        for scenario in self.scenario_list:
            if scenario.detect(self.detector, frame):
                return scenario

        return None
