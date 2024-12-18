import os
import random
from dungeonmax.buffs.attack_boost import MeleeAttackBoost
from dungeonmax.buffs.trogs_curse import TrogsCurse
from dungeonmax.gods.god import God
from dungeonmax.tiles.char_tile_enum import CharTiles

class God2(God):
    NAME = 'God2'
    ALTAR_IMAGE = os.path.join('graphics', 'tiles', 'altar_god2.png')
    PROVIDED_SPELLS = []
    PROVIDED_WEAPONS = []
    ALTAR_DESCRIPTION = "A something altar of God2"
    
    def __init__(self):
        super().__init__(self.NAME, self.ALTAR_IMAGE, self.ALTAR_DESCRIPTION,
                         1, 2, 3, 4, 5)

    def punish(self, equipment_manager, enemies, stage, event=None):
        pass

    def level1_perk(self, equipment_manager, enemies):
        pass

    def level2_perk(self, equipment_manager, enemies):
        pass

    def level3_perk(self, equipment_manager, enemies):
        pass

    def level4_perk(self, equipment_manager, enemies):
        pass

    def level5_perk(self, equipment_manager, enemies):
        pass