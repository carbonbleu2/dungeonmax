import pygame

class Weapon:
    def __init__(self, image, name, codename, ui_graphic, attack_speed, description):
        self.name = name
        self.original_image = pygame.image.load(image).convert_alpha()
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.graphic = pygame.image.load(ui_graphic).convert_alpha()

        self.weapon_type = None

        self.last_used = pygame.time.get_ticks()

        self.codename = codename

        self.attack_speed = attack_speed

        self.description = description