import math
import os
from dungeonmax.buffs.buff import Buff

class Berserker(Buff):
    NAME = "Berserker"
    IMAGE = os.path.join("graphics", "buffs", f"{NAME}.png")
    DESCRIPTION = "Berserker: Increased melee damage and greatly reduced defense"

    DAMAGE_BOOST_PERCENTAGE = 70
    DEFENSE_MULTIPLIER = 0.5

    def __init__(self, affected, duration):
        super().__init__(affected, self.NAME, duration, self.IMAGE, self.DESCRIPTION)
        self.original_melee_defense = affected.melee_defense
        self.original_ranged_defense = affected.ranged_defense
        self.original_special_defense = affected.special_defense
        self.original_attack = affected.melee_attack

    def effect(self):
        self.affected.melee_attack = math.ceil(self.original_attack + (self.DAMAGE_BOOST_PERCENTAGE / 100) * self.original_attack)
        self.affected.melee_defense = math.ceil(self.original_melee_defense * self.DEFENSE_MULTIPLIER)
        self.affected.ranged_defense = math.ceil(self.original_ranged_defense * self.DEFENSE_MULTIPLIER)
        self.affected.special_defense = math.ceil(self.original_special_defense * self.DEFENSE_MULTIPLIER)

    def wear_off(self):
        self.affected.melee_attack = self.original_attack
        self.affected.melee_defense = self.original_melee_defense
        self.affected.ranged_defense = self.original_ranged_defense
        self.affected.special_defense = self.original_special_defense