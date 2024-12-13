import pygame


class Buff:
    def __init__(self, affected, name, duration, image):
        self.affected = affected
        self.name = name
        self.duration = duration
        self.image = pygame.image.load(image).convert_alpha()
        self.start = pygame.time.get_ticks()
        self.active = False

    def update(self):
        if pygame.time.get_ticks() - self.start < self.duration:
            self.active = True
        else:
            self.active = False

    def effect(self):
        pass

    def wear_off(self):
        pass
