from character.character import Character, CharacterClass
from character.skill import Skill


class Noblesse(Character):
    ArcaneSwordBlast = "arcane_sword_blast"
    Ascent = "ascent"
    Crescent = "crescent"
    ElementalShift = "elemental_shift"
    Flash = "flash"
    IllusionSword = "illusion_sword"
    SentimentDuFerCritical = "sentiment_du_fer_critical"
    SwiftDemonSlash = "swift_demon_slash"
    SwiftSword = "swift_sword"
    TossingSlash = "tossing_slash"
    UltimateSlayerTechniqueSpacetimeCutter = "ultimate_slayer_technique_spacetime_cutter"

    def __init__(self, device, ui_ctx, conf):
        super().__init__(device, ui_ctx, CharacterClass.Noblesse, conf)
        self.arcane_sword_blast = Skill(Noblesse.ArcaneSwordBlast, conf["skill"][Noblesse.ArcaneSwordBlast])
        self.ascent = Skill(Noblesse.Ascent, conf["skill"][Noblesse.Ascent])
        self.crescent = Skill(Noblesse.Crescent, conf["skill"][Noblesse.Crescent])
        self.elemental_shift = Skill(Noblesse.ElementalShift, conf["skill"][Noblesse.ElementalShift])
        self.flash = Skill(Noblesse.Flash, conf["skill"][Noblesse.Flash])
        self.illusion_sword = Skill(Noblesse.IllusionSword, conf["skill"][Noblesse.IllusionSword])
        self.sentiment_du_fer_critical = Skill(Noblesse.SentimentDuFerCritical,
                                               conf["skill"][Noblesse.SentimentDuFerCritical])
        self.swift_demon_slash = Skill(Noblesse.SwiftDemonSlash, conf["skill"][Noblesse.SwiftDemonSlash])
        self.swift_sword = Skill(Noblesse.SwiftSword, conf["skill"][Noblesse.SwiftSword])
        self.tossing_slash = Skill(Noblesse.TossingSlash, conf["skill"][Noblesse.TossingSlash])
        self.ultimate_slayer_technique_spacetime_cutter = (
            Skill(Noblesse.UltimateSlayerTechniqueSpacetimeCutter,
                  conf["skill"][Noblesse.UltimateSlayerTechniqueSpacetimeCutter])
        )
