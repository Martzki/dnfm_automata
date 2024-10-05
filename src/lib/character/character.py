import time
from math import sin, cos, radians

from src.common.log import Logger
from src.lib.character.skill import Skill, SkillType
from src.lib.dungeon.battle import BattleMetadata
from src.lib.ui.ui import UIElementCtx

LOGGER = Logger(__name__).logger

DEFAULT_SWIPE_DISTANCE = 200
DEFAULT_MOVE_LENGTH = 150


class CharacterClass(object):
    Unknown = "Unknown"
    Evangelist = "Evangelist"
    HellBringer = "HellBringer"
    Trickster = "Trickster"
    class_map = {"Evangelist": Evangelist, "HellBringer": HellBringer, "Trickster": Trickster}

    @classmethod
    def from_str(cls, class_str):
        return cls.class_map.get(class_str, cls.Unknown)


class Character(object):
    def __init__(self, device, ui_ctx, character_class, conf):
        self.device = device
        self.ui_ctx = ui_ctx
        self.character_class = CharacterClass.from_str(character_class)
        self.attack = Skill("attack", conf["skill"]["attack"])

    def move_with_rad(self, rad, duration=1, need_stop=None):
        center = self.ui_ctx.get_ui_coordinate(UIElementCtx.CategoryBase, "move")
        if not center:
            LOGGER.critical("Failed to get move coordinate.")
            return False

        coordinate = (
            center[0] + DEFAULT_MOVE_LENGTH * cos(rad),
            center[1] - DEFAULT_MOVE_LENGTH * sin(rad)
        )

        start = time.time()
        self.device.raw_touch(coordinate, press=True)

        stop = False
        while True:
            if need_stop and need_stop():
                stop = True
                break

            if time.time() - start > duration:
                break

        self.device.raw_touch(coordinate, press=False)

        return stop

    def move(self, angle, duration=1, need_stop=None):
        return self.move_with_rad(radians(angle), duration, need_stop)

    def move_toward(self, src, dst, need_stop=None):
        distance = BattleMetadata.get_distance(src, dst)
        duration = BattleMetadata.get_move_duration(distance)
        LOGGER.info(f"move({src}, {dst}, {duration})")
        return self.move_with_rad(BattleMetadata.get_rad(src, dst), duration, need_stop)

    def get_skill(self, skill_name):
        skill = getattr(self, skill_name, None)
        assert skill is not None, "skill {} is not found".format(skill_name)
        return skill

    def exec_skill(self, skill, duration=None, delay=None):
        coordinate = self.ui_ctx.get_skill_coordinate(self.character_class, skill.name)
        if not coordinate:
            LOGGER.error("Failed to get coordinate for {}.{}".format(self.character_class, skill.name))
            return

        if not duration:
            duration = skill.duration

        if not delay:
            delay = skill.delay

        LOGGER.info(f"Exec {skill} with {coordinate} {duration} {delay}")

        if skill.type == SkillType.Touch:
            self.device.touch(coordinate, duration)
        elif skill.type == SkillType.SwipeLeft:
            self.device.swipe(coordinate, (coordinate[0] - DEFAULT_SWIPE_DISTANCE, coordinate[1]))
        elif skill.type == SkillType.SwipeRight:
            self.device.swipe(coordinate, (coordinate[0] + DEFAULT_SWIPE_DISTANCE, coordinate[1]))
        elif skill.type == SkillType.SwipeUp:
            self.device.swipe(coordinate, (coordinate[0], coordinate[1] - DEFAULT_SWIPE_DISTANCE))
        elif skill.type == SkillType.SwipeDown:
            self.device.swipe(coordinate, (coordinate[0], coordinate[1] + DEFAULT_SWIPE_DISTANCE))
        else:
            LOGGER.error("Invalid skill: {}".format(skill))

        time.sleep(delay)

        skill.last_exec_time = time.time()

    def wait_skill_cool_down(self, skill):
        delta = time.time() - skill.last_exec_time
        if delta < skill.cool_down:
            time.sleep(skill.cool_down - delta + 1.5)
