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
        "WarriorsResolveParticle": "support",
        "ChomperFireballProjectile": "fire",
        "HaemoblobProjectile": "blood",
        "ProfuseBleedingParticle": "blood"
    }

    # Make each entry one line
    MOB_ANIMS = {
        "Blobble": {"idle": [], "run": []},
        "Chomper": {"idle": [], "run": []},
        "Player": {"idle": [], "run": []},
        "CaveBat": {"idle": [], "run": []},
        "BloodWolf": {"idle": [], "run": []}
    }
        
    ITEM_ANIMS = {
        "Coin": [],
        "HealthPotion": [],
        "EnergyPotion": []
    }   

    PARTICLE_ANIMS = {
        "WarriorsResolveParticle": [],
        "ProfuseBleedingParticle": []
    }

    PROJECTILE_ANIMS = {
        "FireballProjectile": [],
        "WoodenArrow": [],
        "ChomperFireballProjectile": [],
        "HaemoblobProjectile": []
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

        for projectile in self.PROJECTILE_ANIMS:
            image_files = os.listdir(os.path.join('graphics', 'particles', self.PARTICLE_TYPES[projectile], projectile))
            image_files = sorted(image_files, key=natural_keys)
            for image in image_files:
                image_path = os.path.join('graphics', 'particles', self.PARTICLE_TYPES[projectile], projectile, image)
                image_surface = pygame.image.load(image_path).convert_alpha()
                self.PROJECTILE_ANIMS[projectile].append(image_surface)