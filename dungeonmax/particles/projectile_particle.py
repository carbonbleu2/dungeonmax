import math
import random
import pygame

from dungeonmax.settings import *


class ProjectileParticle(pygame.sprite.Sprite):
    def __init__(self, name, animations, x, y, angle, proj_speed, damage, 
                 on_hit, is_magic=False, range_=15,
                 source='Player'):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.animations = animations
        self.frame_index = 0
        self.angle = angle
        self.image = self.animations[self.name][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = proj_speed
        self.damage = damage
        self.is_magic = is_magic
        
        self.on_hit = on_hit

        self.dx = self.speed * math.cos(math.radians(self.angle))
        self.dy = -(self.speed * math.sin(math.radians(self.angle)))

        self.range = range_ * TILE_SIZE
        self.start_point = x, y

        self.source = source

        self.update_time = pygame.time.get_ticks()
        
    def update(self, screen, enemies, player, obstacles, scroll_x, scroll_y):
        damage = 0
        damage_pos = None

        self.rect.x += self.dx + scroll_x
        self.rect.y += self.dy + scroll_y

        animation_cooldown = 100
        self.image = pygame.transform.rotate(self.animations[self.name][self.frame_index], self.angle - 90)

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            if self.frame_index >= len(self.animations[self.name]):
                self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

        if self.rect.right < 0 or self.rect.left > screen.width \
            or self.rect.bottom < 0 or self.rect.top > screen.height:
            self.kill()

        for obstacle in obstacles:
            if obstacle[1].colliderect(self.rect):
                self.kill()

        if pygame.math.Vector2(self.rect.center).distance_to(self.start_point) >= self.range:
            self.kill()

        for enemy in enemies:
            if enemy.rect.colliderect(self.rect) and enemy.alive:
                self.on_hit(player, enemy)
                damage_reduction = enemy.special_defense if self.is_magic else enemy.ranged_defense
                damage = max(1, (self.damage + random.randint(-1, 1) - damage_reduction))
                damage_pos = enemy.rect
                enemy.health -= damage
                if enemy.health <= 0:
                    enemy.on_death(player, 'ranged')
                self.kill()

        return damage, damage_pos

    def draw(self, surface):
        surface.blit(self.image, ((
            self.rect.centerx - int(self.image.get_width() / 2), 
            self.rect.centery - int(self.image.get_height() / 2), 
        )))