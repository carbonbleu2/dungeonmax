import math
import os
import random
from dungeonmax.particles.projectile_particle import ProjectileParticle
from dungeonmax.settings import *

class FireballProjectile(ProjectileParticle):
    CODENAME = "FireballProjectile"
    GRAPHIC = os.path.join('graphics', 'particles', 'fire', f"{CODENAME}.png")

    def __init__(self, x, y, angle, proj_speed, damage, on_hit, range_):
        super().__init__(self.GRAPHIC, x, y, angle, proj_speed, 
                         damage, on_hit, is_magic=True, range_=range_)
        
class ChomperFireballProjectile(ProjectileParticle):
    CODENAME = "ChomperFireballProjectile"
    GRAPHIC = os.path.join('graphics', 'particles', 'fire', "FireballProjectile.png")
    PROJECTILE_SPEED = 8
    DAMAGE = 10
    RANGE = 16

    def __init__(self, x, y, target_x, target_y):
        x_dist = (target_x - x)
        y_dist = -(target_y - y)
        self.angle = math.degrees(math.atan2(y_dist, x_dist))
        super().__init__(self.GRAPHIC, x, y, self.angle, self.PROJECTILE_SPEED, 
                         self.DAMAGE, self.on_hit, is_magic=True, range_=self.RANGE,
                         source='Chomper')
        
    def on_hit(self, player, enemy):
        pass

    def update(self, enemies, player, obstacles, scroll_x, scroll_y):
        self.rect.x += self.dx + scroll_x
        self.rect.y += self.dy + scroll_y

        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH \
            or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

        if pygame.math.Vector2(self.rect.center).distance_to(self.start_point) >= self.range:
            self.kill()

        if player.rect.colliderect(self.rect) and player.alive:
            self.on_hit(player, None)
            damage_reduction = player.special_defense
            damage = max(1, (self.damage + random.randint(-1, 1) - damage_reduction))
            damage_pos = player.rect
            player.health -= damage
            if player.health <= 0:
                player.on_death(player)
            player.deactivate_resting()
            self.kill()

        return None, None

        
        
