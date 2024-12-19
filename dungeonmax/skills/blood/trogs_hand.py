import os

import pygame
from dungeonmax.skills.skill import Skill
from dungeonmax.buffs.trogs_hand_hp_regen import TrogsHandHPRegen

class TrogsHand(Skill):
    COOLDOWN = 30
    CODENAME = "TrogsHand"
    SKILL_CATEGORY = "blood"
    UI_GRAPHIC = os.path.join("graphics", "skills", SKILL_CATEGORY, f"{CODENAME}.png")
    COST = 20
    NAME = "Trog's Hand"
    
    BUFF_DURATION = 10
    HP_REGEN_INCREASE = 20
    DESCRIPTION = "Gain (1 + Favour / 100) HP regeneration rate for 10 seconds."

    def __init__(self):
        super().__init__(
            self.UI_GRAPHIC, self.NAME, self.SKILL_CATEGORY, 
            self.CODENAME, self.COOLDOWN, self.COST, self.DESCRIPTION
        )

    def on_cast(self, player):
        if player.energy >= self.cost and self.can_be_used:
            super().on_cast(player)
            player.energy = max(player.energy - self.cost, 0)
            
            buff = TrogsHandHPRegen(player, self.BUFF_DURATION * 1000)
            player.add_buff(buff)
            buff.active = True            

            self.last_used = pygame.time.get_ticks()
            self.can_be_used = False
        
        return None

    def on_hit(self, player, enemy):
        pass