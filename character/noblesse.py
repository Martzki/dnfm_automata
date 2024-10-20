from character.character import Character, CharacterClass


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
        self.arcane_sword_blast = self.register_skill(
            Noblesse.ArcaneSwordBlast,
            conf["skill"][Noblesse.ArcaneSwordBlast]
        )
        self.ascent = self.register_skill(Noblesse.Ascent, conf["skill"][Noblesse.Ascent])
        self.crescent = self.register_skill(Noblesse.Crescent, conf["skill"][Noblesse.Crescent])
        self.elemental_shift = self.register_skill(Noblesse.ElementalShift, conf["skill"][Noblesse.ElementalShift])
        self.flash = self.register_skill(Noblesse.Flash, conf["skill"][Noblesse.Flash])
        self.illusion_sword = self.register_skill(Noblesse.IllusionSword, conf["skill"][Noblesse.IllusionSword])
        self.sentiment_du_fer_critical = self.register_skill(
            Noblesse.SentimentDuFerCritical,
            conf["skill"][Noblesse.SentimentDuFerCritical]
        )
        self.swift_demon_slash = self.register_skill(Noblesse.SwiftDemonSlash, conf["skill"][Noblesse.SwiftDemonSlash])
        self.swift_sword = self.register_skill(Noblesse.SwiftSword, conf["skill"][Noblesse.SwiftSword])
        self.tossing_slash = self.register_skill(Noblesse.TossingSlash, conf["skill"][Noblesse.TossingSlash])
        self.ultimate_slayer_technique_spacetime_cutter = self.register_skill(
            Noblesse.UltimateSlayerTechniqueSpacetimeCutter,
            conf["skill"][Noblesse.UltimateSlayerTechniqueSpacetimeCutter]
        )
