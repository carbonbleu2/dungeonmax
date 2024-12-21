import math
import os
import random

import pygame
from dungeonmax.buffs.burning import Burning
from dungeonmax.particles.skill.fireball import FireballProjectile
from dungeonmax.skills.skill import Skill

class Fireball(Skill):
    DAMAGE = 8
    COOLDOWN = 2
    CODENAME = "Fireball"
    SKILL_CATEGORY = "flame"
    UI_GRAPHIC = os.path.join("graphics", "skills", SKILL_CATEGORY, f"{CODENAME}.png")
    COST = 5
    NAME = "Fireball"
    DESCRIPTION = "Launch a fireball at the direction of your mouse cursor with \
        a 30% chance to inflict a burn for 5 seconds"
    
    PROJECTILE_SPEED = 5
    PROJECTILE_RANGE = 15
    BURN_DURATION = 5

    def __init__(self):
        super().__init__(
            self.UI_GRAPHIC, self.NAME, self.SKILL_CATEGORY, 
            self.CODENAME, self.COOLDOWN, self.COST, self.DESCRIPTION
        )

    def on_cast(self, player):
        fireball = None

        if player.energy >= self.cost and self.can_be_used:
            super().on_cast(player)
            player.energy = max(player.energy - self.cost, 0)
            
            mouse_pos = pygame.mouse.get_pos()
            current_x, current_y = player.rect.centerx, player.rect.centery
            x_dist = mouse_pos[0] - current_x
            y_dist = -(mouse_pos[1] - current_y)
            angle = math.degrees(math.atan2(y_dist, x_dist))

            fireball = FireballProjectile(current_x, current_y, angle, self.PROJECTILE_SPEED, 
                                          self.DAMAGE + player.special_attack, self.on_hit,
                                          range_=self.PROJECTILE_RANGE)
            self.last_used = pygame.time.get_ticks()
            self.can_be_used = False
        
        return fireball

    def on_hit(self, player, enemy):
        # 30% chance to add burning debuff
        if random.randrange(0, 100) < 30:
            burn = Burning(enemy, self.BURN_DURATION * 1000)
            enemy.add_buff(burn)
            enemy.buffs[burn.name].active = True