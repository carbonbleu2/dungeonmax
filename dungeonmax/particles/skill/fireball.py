import math
import os
import random
from dungeonmax.animation_repository import AnimationRepository
from dungeonmax.buffs.burning import Burning
from dungeonmax.particles.projectile_particle import ProjectileParticle
from dungeonmax.settings import *

class FireballProjectile(ProjectileParticle):
    CODENAME = "FireballProjectile"
    
    def __init__(self, x, y, angle, proj_speed, damage, on_hit, range_):
        super().__init__(self.CODENAME, AnimationRepository.PROJECTILE_ANIMS, x, y, angle, proj_speed, 
                         damage, on_hit, is_magic=True, range_=range_)
        
class ChomperFireballProjectile(ProjectileParticle):
    CODENAME = "ChomperFireballProjectile"
    PROJECTILE_SPEED = 8
    DAMAGE = 10
    RANGE = 16

    def __init__(self, x, y, target_x, target_y, angle):
        super().__init__(self.CODENAME, AnimationRepository.PROJECTILE_ANIMS, x, y, angle, self.PROJECTILE_SPEED, 
                         self.DAMAGE, self.on_hit, is_magic=True, range_=self.RANGE,
                         source='Chomper')
        
    def on_hit(self, player, enemy):
        if random.randrange(0, 100) < 100:
            burn = Burning(player, 5000)
            player.add_buff(burn)
            player.buffs[burn.name].active = True

    def update(self, screen, enemies, player, obstacles, scroll_x, scroll_y):
        self.rect.x += self.dx + scroll_x
        self.rect.y += self.dy + scroll_y

        self.image = pygame.transform.rotate(self.animations[self.name][self.frame_index], self.angle - 90)

        if self.rect.right < 0 or self.rect.left > screen.width \
            or self.rect.bottom < 0 or self.rect.top > screen.height:
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
                player.on_death(player, 'skill')
            player.deactivate_resting()
            self.kill()

        return None, None

        
        
