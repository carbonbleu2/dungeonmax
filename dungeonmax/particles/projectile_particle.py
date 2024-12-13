import math
import random
import pygame

from dungeonmax.settings import *


class ProjectileParticle(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle, proj_speed, damage, on_hit):
        pygame.sprite.Sprite.__init__(self)
        
        self.original_image = pygame.image.load(image).convert_alpha()
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = proj_speed
        self.damage = damage

        self.on_hit = on_hit

        self.dx = self.speed * math.cos(math.radians(self.angle))
        self.dy = -(self.speed * math.sin(math.radians(self.angle)))
        
    def update(self, enemies, player):
        damage = 0
        damage_pos = None

        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH \
            or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

        for enemy in enemies:
            if enemy.rect.colliderect(self.rect) and enemy.alive:
                self.on_hit(player, enemy)
                damage = (self.damage + random.randint(-3, 3) - enemy.ranged_defense)
                damage_pos = enemy.rect
                enemy.health -= damage
                self.kill()

        return damage, damage_pos

    def draw(self, surface):
        surface.blit(self.image, ((
            self.rect.centerx - int(self.image.get_width() / 2), 
            self.rect.centery - int(self.image.get_height() / 2), 
        )))