import os
import textwrap
import pygame
from dungeonmax.colour import NamedColour

pygame.init()

TITLE = "DungeonMax v0.0.1alpha"

TILE_SIZE = 32

SCREEN_WIDTH = 1900
SCREEN_HEIGHT = 1000

BG_COLOUR = '#141414'

FPS = 70

DAMAGE_TEXT_FONT = pygame.font.Font(
    os.path.join('fonts', 'Minecraftia-Regular.ttf'),
    15
)
DAMAGE_TEXT_COLOUR = 'red'

UI_FONT = os.path.join('fonts', 'Minecraftia-Regular.ttf')
UI_FONT_SIZE = 15
UI_FONT_COLOUR = 'black'

UI_INFO_PANEL_COLOUR = '#3d2328'

HEALTH_BAR_COLOUR = 'red'
ENERGY_BAR_COLOUR = 'blue'

BAR_BG_COLOUR = 'black'
BAR_WIDTH = 300
BAR_HEIGHT = 20
BAR_FG_COLOUR = 'white'

UI_BORDER_COLOUR = 'black'

UI_MESSAGE_BAR_HEIGHT = 30
UI_MESSAGE_FONT_SIZE = 15

UI_RELIGION_SELECT_INSTRUCTION_TEXT = '''
Choose a god and press F to join it's religion. 
Hold left-click to see the god's details
'''
UI_RELIGION_SELECT_NO_GODS_NEARBY = '''
There are no god altars nearby
'''

SCROLL_THRESHOLD = 300

STATS_SCREEN = os.path.join("graphics", "ui", "statscreen.png")

STATS_FONT = os.path.join('fonts', 'Minecraftia-Regular.ttf')
STATS_FONT_SIZE = 20
STATS_FONT_COLOUR = 'black'