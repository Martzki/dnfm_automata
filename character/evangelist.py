from character.character import Character, CharacterClass


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
        self.christening_light = self.register_skill(
            Evangelist.ChristeningLight,
            conf["skill"][Evangelist.ChristeningLight]
        )
        self.crux_of_victoria = self.register_skill(Evangelist.CruxOfVictoria, conf["skill"][Evangelist.CruxOfVictoria])
        self.grand_crashing_cross = self.register_skill(
            Evangelist.GrandCrashingCross,
            conf["skill"][Evangelist.GrandCrashingCross]
        )
        self.purifying_lightning = self.register_skill(
            Evangelist.PurifyingLightning,
            conf["skill"][Evangelist.PurifyingLightning]
        )
        self.spear_of_victory = self.register_skill(Evangelist.SpearOfVictory, conf["skill"][Evangelist.SpearOfVictory])
        self.saint_wall = self.register_skill(Evangelist.SaintWall, conf["skill"][Evangelist.SaintWall])
        self.shining_cross = self.register_skill(Evangelist.ShiningCross, conf["skill"][Evangelist.ShiningCross])
        self.valiant_aria = self.register_skill(Evangelist.ValiantAria, conf["skill"][Evangelist.ValiantAria])
