from dungeonmax.animation_repository import AnimationRepository
from dungeonmax.particles.particle import AnimatedParticle


class WarriorsResolveParticle(AnimatedParticle):
    CODENAME = "WarriorsResolveParticle"

    def __init__(self, x, y, duration):
        super().__init__(x, y, self.CODENAME, AnimationRepository.PARTICLE_ANIMS, stick_to_player=True, duration=duration)