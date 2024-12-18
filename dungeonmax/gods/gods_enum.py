from enum import Enum

import pygame

from dungeonmax.gods.god import God
from dungeonmax.gods.god2 import God2
from dungeonmax.gods.trog import Trog

class GodsRepository:
    GODS = {
        "Trog": Trog(),
        "God2": God2()
    }

    CANNOT_REJOIN = ["Trog", "God2"]

    def __init__(self):
        for god in self.GODS:
            self.GODS[god].altar_image = pygame.image.load(self.GODS[god].altar_image).convert_alpha()

    @staticmethod
    def get_god(god_name) -> God:
        return GodsRepository.GODS[god_name]
    
    @staticmethod
    def cannot_rejoin(god_name) -> bool:
        return god_name in GodsRepository.CANNOT_REJOIN