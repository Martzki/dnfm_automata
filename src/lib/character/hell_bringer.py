from src.lib.character.character import Character, CharacterClass
from src.lib.character.skill import Skill


class HellBringer(Character):
    BloodSword = "blood_sword"
    BloodyTwister = "bloody_twister"
    Derange = "derange"
    Enrage = "enrage"
    ExtremeOverkill = "extreme_overkill"
    MountainousWheel = "mountainous_wheel"
    OutrageBreak = "outrage_break"
    RagingFury = "raging_fury"
    Thirst = "thirst"

    def __init__(self, device, ui_ctx, conf):
        super().__init__(device, ui_ctx, CharacterClass.HellBringer, conf)
        self.blood_sword = Skill(HellBringer.BloodSword, conf["skill"][HellBringer.BloodSword])
        self.bloody_twister = Skill(HellBringer.BloodyTwister, conf["skill"][HellBringer.BloodyTwister])
        self.derange = Skill(HellBringer.Derange, conf["skill"][HellBringer.Derange])
        self.enrage = Skill(HellBringer.Enrage, conf["skill"][HellBringer.Enrage])
        self.extreme_overkill = Skill(HellBringer.ExtremeOverkill, conf["skill"][HellBringer.ExtremeOverkill])
        self.mountainous_wheel = Skill(HellBringer.MountainousWheel, conf["skill"][HellBringer.MountainousWheel])
        self.outrage_break = Skill(HellBringer.OutrageBreak, conf["skill"][HellBringer.OutrageBreak])
        self.raging_fury = Skill(HellBringer.RagingFury, conf["skill"][HellBringer.RagingFury])
        self.thirst = Skill(HellBringer.Thirst, conf["skill"][HellBringer.Thirst])
