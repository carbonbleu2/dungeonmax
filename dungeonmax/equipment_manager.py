from dungeonmax.weapons.bows import RecruitsBow
from dungeonmax.weapons.swords import RecruitsSword

class EquipmentManager:
    def __init__(self, weapons_list, skills):
        self.weapons_list = weapons_list
        self.skills = skills
        self.weapon_idx = 0
        self.skill_idx = 0

    def add_weapon(self, weapon):
        self.weapons_list.append(weapon)

    def add_skill(self, skill):
        self.skills.append(skill)

    def get_weapon(self):
        return self.weapons_list[self.weapon_idx]
    
    def get_skill(self):
        return self.skills[self.skill_idx]
    
    def next_weapon(self):
        self.weapon_idx += 1
        if self.weapon_idx == len(self.weapons_list):
            self.weapon_idx = 0

    def previous_weapon(self):
        self.weapon_idx -= 1
        if self.weapon_idx == -1:
            self.weapon_idx = len(self.weapons_list) - 1

    def next_skill(self):
        self.skill_idx += 1
        if self.skill_idx == len(self.skills):
            self.skill_idx = 0

    def previous_skill(self):
        self.skill_idx -= 1
        if self.skill_idx == -1:
            self.skill_idx = len(self.skills) - 1