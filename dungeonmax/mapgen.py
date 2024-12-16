from dungeonmax.tiles.char_tile_enum import CharTiles
from dungeonmax.tiles.exit_tile_enum import ExitTiles
from dungeonmax.tiles.wall_tile_enum import WallTiles
from dungeonmax.tiles.stage import Stage


class MapGen:
    def __init__(self, stage_num, width, height):
        self.stage_num = stage_num
        self.width = width
        self.height = height

    def generate(self):
        map_data = [
            [0 for _ in range(self.width)] for _ in range(self.height)
        ]

        for j in range(self.width):
            if j == 0 or j == self.width - 1:
                for i in range(self.height):
                    map_data[i][j] = WallTiles.STONE_BRICK_WALL1
            map_data[0][j] = WallTiles.STONE_BRICK_WALL1
            map_data[-1][j] = WallTiles.STONE_BRICK_WALL1

        map_data[self.height // 2][self.width // 2] = CharTiles.PLAYER
        map_data[0][self.width // 2] = ExitTiles.STONE_EXIT1

        stage = Stage()
        stage.process_tiles(map_data)
        return stage