from character.character import Character, CharacterClass
from character.skill import Skill


class Champion(Character):
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

    def __init__(self, device, ui_ctx, conf):
        super().__init__(device, ui_ctx, CharacterClass.Champion, conf)
        self.beat_drive = Skill(Champion.BeatDrive, conf["skill"][Champion.BeatDrive])
        self.bone_crusher = Skill(Champion.BoneCrusher, conf["skill"][Champion.BoneCrusher])
        self.continuous_strike = Skill(Champion.ContinuousStrike, conf["skill"][Champion.ContinuousStrike])
        self.rising_fist = Skill(Champion.RisingFist, conf["skill"][Champion.RisingFist])
        self.lightning_dance = Skill(Champion.LightningDance, conf["skill"][Champion.LightningDance])
        self.kihop_low_kick = Skill(Champion.KihopLowKick, conf["skill"][Champion.KihopLowKick])
        self.mountain_pusher = Skill(Champion.MountainPusher, conf["skill"][Champion.MountainPusher])
        self.power_fist = Skill(Champion.PowerFist, conf["skill"][Champion.PowerFist])
        self.seismic_crash = Skill(Champion.SeismicCrash, conf["skill"][Champion.SeismicCrash])
        self.super_armor = Skill(Champion.SuperArmor, conf["skill"][Champion.SuperArmor])
