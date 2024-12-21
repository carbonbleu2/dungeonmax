import os

import pygame
from dungeonmax.buffs.buff import Buff
from dungeonmax.particles.skill.burning import BurningParticle
from dungeonmax.particles.skill.profuse_bleeding import ProfuseBleedingParticle
from dungeonmax.ui.damage_text import DamageText

class Burning(Buff):
    NAME = "Burning"
    IMAGE = os.path.join("graphics", "buffs", "Burning.png")
    DESCRIPTION = "{name}: You're on fire!".format(name=NAME)

    TICK_DAMAGE = 1
    TICK_RATE = 500

    def __init__(self, affected, duration, max_stacks=3):
        super().__init__(affected, self.NAME, duration, self.IMAGE, self.DESCRIPTION)
        self.tick_damage = self.TICK_DAMAGE
        self.last_tick = pygame.time.get_ticks()

        self.particle = None
    
    def effect(self):
        current_time = pygame.time.get_ticks()
        damage = 0

        if current_time - self.last_tick >= self.TICK_RATE:
            damage = self.TICK_DAMAGE
            self.affected.health -= damage
            self.last_tick = current_time

        if self.affected.name != 'Player' and self.particle is None:
            self.particle = BurningParticle(self.affected.rect.centerx, self.affected.rect.centery, -1, 
                                                    self.affected, enemy_rect=self.affected.rect)

        return damage, self.affected.rect
            
    def wear_off(self):
        self.stacks = 0
        if self.particle is not None:
            self.particle.kill()
        self.particle = None