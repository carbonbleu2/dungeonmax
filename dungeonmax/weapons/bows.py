import os
import math

import pygame
from dungeonmax.particles.arrows import WoodenArrow
from dungeonmax.weapons.weapon import Weapon

class Bow(Weapon):
    def __init__(self, image, name, codename, ui_graphic, attack_speed, 
                 arrow_speed, damage, projectile_class, damage_range):
        super().__init__(image, name, codename, ui_graphic, attack_speed)
        self.weapon_type = 'Bow'
        self.projectile_class = projectile_class
        self.fired = False
        self.attack_speed = attack_speed
        self.projectile_speed = arrow_speed
        self.damage = damage
        self.damage_range = damage_range

    def update(self, player):
        shot_cooldown = 1000 / self.attack_speed

        self.rect.center = player.rect.center

        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.centerx
        y_dist = -(pos[1] - self.rect.centery)

        self.angle = math.degrees(math.atan2(y_dist, x_dist))

        arrow = None
        if pygame.mouse.get_pressed()[0] and not self.fired and pygame.time.get_ticks() - self.last_used >= shot_cooldown:
            arrow = self.projectile_class(self.rect.centerx, self.rect.centery, self.angle, 
                                          self.projectile_speed, self.damage, self.on_hit,
                                          range_=self.damage_range)
            self.fired = True
            self.last_used = pygame.time.get_ticks()
        if not pygame.mouse.get_pressed()[0]:
            self.fired = False

        return arrow

    def draw(self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        surface.blit(self.image, ((
            self.rect.centerx - int(self.image.get_width() / 2), 
            self.rect.centery - int(self.image.get_height() / 2), 
        )))

class RecruitsBow(Bow):
    NAME = "Recruit's Bow"
    CODENAME = "RecruitsBow"
    UI_GRAPHIC = os.path.join('graphics', 'weapons', 'bows', f"{CODENAME}Graphic.png")
    GRAPHIC = os.path.join('graphics', 'weapons', 'bows', f"{CODENAME}.png")

    DAMAGE = 5
    ATTACK_SPEED = 3
    ARROW_SPEED = 10
    DAMAGE_RANGE = 10

    def __init__(self):
        super().__init__(self.GRAPHIC, self.NAME, self.CODENAME, self.UI_GRAPHIC, self.ATTACK_SPEED, self.ARROW_SPEED, self.DAMAGE, WoodenArrow, self.DAMAGE_RANGE)

    def on_hit(self, player, enemy):
        pass