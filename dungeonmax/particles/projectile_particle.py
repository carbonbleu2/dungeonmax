import math
import random
import pygame

from dungeonmax.settings import *


class ProjectileParticle(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle, proj_speed, damage, 
                 on_hit, is_magic=False, range_=15,
                 source='Player'):
        pygame.sprite.Sprite.__init__(self)
        
        self.original_image = pygame.image.load(image).convert_alpha()
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
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
        
    def update(self, screen, enemies, player, obstacles, scroll_x, scroll_y):
        damage = 0
        damage_pos = None

        self.rect.x += self.dx + scroll_x
        self.rect.y += self.dy + scroll_y

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