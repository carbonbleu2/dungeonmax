import pygame
from dungeonmax.mobs.character import Character
from dungeonmax.particles.skill.fireball import ChomperFireballProjectile, FireballProjectile


class Chomper(Character):
    # How frequent does Chomper fire fireballs?
    # FIREBALL_SHOOTING_RATE_TIME_RANGE measures the time range
    # FIREBALL_SHOOTING_RATE measures the frequency
    # So a FIREBALL_SHOOTING_RATE of 3 with FIREBALL_SHOOTING_RATE_TIME_RANGE
    # of 2000 implies that it will shoot 3 fireballs every 2 seconds

    FIREBALL_SHOOTING_RATE = 3
    FIREBALL_SHOOTING_RATE_TIME_RANGE = 2000
    FIREBALL_START_DISTANCE = 500

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
        self.special_attack = 8
        self.melee_defense = 8
        self.ranged_defense = 8
        self.special_defense = 8

        self.health = self.max_hp
        self.energy = self.max_ep

        self.invincibility_cooldown = 500
        
        self.speed = 2

        self.maintain_distance = 2

        self.attack_range = 5

        self.last_attack = pygame.time.get_ticks()
    
    def ai(self, screen, player, enemies, obstacles, scroll_x, scroll_y):
        fireball_cooldown = self.FIREBALL_SHOOTING_RATE_TIME_RANGE / self.FIREBALL_SHOOTING_RATE

        super().ai(screen, player, enemies, obstacles, scroll_x, scroll_y)

        clipped_line = ()
        fireball = None

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
            self.move(screen, ai_dx, ai_dy, obstacles)
            if dist < self.attack_range and not player.invincible and self.alive:
                player.health -= max(1, self.melee_attack - player.melee_defense)
                player.activate_invincibility()
                player.deactivate_resting()

            if dist < self.FIREBALL_START_DISTANCE:
                if pygame.time.get_ticks() - self.last_attack >= fireball_cooldown:
                    fireball = ChomperFireballProjectile(self.rect.centerx, self.rect.centery, 
                                                         player.rect.centerx, player.rect.centery)
                    self.last_attack = pygame.time.get_ticks()

        return fireball
    
    def on_death(self, player, damage_type):
        super().on_death(player, damage_type)


        