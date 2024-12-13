import os
import pygame
from dungeonmax.colour import NamedColour

pygame.init()

TITLE = "DungeonMax"

TILE_SIZE = 32

SCREEN_WIDTH = 1900
SCREEN_HEIGHT = 1000

BG_COLOUR = 'grey'

FPS = 60

DAMAGE_TEXT_FONT = pygame.font.Font(
    os.path.join('fonts', 'small_pixel.ttf'),
    15
)
DAMAGE_TEXT_COLOUR = 'red'

UI_FONT = os.path.join('fonts', 'small_pixel.ttf')
UI_FONT_SIZE = 15
UI_FONT_COLOUR = 'black'

UI_INFO_PANEL_COLOUR = '#505050'

HEALTH_BAR_COLOUR = 'red'
ENERGY_BAR_COLOUR = 'blue'

BAR_BG_COLOUR = 'black'
BAR_WIDTH = 300
BAR_HEIGHT = 20
BAR_FG_COLOUR = 'white'

UI_BORDER_COLOUR = 'black'