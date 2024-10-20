from character.character import Character, CharacterClass


class HellBringer(Character):
    Bloodlust = "bloodlust"
    BloodSword = "blood_sword"
    BloodyTwister = "bloody_twister"
    Derange = "derange"
    Enrage = "enrage"
    ExtremeOverkill = "extreme_overkill"
    GoreCross = "gore_cross"
    MountainousWheel = "mountainous_wheel"
    OutrageBreak = "outrage_break"
    RagingFury = "raging_fury"
    Thirst = "thirst"

    def __init__(self, device, ui_ctx, conf):
        super().__init__(device, ui_ctx, CharacterClass.HellBringer, conf)
        self.bloodlust = self.register_skill(HellBringer.Bloodlust, conf["skill"][HellBringer.Bloodlust])
        self.blood_sword = self.register_skill(HellBringer.BloodSword, conf["skill"][HellBringer.BloodSword])
        self.bloody_twister = self.register_skill(HellBringer.BloodyTwister, conf["skill"][HellBringer.BloodyTwister])
        self.derange = self.register_skill(HellBringer.Derange, conf["skill"][HellBringer.Derange])
        self.enrage = self.register_skill(HellBringer.Enrage, conf["skill"][HellBringer.Enrage])
        self.extreme_overkill = self.register_skill(
            HellBringer.ExtremeOverkill,
            conf["skill"][HellBringer.ExtremeOverkill]
        )
        self.gore_cross = self.register_skill(HellBringer.GoreCross, conf["skill"][HellBringer.GoreCross])
        self.mountainous_wheel = self.register_skill(
            HellBringer.MountainousWheel,
            conf["skill"][HellBringer.MountainousWheel]
        )
        self.outrage_break = self.register_skill(HellBringer.OutrageBreak, conf["skill"][HellBringer.OutrageBreak])
        self.raging_fury = self.register_skill(HellBringer.RagingFury, conf["skill"][HellBringer.RagingFury])
        self.thirst = self.register_skill(HellBringer.Thirst, conf["skill"][HellBringer.Thirst])
