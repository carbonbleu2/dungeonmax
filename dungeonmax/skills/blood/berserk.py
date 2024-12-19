import math
import os

import pygame
from dungeonmax.buffs.berserker import Berserker
from dungeonmax.skills.skill import Skill

class Berserk(Skill):
    COOLDOWN = 40
    CODENAME = "Berserk"
    SKILL_CATEGORY = "blood"
    UI_GRAPHIC = os.path.join("graphics", "skills", SKILL_CATEGORY, f"{CODENAME}.png")
    COST = 10
    NAME = "Berserk"
    
    BERSERKER_DURATION = 20
    DESCRIPTION = "Enter a berserk state for 20 seconds, significantly boosting melee attack at the cost of halved defense from all sources."

    def __init__(self):
        super().__init__(
            self.UI_GRAPHIC, self.NAME, self.SKILL_CATEGORY, 
            self.CODENAME, self.COOLDOWN, self.COST, self.DESCRIPTION
        )

    def on_cast(self, player):
        if player.energy >= self.cost and self.can_be_used:
            super().on_cast(player)
            player.energy = max(player.energy - self.cost, 0)
            
            buff = Berserker(player, self.BERSERKER_DURATION * 1000)
            player.add_buff(buff)
            buff.active = True            

            self.last_used = pygame.time.get_ticks()
            self.can_be_used = False
        
        return None

    def on_hit(self, player, enemy):
        pass