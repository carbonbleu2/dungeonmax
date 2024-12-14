import pygame
from dungeonmax.mobs.character import Character

class Blobble(Character):
    def __init__(self, x, y, animations):
        super().__init__(x, y, animations, 'Blobble', 
                         char_type='enemy', exp_gain=5)
        
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

        self.maintain_distance = 2
        self.line_of_sight = 50

        self.attack_range = 5

    def on_death(self, player):
        super().on_death(player)

    def ai(self, player, obstacles, scroll_x, scroll_y):
        super().ai(player, obstacles, scroll_x, scroll_y)
        clipped_line = ()

        ai_dx = 0
        ai_dy = 0
        line_of_sight = (self.rect.center, player.rect.center)

        for obstacle in obstacles:
            if obstacle[1].clipline(line_of_sight):
                clipped_line = obstacle[1].clipline(line_of_sight)
        
        dist = pygame.math.Vector2(self.rect.center).distance_to(player.rect.center)
        if not clipped_line:
            if dist > self.maintain_distance:
                if self.rect.centerx > player.rect.centerx:
                    ai_dx = -self.speed
                if self.rect.centerx < player.rect.centerx:
                    ai_dx = self.speed
                if self.rect.centery > player.rect.centery:
                    ai_dy = -self.speed
                if self.rect.centery < player.rect.centery:
                    ai_dy = self.speed

        if self.alive:
            self.move(ai_dx, ai_dy, obstacles)
            if dist < self.attack_range and not player.invincible and self.alive:
                player.health -= max(1, self.melee_attack - player.melee_defense)
                player.activate_invincibility()

        return None



