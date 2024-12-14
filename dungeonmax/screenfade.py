import pygame

from dungeonmax.settings import SCREEN_HEIGHT, SCREEN_WIDTH

class FadeType:
    WHOLE_SCREEN = 1
    CURTAIN_FALL = 2

class ScreenFade():
    def __init__(self, fade_type, colour, speed):
        self.fade_type = fade_type
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0
    
    def fade(self, screen):
        fade_complete = False
        self.fade_counter += self.speed
        if self.fade_type == FadeType.WHOLE_SCREEN:
            pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour, (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen, self.colour, (0, SCREEN_HEIGHT // 2 + self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))
        elif self.fade_type == FadeType.CURTAIN_FALL:
            pygame.draw.rect(screen, self.colour, (0, 0, SCREEN_WIDTH, self.fade_counter))

        if self.fade_counter >= SCREEN_WIDTH:
            fade_complete = True
        return fade_complete
