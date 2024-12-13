import math
import os
import random
import pygame

from dungeonmax.particles.projectile_particle import ProjectileParticle
from dungeonmax.settings import SCREEN_HEIGHT, SCREEN_WIDTH

class Arrow(ProjectileParticle):
    def __init__(self, image, x, y, angle, proj_speed, damage, on_hit, range_):
        super().__init__(image, x, y, angle, proj_speed, damage, on_hit, range_=range_)

class WoodenArrow(Arrow):
    DAMAGE = 1
    CODENAME = "WoodenArrow"
    GRAPHIC = os.path.join('graphics', 'particles', 'arrows', f"{CODENAME}.png")
    ADDITIONAL_RANGE = 2
    
    def __init__(self, x, y, angle, speed, damage, on_hit, range_):
        super().__init__(
            self.GRAPHIC, x, y, angle, speed, self.DAMAGE + damage, on_hit,
            self.ADDITIONAL_RANGE + range_)
