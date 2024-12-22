import math
import os
import pygame

from dungeonmax.gods.gods_enum import GodsRepository
from dungeonmax.weapons.swing import ArcSwing
from dungeonmax.weapons.weapon import Weapon

class Sword(Weapon):
    def __init__(self, image, name, codename, ui_graphic, 
                 attack_speed, swing_speed, damage, description):
        super().__init__(image, name, codename, ui_graphic, attack_speed, description)
        self.weapon_type = 'Sword'
        self.used = False
        self.attack_speed = attack_speed
        self.swing_speed = swing_speed
        self.damage = damage
        self.swing_angle = 0
        self.swinging = False
        self.particle_class = ArcSwing
        self.max_swing_angle = 170
        
    def update(self, player):
        shot_cooldown = 1000 / self.attack_speed

        # Center the sword at the player's position
        self.rect.center = player.rect.center

        # Calculate the direction towards the mouse cursor
        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.centerx
        y_dist = -(pos[1] - self.rect.centery)

        # Calculate the player's angle towards the mouse
        self.angle = math.degrees(math.atan2(y_dist, x_dist))

        sword_sprite = None

        # Start swinging the sword
        if pygame.mouse.get_pressed()[0] and not self.swinging and pygame.time.get_ticks() - self.last_used >= shot_cooldown:
            sword_sprite = self.particle_class(self.image, self.rect.centerx, self.rect.centery, 
                                               self.angle, self.swing_speed, self.damage + player.melee_attack, self.on_hit)
            self.swinging = True
            self.swing_angle = -self.max_swing_angle // 2  # Start from the leftmost angle
            self.last_used = pygame.time.get_ticks()
            player.deactivate_resting()

        # Update the swing angle if swinging
        if self.swinging:
            self.swing_angle += self.swing_speed
            if self.swing_angle > self.max_swing_angle // 2:
                self.swinging = False  # End the swing

        return sword_sprite

    def draw(self, surface):
        pass

    def on_hit(self, player, enemy):
        trog = GodsRepository.GODS["Trog"]
        if trog.active and not trog.abandoned:
            GodsRepository.GODS["Trog"].favour += 1

class RecruitsSword(Sword):
    NAME = "Recruit's Sword"
    CODENAME = "RecruitsSword"
    UI_GRAPHIC = os.path.join('graphics', 'weapons', 'swords', f"{CODENAME}Graphic.png")
    GRAPHIC = os.path.join('graphics', 'weapons', 'swords', f"{CODENAME}.png")

    DESCRIPTION = "A basic sword to get novice fighters acquainted with the mechanics"

    DAMAGE = 5
    ATTACK_SPEED = 2
    SWING_SPEED = 20

    SCALE_FACTOR = 1.2

    def __init__(self):
        super().__init__(self.GRAPHIC, self.NAME, self.CODENAME, self.UI_GRAPHIC, 
                         self.ATTACK_SPEED, self.SWING_SPEED, self.DAMAGE,
                         self.DESCRIPTION)
        self.image = pygame.transform.scale_by(self.image, self.SCALE_FACTOR)