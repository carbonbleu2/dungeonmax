import os
from dungeonmax.particles.projectile_particle import ProjectileParticle

class FireballProjectile(ProjectileParticle):
    CODENAME = "FireballProjectile"
    GRAPHIC = os.path.join('graphics', 'particles', 'fire', f"{CODENAME}.png")

    def __init__(self, x, y, angle, proj_speed, damage, on_hit, range_):
        super().__init__(self.GRAPHIC, x, y, angle, proj_speed, 
                         damage, on_hit, is_magic=True, range_=range_)