import os

import pygame

from dungeonmax.items import *
from dungeonmax.mobs.enemies import *
from dungeonmax.tiles.char_tile_enum import CharTiles
from dungeonmax.tiles.exit_tile_enum import ExitTiles
from dungeonmax.tiles.item_tile_enum import ItemTiles
from dungeonmax.tiles.floor_tile_enum import FloorTiles
from dungeonmax.tiles.wall_tile_enum import WallTiles
from dungeonmax.tiles.god_tile_enum import GodTiles

WALL_TILE_IDS = [WallTiles.STONE_BRICK_WALL1]
PORTAL_TILE_IDS = [ExitTiles.STONE_EXIT1]
FLOOR_TILE_IDS = [FloorTiles.STONE_FLOOR1]
GOD_TILE_IDS = [GodTiles.TROG, GodTiles.VEHLAAN]

TILE_TO_ITEM_CLASSES = {
    ItemTiles.COIN: Coin,
    ItemTiles.HEALTH_POTION: HealthPotion
}    

TILE_TO_CHAR_CLASSES = {
    CharTiles.BLOBBLE: Blobble,
    CharTiles.CHOMPER: Chomper
}

GOD_TILES_TO_GOD_NAMES = {
    GodTiles.TROG: "Trog",
    GodTiles.VEHLAAN: "Vehlaan"
}

class TileLoader:
    TILE_IMAGE_NAMES = {
        FloorTiles.STONE_FLOOR1: "floor1.png",
        
        WallTiles.STONE_BRICK_WALL1: "wall1.png",
        
        ExitTiles.STONE_EXIT1: "exit1.png",
        
        ItemTiles.COIN: "coin.png",
        ItemTiles.HEALTH_POTION: "healthpotion.png",

        CharTiles.PLAYER: "player.png",
        CharTiles.BLOBBLE: "blobble.png",
        CharTiles.CHOMPER: "chomper.png",

        GodTiles.TROG: "altar_trog.png",
        GodTiles.VEHLAAN: "altar_vehlaan.png"
    }

    TILE_IMAGES = {-1: None}

    def __init__(self):
        for tile_num, img in self.TILE_IMAGE_NAMES.items():
            image_path = os.path.join("graphics", "tiles", img)
            self.TILE_IMAGES[tile_num] = pygame.image.load(image_path).convert_alpha()
