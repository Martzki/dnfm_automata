from src.lib.character.character import Character, CharacterClass
from src.lib.character.skill import Skill


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
        self.acid_rain = Skill(Trickster.AcidRain, conf["skill"][Trickster.AcidRain])
        self.cheeky_doll_shururu = Skill(Trickster.CheekyDollShururu, conf["skill"][Trickster.CheekyDollShururu])
        self.enhanced_magic_missile = Skill(Trickster.EnhancedMagicMissile,
                                            conf["skill"][Trickster.EnhancedMagicMissile])
        self.fusion_craft = Skill(Trickster.FusionCraft, conf["skill"][Trickster.FusionCraft])
        self.gravitas = Skill(Trickster.Gravitas, conf["skill"][Trickster.Gravitas])
        self.lava_potion_no_9 = Skill(Trickster.LavaPotionNo9, conf["skill"][Trickster.LavaPotionNo9])
        self.lollipop = Skill(Trickster.Lollipop, conf["skill"][Trickster.Lollipop])
        self.showtime = Skill(Trickster.Showtime, conf["skill"][Trickster.Showtime])
        self.snow_man = Skill(Trickster.Showtime, conf["skill"][Trickster.SnowMan])

