import os
from dungeonmax.buffs.buff import Buff

class TrogsHandHPRegen(Buff):
    IMAGE = os.path.join("graphics", "buffs", "TrogsHandHPRegen.png")
    DESCRIPTION = "Extra {new_hp_gen} HP regeneration rate for {duration} seconds."

    def __init__(self, affected, duration):
        self.original_hp_regen_rate = affected.health_regen_rate
        super().__init__(affected, "TrogsHandHPRegen", duration, self.IMAGE, "")
        
    def effect(self):
        from dungeonmax.gods.gods_enum import GodsRepository
        favour = GodsRepository.GODS["Trog"].favour
        increase = (1 + favour / 100) / 60
        self.affected.health = min(self.affected.health + increase, self.affected.max_hp)
        self.description = self.DESCRIPTION.format(new_hp_gen=round(increase, 3), duration=self.duration / 1000)

    def wear_off(self):
        super().wear_off()