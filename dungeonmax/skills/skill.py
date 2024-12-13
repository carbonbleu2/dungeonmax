import math
import pygame

class Skill:
    def __init__(self, image, name, skill_class, codename, cooldown, cost, description):
        self.name = name
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        
        self.skill_class = skill_class,

        self.codename = codename

        self.description = None

        self.last_used = 0
        self.can_be_used = True
        self.cooldown = cooldown
        self.time_left_till_next_use = 0

        self.cost = cost

    def on_cast(self, player):
        pass

    def update(self):
        if not self.can_be_used:
            time_passed = pygame.time.get_ticks() - self.last_used
            self.time_left_till_next_use = round(max((self.cooldown * 1000) - time_passed, 0) / 1000, 1)
            if time_passed >= self.cooldown * 1000:
                self.can_be_used = True