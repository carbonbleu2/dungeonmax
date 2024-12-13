from dungeonmax.mobs.character import Character


class Chomper(Character):
    def __init__(self, x, y, animations):
        super().__init__(x, y, animations, 'Chomper', 
                         char_type='enemy', boss=True, size_scale=2,
                         exp_gain=50)
        
        self.rect = self.rect.inflate(-10, 0)
        self.rect.center = (x, y)

        self.max_hp = 100
        self.max_ep = 0
        self.melee_attack = 10
        self.ranged_attack = 0
        self.special_attack = 0
        self.melee_defense = 8
        self.ranged_defense = 8
        self.special_defense = 8

        self.health = self.max_hp
        self.energy = self.max_ep

        self.invincibility_cooldown = 500
        
        self.speed = 3