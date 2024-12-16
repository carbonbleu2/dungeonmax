import pygame


class AnimatedParticle(pygame.sprite.Sprite):
    def __init__(self, x, y, name, animations, stick_to_player=False, duration=-1, source='Player'):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.animations = animations
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animations[name][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.stick_to_player = stick_to_player
        self.start_time = pygame.time.get_ticks()
        self.duration = duration
        self.source = source

    def update(self, enemies, player, *args, **kwargs):
        if self.stick_to_player:
            self.rect.center = player.rect.center

        animation_cooldown = 100
        self.image = self.animations[self.name][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            if self.frame_index >= len(self.animations[self.name]):
                self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

        if self.duration >= 0:
            if pygame.time.get_ticks() - self.start_time >= self.duration:
                self.kill()

        return 0, None
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)