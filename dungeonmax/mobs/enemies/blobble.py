from dungeonmax.mobs.character import Character

class Blobble(Character):
    def __init__(self, x, y, animations):
        super().__init__(x, y, animations, 'Blobble')
        
        # self.rect = self.rect.inflate(0, -10)

        self.max_hp = 20
        self.max_ep = 0
        self.melee_attack = 5
        self.ranged_attack = 0
        self.special_attack = 0
        self.melee_defense = 2
        self.ranged_defense = 2
        self.special_defense = 2

        self.health = self.max_hp
        self.energy = self.max_ep

        self.invincibility_cooldown = 300
        
        self.speed = 3