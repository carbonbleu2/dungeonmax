import math

import pygame

from dungeonmax.settings import TILE_SIZE
from dungeonmax.colour import NamedColour

class Character:
    def __init__(self, x, y, animations, name):
        self.flip = False
        self.animations = animations
        self.frame_index = 0
        self.action = 'idle'
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)
        self.rect.center = (x, y)
        self.name = name
        self.image = animations[name][self.action][self.frame_index]
        self.running = False
        self.alive = True
        self.health = 0
        self.energy = 0

        self.total_xp = 0
        self.xp_to_next_level = 10

        self.level = 1

        self.coins = 0

        self.invincible = False
        self.invincibility_timer = 0
        self.invincibility_cooldown = 500

        self.buffs = {}

    def draw(self, surface):
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(flipped_image, self.rect)
        # pygame.draw.rect(surface, NamedColour.RED.value, self.rect, width=1)

    def move(self, dx, dy):
        self.running = False

        if dx != 0 or dy != 0:
            self.running = True

        if dx < 0:
            self.flip = True
        elif dx > 0:
            self.flip = False

        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2) / 2)
            dy = dy * (math.sqrt(2) / 2)

        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
        for buff_name, buff in list(self.buffs.items()):
            if not buff.active:
                buff.wear_off()
                del self.buffs[buff_name]
            else:
                buff.update()
                buff.effect()

        if self.running:
            self.update_action('run')
        else:
            self.update_action('idle')

        animation_cooldown = 140
        self.image = self.animations[self.name][self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            if self.frame_index >= len(self.animations[self.name][self.action]):
                self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

        if self.invincible and pygame.time.get_ticks() - self.invincibility_timer > self.invincibility_cooldown:
            self.invincible = False
            
    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def update_xp(self, amount):
        pass

    def activate_invincibility(self):
        self.invincible = True
        self.invincibility_timer = pygame.time.get_ticks()
    
    def add_buff(self, buff):
        if buff.name not in self.buffs:
            self.buffs[buff.name] = buff