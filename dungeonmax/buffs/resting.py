import math
import os
from dungeonmax.buffs.buff import Buff
from dungeonmax.settings import FPS

class Resting(Buff):
    NAME = "Resting"
    IMAGE = os.path.join("graphics", "buffs", f"{NAME}.png")
    DESCRIPTION = "Resting: For {health_regen} HP/s and {energy_regen} EP/s"

    def __init__(self, affected):
        self.DESCRIPTION = self.DESCRIPTION.format(
            health_regen=round(affected.health_regen_rate * FPS, 2), 
            energy_regen=round(affected.energy_regen_rate * FPS, 2)
        )
        super().__init__(affected, self.NAME, -1, self.IMAGE, self.DESCRIPTION)

    def effect(self):
        self.affected.health += self.affected.health_regen_rate
        if self.affected.health >= self.affected.max_hp:
            self.affected.health = self.affected.max_hp
        self.affected.energy += self.affected.energy_regen_rate
        if self.affected.energy >= self.affected.max_ep:
            self.affected.energy = self.affected.max_ep
        
        return 0, None

    def wear_off(self):
        pass