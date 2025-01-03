# This file is generated by generator.py, do not change this file.
# Change champion config in conf/config.yml instead.
from character.character import Character
from runtime.character.character_class import CharacterClass


class Champion(Character):
    Attack = "attack"
    BeatDrive = "beat_drive"
    BoneCrusher = "bone_crusher"
    ContinuousStrike = "continuous_strike"
    RisingFist = "rising_fist"
    LightningDance = "lightning_dance"
    KihopLowKick = "kihop_low_kick"
    MountainPusher = "mountain_pusher"
    PowerFist = "power_fist"
    SeismicCrash = "seismic_crash"
    SuperArmor = "super_armor"

    def __init__(self, device, ui_ctx):
        super().__init__(device, ui_ctx, CharacterClass.Champion)
        self.attack = self.register_skill(
            Champion.Attack,
            {
                "type": "touch",
                "duration": 1,
                "cool_down": 0,
                "exec_limit": {"min_distance": 300},
            },
        )
        self.beat_drive = self.register_skill(
            Champion.BeatDrive,
            {
                "type": "swipe_down",
                "coordinate": [1860, 926],
                "duration": 0.1,
                "cool_down": 1,
                "exec_limit": {"min_distance": 250},
            },
        )
        self.bone_crusher = self.register_skill(
            Champion.BoneCrusher,
            {
                "type": "touch",
                "duration": 0.1,
                "cool_down": 7,
                "delay": 0.1,
                "exec_limit": {"min_distance": 250},
            },
        )
        self.continuous_strike = self.register_skill(
            Champion.ContinuousStrike,
            {
                "type": "touch",
                "duration": 0.1,
                "cool_down": 1,
                "exec_limit": {"min_distance": 250},
            },
        )
        self.rising_fist = self.register_skill(
            Champion.RisingFist,
            {
                "type": "swipe_up",
                "coordinate": [1860, 926],
                "duration": 0.1,
                "cool_down": 1,
                "delay": 0.35,
                "exec_limit": {"min_distance": 250},
            },
        )
        self.lightning_dance = self.register_skill(
            Champion.LightningDance,
            {
                "type": "touch",
                "duration": 0.1,
                "cool_down": 1,
                "delay": 1,
                "exec_limit": {"min_distance": 10},
            },
        )
        self.kihop_low_kick = self.register_skill(
            Champion.KihopLowKick,
            {
                "type": "touch",
                "duration": 0.1,
                "cool_down": 1,
                "exec_limit": {"min_distance": 300},
            },
        )
        self.mountain_pusher = self.register_skill(
            Champion.MountainPusher,
            {
                "type": "touch",
                "duration": 0.1,
                "cool_down": 1,
                "exec_limit": {"min_distance": 300},
            },
        )
        self.power_fist = self.register_skill(
            Champion.PowerFist,
            {
                "type": "swipe_right",
                "coordinate": [1860, 926],
                "duration": 1,
                "cool_down": 1,
                "exec_limit": {"min_distance": 0},
            },
        )
        self.seismic_crash = self.register_skill(
            Champion.SeismicCrash,
            {
                "type": "touch",
                "duration": 0.1,
                "cool_down": 6,
                "exec_limit": {"min_distance": 300},
            },
        )
        self.super_armor = self.register_skill(
            Champion.SuperArmor,
            {
                "type": "swipe_left",
                "coordinate": [1860, 926],
                "duration": 0.1,
                "cool_down": 1,
                "exec_limit": {"min_distance": 0},
            },
        )
