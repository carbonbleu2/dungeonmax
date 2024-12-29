from dungeonmax.weapons.bows import *
from dungeonmax.weapons.swords import *

class EquipmentManager:
    def __init__(self, weapons_list, skills):
        self.weapons_list = weapons_list
        self.weapon_names = set([weapon.name for weapon in weapons_list])

        self.skills = skills
        self.skill_names = set([skill.name for skill in skills])

        self.weapon_idx = 0
        self.skill_idx = 0

    def add_weapon(self, weapon):
        if not self.has_skill(weapon.name):
            self.weapons_list.append(weapon)
            self.weapon_names.add(weapon.name)

    def remove_weapon(self, weapon):
        if self.has_weapon(weapon.name):
            self.weapons_list.remove(weapon)
            self.weapon_names.remove(weapon.name)
            self.weapon_idx = 0

    def add_skill(self, skill):
        if not self.has_skill(skill.name):
            self.skills.append(skill)
            self.skill_names.add(skill.name)

    def remove_skill(self, skill):
        if self.has_skill(skill.name):
            self.skills.remove(skill)
            self.skill_names.remove(skill.name)
            self.skill_idx = 0


    def has_weapon(self, weapon_name):
        return weapon_name in self.weapon_names

    def get_weapon(self):
        return self.weapons_list[self.weapon_idx]
    
    def has_skill(self, skill_name):
        return skill_name in self.skill_names
    
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

    def change_current_skill_to(self, skill):
        for my_skill in self.skills:
            if my_skill == skill:
                self.skill_idx = self.skills.index(skill)
                return