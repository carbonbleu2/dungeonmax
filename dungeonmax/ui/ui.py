import pygame

from dungeonmax.settings import *

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, size=UI_FONT_SIZE)

        self.health_bar = pygame.Rect(10, 10, BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar = pygame.Rect(10, 35, BAR_WIDTH, BAR_HEIGHT)

    def show_bar(self, current_amount, max_amount, bg_rect, colour):
        pygame.draw.rect(self.display_surface, BAR_BG_COLOUR, bg_rect)
        ratio = current_amount / max_amount
        current_amount_width = bg_rect.width * ratio
        current_amount_rect = bg_rect.copy()
        current_amount_rect.width = current_amount_width
        text_surface = self.font.render(f"{int(current_amount)}/{max_amount}", False, BAR_FG_COLOUR)
        pygame.draw.rect(self.display_surface, colour, current_amount_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOUR, bg_rect, 2)
        text_rect = text_surface.get_rect(center = bg_rect.center)
        self.display_surface.blit(text_surface, text_rect)

    def draw_text(self, text, colour, x, y):
        image = self.font.render(text, False, colour)
        self.display_surface.blit(image, (x, y))

    def draw_info(self, player):
        pygame.draw.rect(self.display_surface, UI_INFO_PANEL_COLOUR, (0, 0, SCREEN_WIDTH, 80))
        pygame.draw.line(self.display_surface, 'white', (0, 80), (SCREEN_WIDTH, 80))
        self.show_bar(player.health, player.max_hp, self.health_bar, HEALTH_BAR_COLOUR)
        self.show_bar(player.energy, player.max_ep, self.energy_bar, ENERGY_BAR_COLOUR)

        self.draw_text(f"Coins: {player.coins}", 'white', SCREEN_WIDTH - 100, 10)

    def draw_stats(self, player):
        rect = pygame.Rect(0, 0, 700, 500)
        rect.center = self.display_surface.get_rect().center
        pygame.draw.rect(self.display_surface, UI_INFO_PANEL_COLOUR, rect)

    def draw_current_weapon(self, weapon):
        rect = pygame.Rect(320, 10, 45, 45)
        pygame.draw.rect(self.display_surface, 'black', rect, 2)
        weapon_surface = weapon.graphic
        weapon_rect = weapon_surface.get_rect(center=rect.center)
        self.display_surface.blit(weapon_surface, weapon_rect)

    def draw_current_skill(self, skill): 
        rect = pygame.Rect(370, 10, 45, 45)
        pygame.draw.rect(self.display_surface, 'black', rect, 2)
        skill_surface = skill.image
        skill_rect = skill_surface.get_rect(center=rect.center)
        self.display_surface.blit(skill_surface, skill_rect)
        if skill.time_left_till_next_use > 0:
            self.draw_text(str(skill.time_left_till_next_use), 'black', skill_rect.centerx - 10, 56)
        
    def draw_buffs(self, player):
        buff_start = 390
        for i, (_, buff) in enumerate(player.buffs.items()):
            if buff.active:
                rect = pygame.Rect(450 + 18 * i, 10, 18, 18)
                buff_surface = buff.image
                buff_rect = buff_surface.get_rect(center=rect.center)
                self.display_surface.blit(buff_surface, buff_rect)

        