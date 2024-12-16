import math
import os
from dungeonmax.buffs.buff import Buff

class MeleeAttackBoost(Buff):
    NAME = "MeleeAttackBoost"
    INCREASE_IMAGE = os.path.join("graphics", "buffs", f"MeleeDefenseBoost.png")
    DECREASE_IMAGE = os.path.join("graphics", "buffs", f"MeleeDefenseBoost.png")
    DESCRIPTION = "Melee Attack Boost: By {boost_amount}"

    def __init__(self, affected, duration, boost_amount):
        self.DESCRIPTION = self.DESCRIPTION.format(boost_amount=boost_amount)
        if boost_amount < 0:
            super().__init__(affected, self.NAME, duration, self.DECREASE_IMAGE, self.DESCRIPTION)
        else:
            super().__init__(affected, self.NAME, duration, self.INCREASE_IMAGE, self.DESCRIPTION)
        self.original_attack = affected.melee_attack
        self.boost_amount = boost_amount

    def effect(self):
        self.affected.melee_attack = math.ceil(self.original_attack + self.boost_amount)

    def wear_off(self):
        self.affected.melee_attack = self.original_attack