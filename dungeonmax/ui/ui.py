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

    def draw_text(self, text, colour, x, y, font=None):
        if font is None:
            font = self.font
        image = font.render(text, False, colour)
        self.display_surface.blit(image, (x, y))

    def draw_info(self, player, stage_num):
        pygame.draw.rect(self.display_surface, UI_INFO_PANEL_COLOUR, (0, 0, SCREEN_WIDTH, 100))
        pygame.draw.line(self.display_surface, 'white', (0, 100), (SCREEN_WIDTH, 100))
        self.show_bar(player.health, player.max_hp, self.health_bar, HEALTH_BAR_COLOUR)
        self.show_bar(player.energy, player.max_ep, self.energy_bar, ENERGY_BAR_COLOUR)

        self.draw_text(f"Coins: {player.coins}", 'white', SCREEN_WIDTH - 200, 10)
        self.draw_text(f"Stage: {stage_num}", 'white', SCREEN_WIDTH - 200, 40)
        self.draw_text(f"Level: {player.level}", 'white', SCREEN_WIDTH - 300, 10)
        self.draw_text(f"XP to next level: {player.xp_to_next_level}", 'white', SCREEN_WIDTH - 200, 70)

    def draw_stats(self, player):
        image = pygame.image.load(STATS_SCREEN).convert_alpha()
        rect = image.get_rect()
        rect.center = self.display_surface.get_rect().center
        self.display_surface.blit(image, rect)
        
        self.draw_stat(player, 'strength', rect, 108, 20, 52, 20, font_size=20)
        self.draw_stat(player, 'dexterity', rect, 108, 64, 52, 20, font_size=20)
        self.draw_stat(player, 'intelligence', rect, 108, 108, 52, 20, font_size=20)

        self.draw_stat(player, 'melee_attack', rect, 144, 152, 48, 16, font_size=20)
        self.draw_stat(player, 'ranged_attack', rect, 144, 180, 48, 16, font_size=20)
        self.draw_stat(player, 'special_attack', rect, 144, 212, 48, 16, font_size=20)

        self.draw_stat(player, 'melee_defense', rect, 336, 152, 57, 16, font_size=20)
        self.draw_stat(player, 'ranged_defense', rect, 336, 180, 57, 16, font_size=20)
        self.draw_stat(player, 'special_defense', rect, 336, 212, 57, 16, font_size=20)

        self.draw_stat(player, 'speed', rect, 404, 184, 88, 44, font_size=30)
        self.draw_stat(player, 'level', rect, 392, 20, 92, 28, font_size=25)
        self.draw_stat(player, 'xp_to_next_level', rect, 392, 76, 92, 28, font_size=25)

    def draw_stat(self, player, stat_name, stat_rect, 
                  rel_left, rel_top, rect_width, rect_height, 
                  font_size=STATS_FONT_SIZE):
        if hasattr(player, stat_name):
            stat = getattr(player, stat_name)
            font = pygame.font.Font(STATS_FONT, font_size)
            rect = pygame.rect.Rect(stat_rect.left + rel_left, stat_rect.top + rel_top, rect_width, rect_height)
            text = font.render(str(stat), False, 'white')
            text_rect = text.get_rect(center=(rect.left + rect.width // 2, rect.top + rect.height // 2))
            self.display_surface.blit(text, text_rect)

    def draw_current_weapon(self, weapon):
        rect = pygame.Rect(320, 10, 40, 40)
        pygame.draw.rect(self.display_surface, 'grey', rect)
        pygame.draw.rect(self.display_surface, 'black', rect, 2)
        weapon_surface = weapon.graphic
        weapon_rect = weapon_surface.get_rect(center=rect.center)
        self.display_surface.blit(weapon_surface, weapon_rect)
        return weapon_rect

    def draw_current_skill(self, skill): 
        rect = pygame.Rect(370, 10, 40, 40)
        pygame.draw.rect(self.display_surface, 'grey', rect)
        pygame.draw.rect(self.display_surface, 'black', rect, 2)
        skill_surface = skill.image
        skill_rect = skill_surface.get_rect(center=rect.center)
        self.display_surface.blit(skill_surface, skill_rect)
        if skill.time_left_till_next_use > 0:
            self.draw_text(str(skill.time_left_till_next_use), 'black', skill_rect.centerx - 10, 56)
        return skill_rect
        
    def draw_weapon_tooltip(self, rect, weapon):
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            tooltip = pygame.Rect(mouse_pos[0], mouse_pos[1], 200, 50)
            pygame.draw.rect(self.display_surface, '#5e1916', tooltip)
            self.draw_text(weapon.name, 'white', mouse_pos[0] + 10, mouse_pos[1] + 10)
            self.draw_message_text(weapon.description)

    def draw_skill_tooltip(self, rect, skill):
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            tooltip = pygame.Rect(mouse_pos[0], mouse_pos[1], 200, 50)
            pygame.draw.rect(self.display_surface, '#5e1916', tooltip)
            self.draw_text(skill.name, 'white', mouse_pos[0] + 10, mouse_pos[1] + 10)
            self.draw_message_text(skill.description)
        
    def draw_buffs(self, player):
        for i, (_, buff) in enumerate(player.buffs.items()):
            if buff.active:
                rect = pygame.Rect(11 + 18 * i, 60, 18, 18)
                buff_surface = buff.image
                buff_rect = buff_surface.get_rect(center=rect.center)
                if buff_rect.collidepoint(pygame.mouse.get_pos()):
                    self.draw_message_text(buff.description)
                self.display_surface.blit(buff_surface, buff_rect)

    def draw_message_box(self):
        pygame.draw.rect(self.display_surface, '#3d2328', (0, SCREEN_HEIGHT - UI_MESSAGE_BAR_HEIGHT, SCREEN_WIDTH, UI_MESSAGE_BAR_HEIGHT))

    def draw_message_text(self, message):
        font = pygame.font.Font(UI_FONT, UI_MESSAGE_FONT_SIZE)
        message_text = font.render(str(message), False, 'white')
        self.display_surface.blit(message_text, (10, SCREEN_HEIGHT - (UI_MESSAGE_BAR_HEIGHT - 5)))