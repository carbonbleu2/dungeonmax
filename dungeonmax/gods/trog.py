import os
import random
from dungeonmax.buffs.attack_boost import MeleeAttackBoost
from dungeonmax.gods.god import God
from dungeonmax.tiles.char_tile_enum import CharTiles

class Trog(God):
    NAME = 'Trog'
    ALTAR_IMAGE = os.path.join('graphics', 'tiles', 'altar_trog.png')
    PROVIDED_SPELLS = ["Berserk", "Trog's Hand"]
    PROVIDED_WEAPONS = ["Bonecrusher"]
    
    def __init__(self):
        super().__init__(self.NAME, self.ALTAR_IMAGE, 
                         1, 2, 3, 4, 5)

    def punish(self, equipment_manager, enemies, stage, event=None):
        # Passively, slash melee attack by 75%
        melee_attack_change = -self.player.melee_attack * 0.75
        buff = MeleeAttackBoost(self.player, -1, melee_attack_change)
        self.player.add_buff(buff)
        buff.active = True

        # Snatch all of the granted weapons and skills
        for weapon in equipment_manager.weapons:
            if weapon.name in self.PROVIDED_WEAPONS:
                equipment_manager.remove_weapon(weapon)

        for skill in equipment_manager.skills:
            if skill.name in self.PROVIDED_SPELLS:
                equipment_manager.remove_skill(skill)

        if event == 'new_stage':
            # When entering a new stage, there is a 40% chance to 
            # spawn a Trog's Knight or a Blood Wolf
            if random.randrange(0, 100) < 40:
                stage.spawn_enemy(CharTiles.CHOMPER)

    def level1_perk(self, equipment_manager, enemies):
        from dungeonmax.skills.flame.fireball import Fireball
        equipment_manager.add_skill(Fireball())

    def level2_perk(self, equipment_manager, enemies):
        print("Level 2 perk")

    def level3_perk(self, equipment_manager, enemies):
        print("Level 3 perk")

    def level4_perk(self, equipment_manager, enemies):
        print("Level 4 perk")

    def level5_perk(self, equipment_manager, enemies):
        print("Level 5 perk")