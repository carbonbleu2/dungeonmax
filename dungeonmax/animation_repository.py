import os
import re

import pygame

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [atoi(c) for c in re.split(r'(\d+)', text) ]

class AnimationRepository:
    PARTICLE_TYPES = {
        "FireballProjectile": "fire",
        "WoodenArrow": "arrows",
        "WarriorsResolveParticle": "support"
    }

    MOB_ANIMS = {
        "Blobble": {
            "idle": [],
            "run": []
        },
        "Chomper": {
            "idle": [],
            "run": []
        },
        "Player": {
            "idle": [],
            "run": []
        }
    }
        
    ITEM_ANIMS = {
        "Coin": [],
        "HealthPotion": [],
        "EnergyPotion": []
    }   

    PARTICLE_ANIMS = {
        "WarriorsResolveParticle": []
    }

    def __init__(self):
        for mob in self.MOB_ANIMS:
            for state in self.MOB_ANIMS[mob].keys():
                image_files = os.listdir(os.path.join('graphics', 'characters', mob, state))
                image_files = sorted(image_files, key=natural_keys)
                for image in image_files:
                    image_path = os.path.join('graphics', 'characters', mob, state, image)
                    image_surface = pygame.image.load(image_path).convert_alpha()
                    self.MOB_ANIMS[mob][state].append(image_surface)

            

        for item in self.ITEM_ANIMS:
            image_files = os.listdir(os.path.join('graphics', 'items', item))
            image_files = sorted(image_files, key=natural_keys)
            for image in image_files:
                image_path = os.path.join('graphics', 'items', item, image)
                image_surface = pygame.image.load(image_path).convert_alpha()
                self.ITEM_ANIMS[item].append(image_surface)

        
        for particle in self.PARTICLE_ANIMS:
            image_files = os.listdir(os.path.join('graphics', 'particles', self.PARTICLE_TYPES[particle], particle))
            image_files = sorted(image_files, key=natural_keys)
            for image in image_files:
                image_path = os.path.join('graphics', 'particles', self.PARTICLE_TYPES[particle], particle, image)
                image_surface = pygame.image.load(image_path).convert_alpha()
                self.PARTICLE_ANIMS[particle].append(image_surface)