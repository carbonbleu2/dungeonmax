import math
import os
import pygame

from dungeonmax.buffs.haemorrhaging import HaemorrhagingDebuff
from dungeonmax.particles.skill.haemoblob import HaemoblobProjectile
from dungeonmax.skills.skill import Skill

class Haemorrhage(Skill):
    DAMAGE = 8
    COOLDOWN = 3
    CODENAME = "Haemorrhage"
    SKILL_CATEGORY = "blood"
    UI_GRAPHIC = os.path.join("graphics", "skills", SKILL_CATEGORY, f"{CODENAME}.png")
    COST = 8
    NAME = "Haemorrhage"
    PROJECTILE_SPEED = 4
    PROJECTILE_RANGE = 12
    
    STACK_LIMIT = 3
    TICK_RATE = 1000

    DEBUFF_DURATION = 10
    DESCRIPTION = "Throw a blob of blood to deal damage and inflict a stacking bleed that slows enemies and deals increasing damage over time"

    def __init__(self):
        super().__init__(
            self.UI_GRAPHIC, self.NAME, self.SKILL_CATEGORY,
            self.CODENAME, self.COOLDOWN, self.COST, self.DESCRIPTION
        )
        
    def on_cast(self, player):
        projectile = None

        if player.energy >= self.cost and self.can_be_used:
            super().on_cast(player)
            player.energy = max(player.energy - self.cost, 0)
            
            mouse_pos = pygame.mouse.get_pos()
            current_x, current_y = player.rect.centerx, player.rect.centery
            x_dist = mouse_pos[0] - current_x
            y_dist = -(mouse_pos[1] - current_y)
            angle = math.degrees(math.atan2(y_dist, x_dist))

            projectile = HaemoblobProjectile(current_x, current_y, angle, self.PROJECTILE_SPEED,
                                       self.DAMAGE + player.special_attack, self.on_hit,
                                       range_=self.PROJECTILE_RANGE)
            self.last_used = pygame.time.get_ticks()
            self.can_be_used = False
        
        return projectile

    def on_hit(self, player, enemy):
        # Check if enemy already has hemorrhage debuff
        existing_hemorrhage = None
        for buff in enemy.buffs:  # Assuming enemy has a buffs list
            if buff == 'Haemorrhaging':
                existing_hemorrhage = enemy.buffs[buff]
                break
        particle = None
        if existing_hemorrhage:
            # Add stack to existing hemorrhage
            existing_hemorrhage.add_stack()
        else:
            # Create new hemorrhage debuff
            new_hemorrhage = HaemorrhagingDebuff(
                enemy, self.DEBUFF_DURATION * 1000, self.TICK_RATE, 
                max_stacks=self.STACK_LIMIT
            )
            enemy.add_buff(new_hemorrhage)
            enemy.buffs[new_hemorrhage.name].active = True
