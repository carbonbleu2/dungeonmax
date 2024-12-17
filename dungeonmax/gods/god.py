import pygame

class God:
    def __init__(self, name, altar_image, altar_description, 
                 level1_threshold, level2_threshold, 
                 level3_threshold, level4_threshold, 
                 level5_threshold,
                 favour=0):
        self.name = name
        self.altar_image = altar_image
        self.altar_description = altar_description
        self.favour = favour
        self.abandoned = False
        self.active = False

        self.player = None

        self.level1_threshold = level1_threshold
        self.level2_threshold = level2_threshold
        self.level3_threshold = level3_threshold
        self.level4_threshold = level4_threshold
        self.level5_threshold = level5_threshold

    def set_player(self, player):
        self.player = player

    def join_religion(self):
        from dungeonmax.gods import GodsRepository

        joinable = (not self.abandoned) or \
            (self.abandoned and not GodsRepository.cannot_rejoin(self.name))

        if joinable:
            self.active = True
            self.abandoned = False
            self.favour = 1

    def abandon_religion(self):
        self.abandoned = True
        self.active = False

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

    def punish(self, equipment_manager, enemies, stage, event=None):
        pass

    def update(self, equipment_manager, enemies, stage, event=None):
        if self.abandoned:
            self.favour = 0
        if self.favour <= 0:
            self.abandon_religion()
            self.punish(equipment_manager, enemies, stage, event=event)

        levels = [
            (self.level1_threshold, self.level1_perk),
            (self.level2_threshold, self.level2_perk),
            (self.level3_threshold, self.level3_perk),
            (self.level4_threshold, self.level4_perk),
            (self.level5_threshold, self.level5_perk)
        ]

        for threshold, perk in levels:
            if self.favour >= threshold:
                perk(equipment_manager, enemies)
        