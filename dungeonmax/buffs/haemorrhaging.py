import os

import pygame
from dungeonmax.buffs.buff import Buff
from dungeonmax.particles.skill.profuse_bleeding import ProfuseBleedingParticle
from dungeonmax.ui.damage_text import DamageText

class HaemorrhagingDebuff(Buff):
    NAME = "Haemorrhaging"
    IMAGE = os.path.join("graphics", "buffs", f"{NAME}.png")
    DESCRIPTION = "Haemorrhaging: Bleeding profusely ({stacks} stacks) with reduced speed"

    TICK_DAMAGE = 2

    def __init__(self, affected, duration, tick_rate, max_stacks=3):
        super().__init__(affected, self.NAME, duration, self.IMAGE, self.DESCRIPTION)
        self.tick_damage = self.TICK_DAMAGE
        self.stacks = 1
        self.max_stacks = max_stacks
        self.last_tick = pygame.time.get_ticks()
        self.tick_rate = tick_rate

        self.particle = None

        self.original_speed = affected.speed

        self.description = self.DESCRIPTION.format(stacks=self.stacks)
    
    def add_stack(self):
        if self.stacks < self.max_stacks:
            self.stacks += 1
        self.start = pygame.time.get_ticks()
        self.active = True
        self.description = self.DESCRIPTION.format(stacks=self.stacks)

    def effect(self):
        current_time = pygame.time.get_ticks()
        damage = 0

        self.affected.speed = max(self.original_speed * 0.1, self.original_speed * (1 - (0.1 * self.stacks)))

        if current_time - self.last_tick >= self.tick_rate:
            stack_multiplier = self.stacks
            damage = int(self.tick_damage * stack_multiplier)
            
            self.affected.health -= damage
            
            self.last_tick = current_time

        if self.affected.name != 'Player' and self.particle is None:
            self.particle = ProfuseBleedingParticle(self.affected.rect.centerx, self.affected.rect.centery, -1, 
                                                    self.affected, enemy_rect=self.affected.rect)

        return damage, self.affected.rect
            
    def wear_off(self):
        self.stacks = 0
        self.particle.kill()
        self.particle = None
        self.affected.speed = self.original_speed