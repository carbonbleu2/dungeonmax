import math
import os
from dungeonmax.buffs.buff import Buff

class MeleeDefenseBoost(Buff):
    NAME = "MeleeDefenseBoost"
    IMAGE = os.path.join("graphics", "buffs", f"{NAME}.png")
    DESCRIPTION = "Melee Defense Boost: By {boost_amount}"

    def __init__(self, affected, duration, boost_amount):
        self.DESCRIPTION = self.DESCRIPTION.format(boost_amount=boost_amount)
        super().__init__(affected, self.NAME, duration, self.IMAGE, self.DESCRIPTION)
        self.original_defense = affected.melee_defense
        self.boost_amount = boost_amount

    def effect(self):
        self.affected.melee_defense = math.ceil(self.original_defense + self.boost_amount)

        return 0, None

    def wear_off(self):
        self.affected.melee_defense = self.original_defense