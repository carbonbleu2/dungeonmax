import math
import os
import random
import pygame

from dungeonmax.animation_repository import AnimationRepository
from dungeonmax.particles.projectile_particle import ProjectileParticle

class Arrow(ProjectileParticle):
    def __init__(self, name, x, y, angle, proj_speed, damage, on_hit, range_):
        super().__init__(name, AnimationRepository.PROJECTILE_ANIMS, x, y, angle, proj_speed, damage, on_hit, range_=range_)

class WoodenArrow(Arrow):
    DAMAGE = 1
    CODENAME = "WoodenArrow"
    ADDITIONAL_RANGE = 2
    
    def __init__(self, x, y, angle, speed, damage, on_hit, range_):
        super().__init__(
            self.CODENAME, x, y, angle, speed, self.DAMAGE + damage, on_hit,
            self.ADDITIONAL_RANGE + range_)
