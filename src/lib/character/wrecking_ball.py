from src.lib.character.character import Character, CharacterClass
from src.lib.character.skill import Skill


class WreckingBall(Character):
    Destroyer90BunkerBomb = "destroyer_90_bunker_bomb"
    EagleEye = "eagle_eye"
    FireConcentrate = "fire_concentrate"
    FM31GrenadeLauncher = "fm_31_grenade_launcher"
    FM92Stinger = "fm_92_stinger"
    LaserRifle = "laser_rifle"
    QuantumBomb = "quantum_bomb"
    SatelliteBeam = "satellite_beam"
    Shotgun = "shotgun"
    SteyrAMR = "steyr_amr"
    X1Extruder = "x_1_extruder"

    def __init__(self, device, ui_ctx, conf):
        super().__init__(device, ui_ctx, CharacterClass.WreckingBall, conf)
        self.destroyer_90_bunker_bomb = Skill(WreckingBall.Destroyer90BunkerBomb,
                                              conf["skill"][WreckingBall.Destroyer90BunkerBomb])
        self.eagle_eye = Skill(WreckingBall.EagleEye, conf["skill"][WreckingBall.EagleEye])
        self.fire_concentrate = Skill(WreckingBall.FireConcentrate, conf["skill"][WreckingBall.FireConcentrate])
        self.fm_31_grenade_launcher = Skill(WreckingBall.FM31GrenadeLauncher,
                                            conf["skill"][WreckingBall.FM31GrenadeLauncher])
        self.fm_92_stinger = Skill(WreckingBall.FM92Stinger, conf["skill"][WreckingBall.FM92Stinger])
        self.laser_rifle = Skill(WreckingBall.LaserRifle, conf["skill"][WreckingBall.LaserRifle])
        self.quantum_bomb = Skill(WreckingBall.QuantumBomb, conf["skill"][WreckingBall.QuantumBomb])
        self.satellite_beam = Skill(WreckingBall.SatelliteBeam, conf["skill"][WreckingBall.SatelliteBeam])
        self.shotgun = Skill(WreckingBall.Shotgun, conf["skill"][WreckingBall.Shotgun])
        self.steyr_amr = Skill(WreckingBall.SteyrAMR, conf["skill"][WreckingBall.SteyrAMR])
        self.x_1_extruder = Skill(WreckingBall.X1Extruder, conf["skill"][WreckingBall.X1Extruder])
