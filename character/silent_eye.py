from character.character import Character, CharacterClass
from character.skill import Skill


class SilentEye(Character):
    AgniPentacle = "agni_pentacle"
    DeadlyEnticer = "deadly_enticer"
    FireWaveSword = "fire_wave_sword"
    ForceWaveNeutral = "force_wave_neutral"
    GhostOrb = "ghost_orb"
    GroundQuaker = "ground_quaker"
    IceWaveSword = "ice_wave_sword"
    MurderousWave = "murderous_wave"
    SpiritCrescent = "spirit_crescent"
    WaveEye = "wave_eye"
    WaveRadiation = "wave_radiation"

    def __init__(self, device, ui_ctx, conf):
        super().__init__(device, ui_ctx, CharacterClass.SilentEye, conf)
        self.agni_pentacle = Skill(SilentEye.AgniPentacle, conf["skill"][SilentEye.AgniPentacle])
        self.deadly_enticer = Skill(SilentEye.DeadlyEnticer, conf["skill"][SilentEye.DeadlyEnticer])
        self.fire_wave_sword = Skill(SilentEye.FireWaveSword, conf["skill"][SilentEye.FireWaveSword])
        self.force_wave_neutral = Skill(SilentEye.ForceWaveNeutral, conf["skill"][SilentEye.ForceWaveNeutral])
        self.ghost_orb = Skill(SilentEye.GhostOrb, conf["skill"][SilentEye.GhostOrb])
        self.ground_quaker = Skill(SilentEye.GroundQuaker, conf["skill"][SilentEye.GroundQuaker])
        self.ice_wave_sword = Skill(SilentEye.IceWaveSword, conf["skill"][SilentEye.IceWaveSword])
        self.murderous_wave = Skill(SilentEye.MurderousWave, conf["skill"][SilentEye.MurderousWave])
        self.spirit_crescent = Skill(SilentEye.SpiritCrescent, conf["skill"][SilentEye.SpiritCrescent])
        self.wave_eye = Skill(SilentEye.WaveEye, conf["skill"][SilentEye.WaveEye])
        self.wave_radiation = Skill(SilentEye.WaveRadiation, conf["skill"][SilentEye.WaveRadiation])
