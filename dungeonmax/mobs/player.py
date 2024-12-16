import random

import pygame
from dungeonmax.buffs.resting import Resting
from dungeonmax.gods.god import God
from dungeonmax.gods.gods_enum import GodsRepository
from dungeonmax.mobs.character import Character
from dungeonmax.settings import FPS

class Player(Character):
    def __init__(self, x, y, animations):
        super().__init__(x, y, animations, 'Player', char_type='player')

        self.rect = self.rect.inflate(-10, 0)
        self.rect.center = x, y

        # Attributes
        self.strength = 10
        self.intelligence = 5
        self.dexterity = 5

        # Calibrate stats based on attributes
        self.calibrate_stats()

        # Current stats
        self.health = self.max_hp
        self.energy = self.max_ep

        self.resting = True

        self.invincibility_cooldown = 800

        self.resting_deactivate_timer = pygame.time.get_ticks()
        self.resting_cooldown = 5000

        self.coin_xp_gain = 2

    def calibrate_stats(self):
        self.max_hp = int(self.strength * 10)
        self.max_ep = int(self.intelligence * 8)
        self.melee_attack = int(self.strength * 0.60)
        self.ranged_attack = int(self.dexterity * 0.80)
        self.special_attack = int(self.intelligence * 0.80)
        self.melee_defense = int(self.strength * 0.50)
        self.ranged_defense = int(self.dexterity * 0.50)
        self.special_defense = int(self.intelligence * 0.50)

        self.health_regen_rate = (self.strength * 0.08) / FPS
        self.energy_regen_rate = (self.intelligence * 0.06) / FPS

        self.speed = int(self.dexterity * 0.7)

    def collect(self, item):
        if item.name == 'Coin':
            self.coins += 1
            self.gain_xp(self.coin_xp_gain)
        elif item.name == 'HealthPotion':
            self.health = min(self.max_hp, self.health + 10)
        else:
            print(f"Item collected: {item.name}")

    def gain_xp(self, exp_gain):
        self.total_xp += exp_gain
        self.xp_to_next_level = self.xp_to_next_level - exp_gain
        while self.xp_to_next_level <= 0:
            self.level_up()
            self.xp_to_next_level = self.level * 10 + self.xp_to_next_level

    def level_up(self):
        self.level += 1
        self.strength += 2
        self.dexterity += 0.2
        self.intelligence += 1
        self.calibrate_stats()

    def stats(self):
        return {
            'max_hp': self.max_hp,
            'max_ep': self.max_ep,
            'str': self.strength,
            'dex': self.dexterity,
            'int': self.intelligence,
            'melee_attack': self.melee_attack,
            'ranged_attack': self.ranged_attack,
            'special_attack': self.special_attack,
            'melee_defense': self.melee_defense,
            'ranged_defense': self.ranged_defense,
            'special_defense': self.special_defense,
        }
    
    def get_mouse_side(self):
        if pygame.mouse.get_pos()[0] >= self.rect.centerx:
            return 'right'
        return 'left'
    
    def update(self, player):
        super().update(player)
        buff = Resting(self)
        if self.resting:
            if buff.name not in self.buffs:
                self.add_buff(buff)
            self.buffs[buff.name].active = True
        else:
            if buff.name in self.buffs: 
                self.buffs[buff.name].active = False

        if not self.resting and pygame.time.get_ticks() - self.resting_deactivate_timer > self.resting_cooldown:
            self.resting = True

    def deactivate_resting(self):
        self.resting = False
        self.resting_deactivate_timer = pygame.time.get_ticks()

    def move(self, dx, dy, obstacles, exit_tile=None):
        val = super().move(dx, dy, obstacles, exit_tile)
        if dx != 0 or dy != 0:
            self.deactivate_resting()
        return val
            