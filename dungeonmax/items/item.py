import pygame

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, name, animations):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.animations = animations
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animations[name][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, player, *args, **kwargs):
        animation_cooldown = 100
        self.image = self.animations[self.name][self.frame_index]

        if self.rect.colliderect(player.rect):
            if hasattr(player, 'collect'):
                player.collect(self)
            self.kill()

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            if self.frame_index >= len(self.animations[self.name]):
                self.frame_index = 0
            self.update_time = pygame.time.get_ticks()