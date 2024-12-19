import math
import os
from dungeonmax.buffs.buff import Buff

class TrogsCurse(Buff):
    NAME = "TrogsCurse"
    IMAGE = os.path.join("graphics", "buffs", f"{NAME}.png")
    DESCRIPTION = "Trog's Curse: Melee damage permanently reduced by 75%"

    MELEE_ATTACK_DIP_PERCENTAGE = 75
    DURATION = -1

    def __init__(self, affected):
        super().__init__(affected, self.NAME, -1, self.IMAGE, self.DESCRIPTION)
        self.original_melee_attack = affected.melee_attack

    def effect(self):
        self.affected.melee_attack = math.ceil(self.original_melee_attack - 
                                    (self.MELEE_ATTACK_DIP_PERCENTAGE / 100) * self.original_melee_attack)

    def wear_off(self):
        self.affected.melee_attack = self.original_melee_attack