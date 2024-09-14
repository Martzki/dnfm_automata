from src.lib.character.character import Character, CharacterClass
from src.lib.character.skill import Skill


class Evangelist(Character):
    ChristeningLight = "christening_light"
    CruxOfVictoria = "crux_of_victoria"
    GrandCrashingCross = "grand_crashing_cross"
    PurifyingLightning = "purifying_lightning"
    SaintWall = "saint_wall"
    ShiningCross = "shining_cross"
    SpearOfVictory = "spear_of_victory"
    ValiantAria = "valiant_aria"

    def __init__(self, device, ui_ctx, conf):
        super().__init__(device, ui_ctx, CharacterClass.Evangelist, conf)
        self.christening_light = Skill(Evangelist.ChristeningLight, conf["skill"][Evangelist.ChristeningLight])
        self.crux_of_victoria = Skill(Evangelist.CruxOfVictoria, conf["skill"][Evangelist.CruxOfVictoria])
        self.grand_crashing_cross = Skill(Evangelist.GrandCrashingCross, conf["skill"][Evangelist.GrandCrashingCross])
        self.purifying_lightning = Skill(Evangelist.PurifyingLightning, conf["skill"][Evangelist.PurifyingLightning])
        self.spear_of_victory = Skill(Evangelist.SpearOfVictory, conf["skill"][Evangelist.SpearOfVictory])
        self.saint_wall = Skill(Evangelist.SaintWall, conf["skill"][Evangelist.SaintWall])
        self.shining_cross = Skill(Evangelist.ShiningCross, conf["skill"][Evangelist.ShiningCross])
        self.valiant_aria = Skill(Evangelist.ValiantAria, conf["skill"][Evangelist.ValiantAria])
