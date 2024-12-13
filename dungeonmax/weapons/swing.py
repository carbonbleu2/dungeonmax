import math
import random
import pygame

class ArcSwing(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle, proj_speed, damage, on_hit):
        pygame.sprite.Sprite.__init__(self)

        self.pivot = (x, y)  # Pivot point (center of the swing)
        self.original_image = image  # Unrotated image
        self.speed = proj_speed  # Speed of swing rotation
        self.damage = damage  # Damage dealt

        self.image = self.original_image
        self.rect = self.image.get_rect(center=self.pivot)

        self.angle = angle  # Initial angle of the swing
        self.swing_angle = -85  # Start swing angle (relative to the pivot)
        self.max_swing_angle = 85  # Maximum swing arc  

        self.radius = 30     
        self.on_hit = on_hit
        
    def update(self, enemies, player):
        damage = 0
        damage_pos = None

        # Rotate the sword
        self.swing_angle += self.speed
        if self.swing_angle > self.max_swing_angle:
            self.kill()  # Remove the swing when arc is complete

        # Update the pivot point to follow the player
        self.pivot = player.rect.center

        # Update the position based on the rotation
        rad_angle = math.radians(self.angle + self.swing_angle)
        offset_x = math.cos(rad_angle) * self.radius
        offset_y = math.sin(rad_angle) * self.radius
        self.rect.center = (self.pivot[0] + offset_x, self.pivot[1] - offset_y)

        # Rotate the image
        self.image = pygame.transform.rotate(self.original_image, (self.angle + self.swing_angle) - 90)
        self.rect = self.image.get_rect(center=self.rect.center)

        # Check for collisions with enemies
        for enemy in enemies:
            if enemy.rect.colliderect(self.rect) and enemy.alive and not enemy.invincible:
                self.on_hit(player, enemy)
                damage = max(1, self.damage + random.randint(-1, 1) - enemy.melee_defense)
                damage_pos = enemy.rect
                enemy.health -= damage
                enemy.activate_invincibility()

        return damage, damage_pos
    
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
