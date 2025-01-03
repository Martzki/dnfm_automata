# This file is generated by generator.py, do not change this file.
# Change grand_master config in conf/config.yml instead.
from character.character import Character
from runtime.character.character_class import CharacterClass


class GrandMaster(Character):
    Attack = "attack"
    Overdrive = "overdrive"
    ChargeCrash = "charge_crash"
    ChargeBurst = "charge_burst"
    IllusionSwordDance = "illusion_sword_dance"
    DrawSword = "draw_sword"
    UltimateSlayTempest = "ultimate_slay_tempest"
    OmnislayShootingStar = "omnislay_shooting_star"
    FlowingStanceSwift = "flowing_stance_swift"
    ContinuousSlash = "continuous_slash"
    RagingDragonSlash = "raging_dragon_slash"

    def __init__(self, device, ui_ctx):
        super().__init__(device, ui_ctx, CharacterClass.GrandMaster)
        self.attack = self.register_skill(
            GrandMaster.Attack,
            {
                "type": "touch",
                "duration": 2,
                "cool_down": 0,
                "delay": 0,
                "exec_limit": {"min_distance": 300},
            },
        )
        self.overdrive = self.register_skill(
            GrandMaster.Overdrive,
            {
                "type": "swipe_right",
                "coordinate": [1860, 926],
                "duration": 0.1,
                "cool_down": 0,
                "delay": 0,
                "exec_limit": {"min_distance": 0},
            },
        )
        self.charge_crash = self.register_skill(
            GrandMaster.ChargeCrash,
            {
                "type": "touch",
                "duration": 1,
                "cool_down": 0,
                "delay": 0,
                "exec_limit": {"min_distance": 300},
            },
        )
        self.charge_burst = self.register_skill(
            GrandMaster.ChargeBurst,
            {
                "type": "touch",
                "duration": 1.5,
                "cool_down": 0,
                "delay": 0,
                "exec_limit": {"min_distance": 300},
            },
        )
        self.illusion_sword_dance = self.register_skill(
            GrandMaster.IllusionSwordDance,
            {
                "type": "swipe_down",
                "coordinate": [1860, 926],
                "duration": 0.1,
                "cool_down": 0,
                "delay": 3,
                "exec_limit": {"min_distance": 300},
            },
        )
        self.draw_sword = self.register_skill(
            GrandMaster.DrawSword,
            {
                "type": "touch",
                "duration": 1,
                "cool_down": 0,
                "delay": 0,
                "exec_limit": {"min_distance": 700},
            },
        )
        self.ultimate_slay_tempest = self.register_skill(
            GrandMaster.UltimateSlayTempest,
            {
                "type": "touch",
                "duration": 5,
                "cool_down": 0,
                "delay": 0,
                "exec_limit": {"min_distance": 700},
            },
        )
        self.omnislay_shooting_star = self.register_skill(
            GrandMaster.OmnislayShootingStar,
            {
                "type": "touch",
                "duration": 0.1,
                "cool_down": 0,
                "delay": 0,
                "exec_limit": {"min_distance": 300},
            },
        )
        self.flowing_stance_swift = self.register_skill(
            GrandMaster.FlowingStanceSwift,
            {
                "type": "touch",
                "duration": 0.5,
                "cool_down": 0,
                "delay": 0,
                "exec_limit": {"min_distance": 500},
            },
        )
        self.continuous_slash = self.register_skill(
            GrandMaster.ContinuousSlash,
            {
                "type": "touch",
                "duration": 0.1,
                "cool_down": 0,
                "delay": 0,
                "exec_limit": {"min_distance": 300},
            },
        )
        self.raging_dragon_slash = self.register_skill(
            GrandMaster.RagingDragonSlash,
            {
                "type": "touch",
                "duration": 0.1,
                "cool_down": 0,
                "delay": 0,
                "exec_limit": {"min_distance": 1000},
            },
        )
