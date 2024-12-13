import math
import os
import random
import pygame

from dungeonmax.particles.projectile_particle import ProjectileParticle
from dungeonmax.settings import SCREEN_HEIGHT, SCREEN_WIDTH

class Arrow(ProjectileParticle):
    def __init__(self, image, x, y, angle, proj_speed, damage, on_hit):
        super().__init__(image, x, y, angle, proj_speed, damage, on_hit)

class WoodenArrow(Arrow):
    DAMAGE = 1
    CODENAME = "WoodenArrow"
    GRAPHIC = os.path.join('graphics', 'particles', 'arrows', f"{CODENAME}.png")
    
    def __init__(self, x, y, angle, speed, damage, on_hit):
        super().__init__(self.GRAPHIC, x, y, angle, speed, self.DAMAGE + damage, on_hit)
