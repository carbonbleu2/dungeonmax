import os

import pygame


class TileLoader:
    TILE_IMAGE_NAMES = {
        1: "wall1.png",
        0: "floor1.png"
    }

    TILE_IMAGES = {-1: None}

    def __init__(self):
        for tile_num, img in self.TILE_IMAGE_NAMES.items():
            image_path = os.path.join("graphics", "tiles", img)
            self.TILE_IMAGES[tile_num] = pygame.image.load(image_path).convert_alpha()
