import os
from dungeonmax.animation_repository import AnimationRepository
from dungeonmax.particles.projectile_particle import ProjectileParticle

class HaemoblobProjectile(ProjectileParticle):
    CODENAME = "HaemoblobProjectile"
    GRAPHIC = os.path.join('graphics', 'particles', 'fire', f"{CODENAME}.png")

    def __init__(self, x, y, angle, proj_speed, damage, on_hit, range_):
        print(damage)
        super().__init__(self.CODENAME, AnimationRepository.PROJECTILE_ANIMS, x, y, angle, proj_speed, 
                         damage, on_hit, is_magic=True, range_=range_)