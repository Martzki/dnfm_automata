import time


class SkillType(object):
    Touch = 0
    SwipeLeft = 1
    SwipeRight = 2
    SwipeUp = 3
    SwipeDown = 4
    type_map = {
        "touch": Touch,
        "swipe_left": SwipeLeft,
        "swipe_right": SwipeRight,
        "swipe_up": SwipeUp,
        "swipe_down": SwipeDown,
    }

    @classmethod
    def from_str(cls, type_str):
        return cls.type_map.get(type_str, cls.Touch)


class ExecLimit(object):
    def __init__(self, min_distance=0, vertical_only=False):
        self.min_distance = min_distance
        self.vertical_only = vertical_only


class Skill(object):
    def __init__(self, name, conf):
        self.name = name
        self.type = SkillType.from_str(conf.get("type", "touch"))
        self.duration = conf.get("duration", 1)
        self.delay = conf.get("delay", 0)
        self.cool_down = conf.get("cool_down", 1)
        self.last_exec_time = time.time()
        self.exec_limit = ExecLimit(**conf["exec_limit"])

    def __repr__(self):
        return f"Skill({self.name}, {self.type}, {self.duration}, {self.cool_down})"

    def is_cool_down(self):
        return time.time() - self.last_exec_time > self.cool_down
