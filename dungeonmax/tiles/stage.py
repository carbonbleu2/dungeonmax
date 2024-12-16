import os
import random
from dungeonmax.mobs.player import Player
from dungeonmax.tiles.tile_loader import *
from dungeonmax.settings import TILE_SIZE
from dungeonmax.animation_repository import AnimationRepository

class Stage:
    def __init__(self):
        self.map_tiles = []
        self.obstacle_tiles = []
        self.portal_tile = None
        self.item_list = []
        self.player = None
        self.npc_list = []
        self.floor_tiles = []

    def process_tiles(self, data):
        self.length = len(data)

        for y, row in enumerate(data):
            for x, col in enumerate(row):
                image = TileLoader.TILE_IMAGES[col]
                if image is not None:
                    image_rect = image.get_rect()
                    image_x = x * TILE_SIZE
                    image_y = y * TILE_SIZE
                    image_rect.center = image_x, image_y
                    tile = [image, image_rect, image_x, image_y]
                    self.map_tiles.append(tile)
                    if col in FLOOR_TILE_IDS:
                        self.floor_tiles.append(tile)
                    if col in WALL_TILE_IDS:
                        self.obstacle_tiles.append(tile)
                    if col in PORTAL_TILE_IDS:
                        self.portal_tile = tile

                    if col in TILE_TO_ITEM_CLASSES:
                        item_class = TILE_TO_ITEM_CLASSES[col]
                        self.item_list.append(item_class(image_x, image_y, AnimationRepository.ITEM_ANIMS))
                        tile[0] = TileLoader.TILE_IMAGES[random.choice(FLOOR_TILE_IDS)]
                    if col == CharTiles.PLAYER:
                        self.player = Player(image_x, image_y, AnimationRepository.MOB_ANIMS)
                        tile[0] = TileLoader.TILE_IMAGES[random.choice(FLOOR_TILE_IDS)]
                    elif col in TILE_TO_CHAR_CLASSES:
                        char_class = TILE_TO_CHAR_CLASSES[col]
                        character = char_class(image_x, image_y, AnimationRepository.MOB_ANIMS)
                        self.npc_list.append(character)
                        tile[0] = TileLoader.TILE_IMAGES[random.choice(FLOOR_TILE_IDS)]

    def spawn_enemy(self, enemy_id):
        random_floor_tile = random.choice(self.floor_tiles)
        char_class = TILE_TO_CHAR_CLASSES[enemy_id]
        character = char_class(random_floor_tile[2], random_floor_tile[3], AnimationRepository.MOB_ANIMS)
        self.npc_list.append(character)


    def read_from_file(self, file_name):
        map_data = []
        with open(os.path.join("maps", file_name), "r") as f:
            for line in f.readlines():
                l = list(map(int, line.split(",")))
                map_data.append(l)
        self.process_tiles(map_data)

    def draw(self, screen):
        for tile in self.map_tiles:
            screen.blit(tile[0], tile[1])

    def update(self, screen_scroll_x, screen_scroll_y):
        for tile in self.map_tiles:
            tile[2] += screen_scroll_x
            tile[3] += screen_scroll_y
            tile[1].center = tile[2], tile[3]