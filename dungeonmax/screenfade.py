import pygame

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
            pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, screen.width // 2, screen.height))
            pygame.draw.rect(screen, self.colour, (screen.width // 2 + self.fade_counter, 0, screen.width, screen.height))
            pygame.draw.rect(screen, self.colour, (0, 0 - self.fade_counter, screen.width, screen.height // 2))
            pygame.draw.rect(screen, self.colour, (0, screen.height // 2 + self.fade_counter, screen.width, screen.height))
        elif self.fade_type == FadeType.CURTAIN_FALL:
            pygame.draw.rect(screen, self.colour, (0, 0, screen.width, self.fade_counter))

        if self.fade_counter >= screen.width:
            fade_complete = True
        return fade_complete
