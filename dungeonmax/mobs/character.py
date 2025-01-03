import math

import pygame

from dungeonmax.settings import SCROLL_THRESHOLD, TILE_SIZE
from dungeonmax.colour import NamedColour

class Character:
    def __init__(self, x, y, animations, name, char_type, boss=False, size_scale=1, exp_gain=0):
        self.flip = False
        self.animations = animations
        self.frame_index = 0
        self.action = 'idle'
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect(0, 0, TILE_SIZE * size_scale, TILE_SIZE * size_scale)
        self.rect.center = (x, y)
        self.name = name
        self.image = animations[name][self.action][self.frame_index]
        self.running = False
        self.alive = True
        self.health = 0
        self.energy = 0
        self.char_type = char_type
        
        self.boss = boss

        self.total_xp = 0
        self.xp_to_next_level = 10

        self.level = 1

        self.coins = 0

        self.invincible = False
        self.invincibility_timer = 0
        self.invincibility_cooldown = 800

        self.animation_cooldown = 140

        self.buffs = {}

        self.exp_gain = exp_gain

    def draw(self, surface):
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(flipped_image, self.rect)
        # pygame.draw.rect(surface, NamedColour.RED.value, self.rect, width=1)

    def move(self, screen, dx, dy, obstacles, exit_tile=None):
        screen_scroll_x = 0
        screen_scroll_y = 0

        level_complete = False

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

        self.rect.x += round(dx)
        for obstacle in obstacles:
            if obstacle[1].colliderect(self.rect):
                if dx > 0:
                    self.rect.right = obstacle[1].left
                elif dx < 0:
                    self.rect.left = obstacle[1].right
        self.rect.y += round(dy)
        for obstacle in obstacles:
            if obstacle[1].colliderect(self.rect):
                if dy > 0:
                    self.rect.bottom = obstacle[1].top
                elif dy < 0:
                    self.rect.top = obstacle[1].bottom

        if self.char_type == 'player':
            if exit_tile[1].colliderect(self.rect):
                exit_distance = pygame.math.Vector2(exit_tile[1].center).distance_to(self.rect.center)
                if exit_distance < 20:
                    level_complete = True

            if self.rect.right > (screen.height - SCROLL_THRESHOLD):
                screen_scroll_x = (screen.height - SCROLL_THRESHOLD) - self.rect.right
                self.rect.right = screen.height - SCROLL_THRESHOLD
            if self.rect.left < SCROLL_THRESHOLD:
                screen_scroll_x = SCROLL_THRESHOLD - self.rect.left
                self.rect.left = SCROLL_THRESHOLD

            if self.rect.bottom > (screen.height - SCROLL_THRESHOLD):
                screen_scroll_y = (screen.height - SCROLL_THRESHOLD) - self.rect.bottom
                self.rect.bottom = screen.height - SCROLL_THRESHOLD
            if self.rect.top < SCROLL_THRESHOLD:
                screen_scroll_y = SCROLL_THRESHOLD - self.rect.top
                self.rect.top = SCROLL_THRESHOLD

        return screen_scroll_x, screen_scroll_y, level_complete

    def update(self, player):
        buff_damages = {}

        if self.health <= 0:
            self.health = 0
            self.alive = False

        for buff_name, buff in list(self.buffs.items()):
            if not buff.active:
                buff.wear_off()
                del self.buffs[buff_name]
            else:
                buff.update()
                buff_damages[buff_name] = buff.effect()

        if self.running:
            self.update_action('run')
        else:
            self.update_action('idle')

        animation_cooldown = self.animation_cooldown
        self.image = self.animations[self.name][self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            if self.frame_index >= len(self.animations[self.name][self.action]):
                self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

        if self.invincible and pygame.time.get_ticks() - self.invincibility_timer > self.invincibility_cooldown:
            self.invincible = False

        return {
            "BuffDamages": buff_damages
        }
            
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

    def deactivate_buff(self, buff):
        if buff.name in self.buffs:
            self.buffs[buff.name].active = False

    def ai(self, screen, player, enemies, obstacles, scroll_x, scroll_y):
        self.rect.x += scroll_x
        self.rect.y += scroll_y

    def on_death(self, player, damage_type):
        if player is None:
            return
        player.gain_xp(self.exp_gain)
        if self.char_type != 'player':
            from dungeonmax.gods.gods_enum import GodsRepository
            if damage_type == 'melee':
                GodsRepository.GODS["Trog"].favour += 2
            else:
                GodsRepository.GODS["Trog"].favour -= 1