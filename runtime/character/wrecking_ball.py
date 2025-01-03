# This file is generated by generator.py, do not change this file.
# Change wrecking_ball config in conf/config.yml instead.
from character.character import Character
from runtime.character.character_class import CharacterClass


class WreckingBall(Character):
    Attack = "attack"
    Destroyer90BunkerBomb = "destroyer_90_bunker_bomb"
    EagleEye = "eagle_eye"
    FireConcentrate = "fire_concentrate"
    Fm31GrenadeLauncher = "fm_31_grenade_launcher"
    Fm92Stinger = "fm_92_stinger"
    LaserRifle = "laser_rifle"
    QuantumBomb = "quantum_bomb"
    SatelliteBeam = "satellite_beam"
    Shotgun = "shotgun"
    SteyrAmr = "steyr_amr"
    X1Extruder = "x_1_extruder"
    Railgun = "railgun"

    def __init__(self, device, ui_ctx):
        super().__init__(device, ui_ctx, CharacterClass.WreckingBall)
        self.attack = self.register_skill(
            WreckingBall.Attack,
            {
                "type": "touch",
                "duration": 2.5,
                "cool_down": 0,
                "delay": 0,
                "exec_limit": {"min_distance": 300},
            },
        )
        self.destroyer_90_bunker_bomb = self.register_skill(
            WreckingBall.Destroyer90BunkerBomb,
            {
                "type": "touch",
                "duration": 0.5,
                "cool_down": 1,
                "delay": 0,
                "exec_limit": {"min_distance": 600},
            },
        )
        self.eagle_eye = self.register_skill(
            WreckingBall.EagleEye,
            {
                "type": "swipe_left",
                "coordinate": [1860, 926],
                "duration": 0.1,
                "cool_down": 1,
                "delay": 0,
                "exec_limit": {"min_distance": 0},
            },
        )
        self.fire_concentrate = self.register_skill(
            WreckingBall.FireConcentrate,
            {
                "type": "swipe_right",
                "coordinate": [1860, 926],
                "duration": 0.1,
                "cool_down": 1,
                "delay": 0,
                "exec_limit": {"min_distance": 0},
            },
        )
        self.fm_31_grenade_launcher = self.register_skill(
            WreckingBall.Fm31GrenadeLauncher,
            {
                "type": "touch",
                "duration": 0.1,
                "cool_down": 1,
                "delay": 1,
                "exec_limit": {"min_distance": 600},
            },
        )
        self.fm_92_stinger = self.register_skill(
            WreckingBall.Fm92Stinger,
            {
                "type": "touch",
                "duration": 0.1,
                "cool_down": 1,
                "delay": 0.5,
                "exec_limit": {"min_distance": 500},
            },
        )
        self.laser_rifle = self.register_skill(
            WreckingBall.LaserRifle,
            {
                "type": "touch",
                "duration": 0.6,
                "cool_down": 1,
                "delay": 0,
                "exec_limit": {"min_distance": 80, "vertical_only": True},
            },
        )
        self.quantum_bomb = self.register_skill(
            WreckingBall.QuantumBomb,
            {
                "type": "swipe",
                "coordinate": [1860, 926],
                "duration": 0.1,
                "cool_down": 1,
                "delay": 0,
                "exec_limit": {"min_distance": 0},
            },
        )
        self.satellite_beam = self.register_skill(
            WreckingBall.SatelliteBeam,
            {
                "type": "swipe",
                "coordinate": [1860, 926],
                "duration": 0.1,
                "cool_down": 5,
                "delay": 0,
                "exec_limit": {"min_distance": 250},
            },
        )
        self.shotgun = self.register_skill(
            WreckingBall.Shotgun,
            {
                "type": "touch",
                "duration": 0.1,
                "cool_down": 5,
                "delay": 0,
                "exec_limit": {"min_distance": 250},
            },
        )
        self.steyr_amr = self.register_skill(
            WreckingBall.SteyrAmr,
            {
                "type": "touch",
                "duration": 0.1,
                "cool_down": 5,
                "delay": 0,
                "exec_limit": {"min_distance": 100, "vertical_only": 80},
            },
        )
        self.x_1_extruder = self.register_skill(
            WreckingBall.X1Extruder,
            {
                "type": "touch",
                "duration": 0.1,
                "cool_down": 1,
                "delay": 0,
                "exec_limit": {"min_distance": 600},
            },
        )
        self.railgun = self.register_skill(
            WreckingBall.Railgun,
            {
                "type": "touch",
                "duration": 0.1,
                "cool_down": 0,
                "delay": 0.5,
                "exec_limit": {"min_distance": 80, "vertical_only": True},
            },
        )
