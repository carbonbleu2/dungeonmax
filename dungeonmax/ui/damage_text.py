import os
import pygame

from dungeonmax.settings import DAMAGE_TEXT_FONT

class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = DAMAGE_TEXT_FONT.render(str(damage), False, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self, scroll_x, scroll_y, **kwargs):
        self.rect.x += scroll_x
        self.rect.y += scroll_y
        
        self.rect.y -= 1
        self.counter += 1
        if self.counter >= 30:
            self.kill()
    