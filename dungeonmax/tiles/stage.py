from dungeonmax.tiles.tile_loader import TileLoader
from dungeonmax.settings import TILE_SIZE

class Stage:
    def __init__(self):
        self.map_tiles = []

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

    def draw(self, screen):
        for tile in self.map_tiles:
            screen.blit(tile[0], tile[1])