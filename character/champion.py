from character.character import Character, CharacterClass


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
        self.beat_drive = self.register_skill(Champion.BeatDrive, conf["skill"][Champion.BeatDrive])
        self.bone_crusher = self.register_skill(Champion.BoneCrusher, conf["skill"][Champion.BoneCrusher])
        self.continuous_strike = self.register_skill(
            Champion.ContinuousStrike,
            conf["skill"][Champion.ContinuousStrike]
        )
        self.rising_fist = self.register_skill(Champion.RisingFist, conf["skill"][Champion.RisingFist])
        self.lightning_dance = self.register_skill(Champion.LightningDance, conf["skill"][Champion.LightningDance])
        self.kihop_low_kick = self.register_skill(Champion.KihopLowKick, conf["skill"][Champion.KihopLowKick])
        self.mountain_pusher = self.register_skill(Champion.MountainPusher, conf["skill"][Champion.MountainPusher])
        self.power_fist = self.register_skill(Champion.PowerFist, conf["skill"][Champion.PowerFist])
        self.seismic_crash = self.register_skill(Champion.SeismicCrash, conf["skill"][Champion.SeismicCrash])
        self.super_armor = self.register_skill(Champion.SuperArmor, conf["skill"][Champion.SuperArmor])
