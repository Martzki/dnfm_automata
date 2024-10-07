import time


class SkillStrategy(object):
    def __init__(self, skill, pre_attack_duration, priority):
        self.skill = skill
        self.pre_attack_duration = pre_attack_duration
        self.priority = priority


class BattleStrategy(object):
    def __init__(self):
        self.skill_strategy_list = []

    def register_skill(self, skill, priority, pre_attack_duration=0):
        self.skill_strategy_list.append(SkillStrategy(skill, pre_attack_duration, priority))
        self.skill_strategy_list = sorted(self.skill_strategy_list, key=lambda x: x.priority)

    def get_next_skill(self, character):
        for skill_strategy in self.skill_strategy_list:
            skill = getattr(character, skill_strategy.skill, None)
            if skill and skill.is_cool_down():
                return skill

        return None
