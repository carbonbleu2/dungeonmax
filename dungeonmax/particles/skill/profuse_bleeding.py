from dungeonmax.animation_repository import AnimationRepository
from dungeonmax.particles.particle import AnimatedParticle


class ProfuseBleedingParticle(AnimatedParticle):
    CODENAME = "ProfuseBleedingParticle"

    def __init__(self, x, y, duration, entity, enemy_rect=None):
        super().__init__(x, y, self.CODENAME, AnimationRepository.PARTICLE_ANIMS, 
                         stick_to_enemy=True, entity=entity, duration=duration, 
                         enemy_rect=enemy_rect)
        self.animation_cooldown = 50