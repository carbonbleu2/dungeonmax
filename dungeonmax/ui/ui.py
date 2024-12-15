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
        
        font = pygame.font.Font(STATS_FONT, STATS_FONT_SIZE)

        self.draw_text(str(player.strength), 'white', rect.left + 120, rect.top + 16, font)
        self.draw_text(str(player.dexterity), 'white', rect.left + 120, rect.top + 60, font)
        self.draw_text(str(player.intelligence), 'white', rect.left + 120, rect.top + 104, font)

        self.draw_text(str(player.melee_attack), 'white', rect.left + 160, rect.top + 148, font)
        self.draw_text(str(player.ranged_attack), 'white', rect.left + 160, rect.top + 176, font)
        self.draw_text(str(player.special_attack), 'white', rect.left + 160, rect.top + 208, font)

        self.draw_text(str(player.melee_defense), 'white', rect.left + 352, rect.top + 148, font)
        self.draw_text(str(player.ranged_defense), 'white', rect.left + 352, rect.top + 176, font)
        self.draw_text(str(player.special_defense), 'white', rect.left + 352, rect.top + 208, font)

        self.draw_text(str(player.speed), 'white', rect.left + 441, rect.top + 194, font)

        self.draw_text(str(player.level), 'white', rect.left + 428, rect.top + 22, font)
        self.draw_text(str(player.xp_to_next_level), 'white', rect.left + 428, rect.top + 78, font)



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