import time
from math import sin, cos, radians

from character.skill import Skill, SkillType
from common.log import Logger
from dungeon.battle import BattleMetadata
from runtime.ui import ui_elements
from ui.ui import UIElement

LOGGER = Logger(__name__).logger

DEFAULT_SWIPE_DISTANCE = 350
DEFAULT_MOVE_LENGTH = 150


class Character(object):
    def __init__(self, device, ui_ctx, character_class):
        self.device = device
        self.ui_ctx = ui_ctx
        self.character_class = character_class
        self.reserve_fatigue_points = 0

    def register_skill(self, name, conf):
        if "coordinate" not in conf:
            path = self.ui_ctx.base_dir / UIElement.CategorySkill / self.character_class
            self.ui_ctx.register_dynamic_ui_elements(path, f"{UIElement.CategorySkill}.{self.character_class}")
        else:
            self.ui_ctx.register_ui_element(
                f"{UIElement.CategorySkill}.{self.character_class}.{name}",
                UIElement(coordinate=conf["coordinate"])
            )
        return Skill(name, conf)

    def move_with_rad(self, rad, duration=1, move_check=None):
        center = self.ui_ctx.get_ui_coordinate(ui_elements.Common.Move)
        if not center:
            LOGGER.critical("Failed to get move coordinate.")
            return False

        coordinate = (
            center[0] + DEFAULT_MOVE_LENGTH * cos(rad),
            center[1] - DEFAULT_MOVE_LENGTH * sin(rad)
        )

        start = time.time()
        self.device.raw_touch(coordinate, press=True)

        try:
            while True:
                if move_check:
                    move_check()

                if time.time() - start > duration:
                    break
        finally:
            self.device.raw_touch(coordinate, press=False)

    def move(self, angle, duration=1, move_check=None):
        self.move_with_rad(radians(angle), duration, move_check)

    def move_toward(self, src, dst, move_check=None):
        distance = BattleMetadata.get_distance(src, dst)
        duration = BattleMetadata.get_move_duration(distance)
        LOGGER.info(f"move({src}, {dst}, {duration})")
        self.move_with_rad(BattleMetadata.get_rad(src, dst), duration, move_check)

    def get_skill(self, skill_name):
        skill = getattr(self, skill_name, None)
        assert skill is not None, "skill {} is not found".format(skill_name)
        return skill

    def exec_skill(self, skill, duration=None, delay=None, swipe_angle=None):
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
        elif skill.type == SkillType.Swipe:
            if swipe_angle:
                rad = radians(swipe_angle)
                dst = (
                    coordinate[0] + DEFAULT_SWIPE_DISTANCE * cos(rad),
                    coordinate[1] - DEFAULT_SWIPE_DISTANCE * sin(rad)
                )
                self.device.swipe(coordinate, dst)
            else:
                LOGGER.warning(f"Swipe skill: {skill} has no angle, use touch instead")
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
