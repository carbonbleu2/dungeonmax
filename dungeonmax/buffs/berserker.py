import math
import os

import pygame
from dungeonmax.buffs.buff import Buff
from dungeonmax.colour import NamedColour
from dungeonmax.settings import SCREEN_HEIGHT, SCREEN_WIDTH

class Berserker(Buff):
    NAME = "Berserker"
    IMAGE = os.path.join("graphics", "buffs", f"{NAME}.png")
    DESCRIPTION = "Berserker: Increased melee damage and greatly reduced defense"

    DAMAGE_BOOST_PERCENTAGE = 70
    DEFENSE_MULTIPLIER = 0.5

    CIRCLE_RADIUS = 40
    CIRCLE_COLOR = NamedColour.RED.value
    MIN_ALPHA = 30
    MAX_ALPHA = 180
    FADE_SPEED = 5

    def __init__(self, affected, duration):
        super().__init__(affected, self.NAME, duration, self.IMAGE, self.DESCRIPTION)
        self.original_melee_defense = affected.melee_defense
        self.original_ranged_defense = affected.ranged_defense
        self.original_special_defense = affected.special_defense
        self.original_attack = affected.melee_attack

        self.current_alpha = self.MAX_ALPHA
        self.fading_out = True

        self.circle_surf = pygame.Surface((self.CIRCLE_RADIUS * 2, self.CIRCLE_RADIUS * 2), pygame.SRCALPHA)

    def effect(self):
        self.affected.melee_attack = math.ceil(self.original_attack + (self.DAMAGE_BOOST_PERCENTAGE / 100) * self.original_attack)
        self.affected.melee_defense = math.ceil(self.original_melee_defense * self.DEFENSE_MULTIPLIER)
        self.affected.ranged_defense = math.ceil(self.original_ranged_defense * self.DEFENSE_MULTIPLIER)
        self.affected.special_defense = math.ceil(self.original_special_defense * self.DEFENSE_MULTIPLIER)

    def wear_off(self):
        self.affected.melee_attack = self.original_attack
        self.affected.melee_defense = self.original_melee_defense
        self.affected.ranged_defense = self.original_ranged_defense
        self.affected.special_defense = self.original_special_defense

    def update_fade(self):
        if self.fading_out:
            self.current_alpha -= self.FADE_SPEED
            if self.current_alpha <= self.MIN_ALPHA:
                self.current_alpha = self.MIN_ALPHA
                self.fading_out = False
        else:
            self.current_alpha += self.FADE_SPEED
            if self.current_alpha >= self.MAX_ALPHA:
                self.current_alpha = self.MAX_ALPHA
                self.fading_out = True

    def draw(self, screen):
        self.update_fade()
        self.circle_surf.fill((0, 0, 0, 0))
        pygame.draw.circle(
            self.circle_surf,
            (*self.CIRCLE_COLOR, int(self.current_alpha)),
            (self.CIRCLE_RADIUS, self.CIRCLE_RADIUS),
            self.CIRCLE_RADIUS
        )
        circle_x = self.affected.rect.centerx - self.CIRCLE_RADIUS
        circle_y = self.affected.rect.centery - self.CIRCLE_RADIUS
        screen.blit(self.circle_surf, (circle_x, circle_y))