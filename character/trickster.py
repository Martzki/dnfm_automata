from character.character import Character, CharacterClass


class Trickster(Character):
    AcidRain = "acid_rain"
    CheekyDollShururu = "cheeky_doll_shururu"
    EnhancedMagicMissile = "enhanced_magic_missile"
    FusionCraft = "fusion_craft"
    Gravitas = "gravitas"
    LavaPotionNo9 = "lava_potion_no_9"
    Lollipop = "lollipop"
    Showtime = "showtime"
    SnowMan = "snow_man"

    def __init__(self, device, ui_ctx, conf):
        super().__init__(device, ui_ctx, CharacterClass.Trickster, conf)
        self.acid_rain = self.register_skill(Trickster.AcidRain, conf["skill"][Trickster.AcidRain])
        self.cheeky_doll_shururu = self.register_skill(
            Trickster.CheekyDollShururu,
            conf["skill"][Trickster.CheekyDollShururu]
        )
        self.enhanced_magic_missile = self.register_skill(
            Trickster.EnhancedMagicMissile,
            conf["skill"][Trickster.EnhancedMagicMissile]
        )
        self.fusion_craft = self.register_skill(Trickster.FusionCraft, conf["skill"][Trickster.FusionCraft])
        self.gravitas = self.register_skill(Trickster.Gravitas, conf["skill"][Trickster.Gravitas])
        self.lava_potion_no_9 = self.register_skill(Trickster.LavaPotionNo9, conf["skill"][Trickster.LavaPotionNo9])
        self.lollipop = self.register_skill(Trickster.Lollipop, conf["skill"][Trickster.Lollipop])
        self.showtime = self.register_skill(Trickster.Showtime, conf["skill"][Trickster.Showtime])
        self.snow_man = self.register_skill(Trickster.Showtime, conf["skill"][Trickster.SnowMan])
