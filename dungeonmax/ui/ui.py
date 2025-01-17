import textwrap
import pygame

from dungeonmax.settings import *

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, size=UI_FONT_SIZE)

        self.health_bar = pygame.Rect(10, 10, BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar = pygame.Rect(10, 35, BAR_WIDTH, BAR_HEIGHT)

        self.god_to_select = None
        self.item_to_select = None

        self.spell_to_select = None
        self.show_spellbook = False
        self.chosen_spellbook = None

        self.selecting_skill_from_sidepanel = None
        self.hovering_over_skill = {}

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
        pygame.draw.rect(self.display_surface, UI_INFO_PANEL_COLOUR, (0, 0, self.display_surface.width, 100))
        pygame.draw.line(self.display_surface, 'white', (0, 100), (self.display_surface.width, 100))
        self.show_bar(player.health, player.max_hp, self.health_bar, HEALTH_BAR_COLOUR)
        self.show_bar(player.energy, player.max_ep, self.energy_bar, ENERGY_BAR_COLOUR)

        self.draw_text(f"Coins: {player.coins}", 'white', self.display_surface.width - 200, 10)
        self.draw_text(f"Stage: {stage_num}", 'white', self.display_surface.width - 200, 40)
        self.draw_text(f"Level: {player.level}", 'white', self.display_surface.width - 300, 10)
        self.draw_text(f"XP to next level: {player.xp_to_next_level}", 'white', self.display_surface.width - 200, 70)

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
    
    def draw_current_god(self, god):
        rect = pygame.Rect(420, 10, 40, 40)
        pygame.draw.rect(self.display_surface, 'grey', rect)
        pygame.draw.rect(self.display_surface, 'black', rect, 2)
        if god is not None:
            god_image = god.altar_image
            god_rect = god_image.get_rect(center=rect.center)
            self.display_surface.blit(god_image, god_rect)
            return god_rect
        return rect
        
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
            tooltip = pygame.Rect(mouse_pos[0], mouse_pos[1], 200, 100)
            pygame.draw.rect(self.display_surface, '#5e1916', tooltip)
            skill_text = f"{skill.name}\nCost: {skill.cost}\nCooldown: {skill.cooldown}"
            self.draw_text(skill_text, 'white', mouse_pos[0] + 10, mouse_pos[1] + 10)
            self.draw_message_text(skill.description)

    def draw_god_tooltip(self, rect, god):
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            if god is not None:
                tooltip = pygame.Rect(mouse_pos[0], mouse_pos[1], 200, 50)
                pygame.draw.rect(self.display_surface, '#5e1916', tooltip)
                self.draw_text(god.name, 'white', mouse_pos[0] + 10, mouse_pos[1] + 10)
                self.draw_message_text(f"You are a devotee of {god.name}")
            else:
                self.draw_message_text(f"You are not worshipping any gods")
        
    def draw_buffs(self, player):
        for i, (_, buff) in enumerate(player.buffs.items()):
            if buff.active:
                rect = pygame.Rect(11 + 20 * i, 60, 20, 20)
                buff_surface = buff.image
                buff_rect = buff_surface.get_rect(center=rect.center)
                if buff_rect.collidepoint(pygame.mouse.get_pos()):
                    self.draw_message_text(buff.description)
                self.display_surface.blit(buff_surface, buff_rect)

    def draw_message_box(self):
        pygame.draw.rect(self.display_surface, '#3d2328', (0, self.display_surface.height - UI_MESSAGE_BAR_HEIGHT, self.display_surface.width, UI_MESSAGE_BAR_HEIGHT))

    def draw_message_text(self, message):
        font = pygame.font.Font(UI_FONT, UI_MESSAGE_FONT_SIZE)
        message_text = font.render(str(message), False, 'white')
        self.display_surface.blit(message_text, (10, self.display_surface.height - (UI_MESSAGE_BAR_HEIGHT - 5)))

    def draw_religion_selection(self, gods):
        from dungeonmax.gods.gods_enum import GodsRepository

        rect = pygame.Rect(0, 0, self.display_surface.width // 1.5, self.display_surface.height // 1.5)
        rect.center = self.display_surface.get_rect().center
        pygame.draw.rect(self.display_surface, 'grey', rect)
        
        font = pygame.font.Font(UI_FONT, UI_MESSAGE_FONT_SIZE)
        text_instruction = font.render(
            UI_RELIGION_SELECT_INSTRUCTION_TEXT, False, 'black')
        text_instruction_topleft = (rect.left + 10, rect.top + 2)
        text_instruction_rect = text_instruction.get_rect(topleft=text_instruction_topleft)
        self.display_surface.blit(text_instruction, text_instruction_rect)
        
        if len(gods) == 0:
            text_no_gods = font.render(UI_RELIGION_SELECT_NO_GODS_NEARBY, False, 'black')
            text_no_gods_topleft = (rect.left + 10, rect.top + 50)
            text_no_gods_rect = text_instruction.get_rect(topleft=text_no_gods_topleft)
            self.display_surface.blit(text_no_gods, text_no_gods_rect)
        else:
            for i, god in enumerate(list(gods)):
                god_selection_rect = pygame.Rect(rect.left + 10, rect.top + 70 + 50 * (i + 1), rect.width - 10, 50)
                god_selection_rect.centerx = rect.centerx

                god_details = GodsRepository.GODS[god]

                god_image = god_details.altar_image
                god_rect = god_image.get_rect(left=god_selection_rect.left + 20, centery=god_selection_rect.centery)
                self.display_surface.blit(god_image, god_rect)

                god_description = str(god_details.altar_description)
                god_description_text = font.render(god_description, False, 'black')
                god_description_rect = god_description_text.get_rect(
                    left=god_rect.right + 20, centery=god_selection_rect.centery)
                self.display_surface.blit(god_description_text, god_description_rect)

                if god_selection_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.display_surface, 'black', god_selection_rect, 2)
                    if pygame.mouse.get_pressed()[0]:
                        self.draw_text_box(god_details.full_description)
                    self.god_to_select = god
                    

    def draw_text_box(self, text):
        font = pygame.font.Font(UI_FONT, 12)
        rect = pygame.Rect(0, 0, self.display_surface.width // 1.3, self.display_surface.height // 1.3)
        rect.center = self.display_surface.get_rect().center
        text = "\n".join(textwrap.wrap(text, width=80, replace_whitespace=False, fix_sentence_endings=True))
        pygame.draw.rect(self.display_surface, 'grey', rect)
        text_surface = font.render(text, False, 'black')
        text_instruction_topleft = (rect.left + 10, rect.top + 2)
        text_instruction_rect = text_surface.get_rect(topleft=text_instruction_topleft)
        self.display_surface.blit(text_surface, text_instruction_rect)

    def draw_fps(self, fps):
        font = pygame.font.Font(UI_FONT, 12)
        text_fps = font.render(str(int(fps)), False, 'white')
        text_fps_surface = (self.display_surface.width - 50, self.display_surface.height - 50)
        text_fps_rect = text_fps.get_rect(center=text_fps_surface)
        self.display_surface.blit(text_fps, text_fps_rect)

    def draw_inventory(self, inventory):
        rect = pygame.Rect(0, 0, self.display_surface.width // 1.5, self.display_surface.height // 1.5)
        rect.center = self.display_surface.get_rect().center
        pygame.draw.rect(self.display_surface, 'grey', rect)

        inventory_item_names = inventory.get_item_names()
        item_index = 0

        item_count_font = pygame.font.Font(UI_FONT, 8)

        for i in range(0, 10):
            for j in range(0, 7):
                if item_index < len(inventory_item_names):
                    item_name = inventory_item_names[item_index]
                    item = inventory.item_instances[item_name]
                    
                    item_surface = item.image
                    item_rect = item_surface.get_rect(left=rect.left + 10 + 40 * j, top=rect.top + 10 + 40 * i)
                    self.display_surface.blit(item_surface, item_rect)
                    
                    border_rect = pygame.Rect(0, 0, 40, 40)
                    border_rect.center = item_rect.center

                    item_count = inventory.items[item_name]
                    count_text = item_count_font.render(str(item_count), False, 'black')
                    count_rect = count_text.get_rect(right=border_rect.right - 2, top=border_rect.top + 2)
                    self.display_surface.blit(count_text, count_rect)
                    
                    if item_rect.collidepoint(pygame.mouse.get_pos()):
                        pygame.draw.rect(self.display_surface, 'black', border_rect, 2)
                        self.draw_message_text(item.description)
                        self.item_to_select = item_name
                    item_index += 1

    def draw_spellbook(self):
        if self.chosen_spellbook is None and self.show_spellbook:
            return
        
        spellbook = self.chosen_spellbook

        rect = pygame.Rect(0, 0, self.display_surface.width // 1.5, self.display_surface.height // 1.5)
        rect.center = self.display_surface.get_rect().center
        pygame.draw.rect(self.display_surface, 'grey', rect)

        font = pygame.font.Font(UI_FONT, UI_MESSAGE_FONT_SIZE)
        text_instruction = font.render(
            UI_SPELL_SELECT_INSTRUCTION_TEXT, False, 'black')
        text_instruction_topleft = (rect.left + 10, rect.top + 2)
        text_instruction_rect = text_instruction.get_rect(topleft=text_instruction_topleft)
        self.display_surface.blit(text_instruction, text_instruction_rect)

        if len(spellbook.spells) == 0:
            text_no_spells = font.render(UI_SPELL_SELECT_NO_SPELLS, False, 'black')
            text_no_spells_topleft = (rect.left + 10, rect.top + 50)
            text_no_spells_rect = text_instruction.get_rect(topleft=text_no_spells_topleft)
            self.display_surface.blit(text_no_spells, text_no_spells_rect)
        else:
            for i, spell in enumerate(spellbook.spells):
                spell_selection_rect = pygame.Rect(rect.left + 10, rect.top + 70 + 50 * (i + 1), rect.width - 10, 50)
                spell_selection_rect.centerx = rect.centerx

                spell_image = spell.image
                spell_rect = spell_image.get_rect(left=spell_selection_rect.left + 20, centery=spell_selection_rect.centery)
                self.display_surface.blit(spell_image, spell_rect)

                spell_name = str(spell.name)
                spell_name_text = font.render(spell_name, False, 'black')
                spell_name_rect = spell_name_text.get_rect(
                    left=spell_rect.right + 20, centery=spell_selection_rect.centery)
                self.display_surface.blit(spell_name_text, spell_name_rect)

                if spell_selection_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.display_surface, 'black', spell_selection_rect, 2)
                    self.draw_message_text(spell.description)
                    self.spell_to_select = spell

    def draw_skills_sidepanel(self, player, equipment_manager):
        # Arrange skills in a 10x10 grid on the right side of screen
        rect_ = pygame.draw.rect(self.display_surface, BG_COLOUR, (self.display_surface.width - 410, 110, 410, 500))
        text_skills = self.font.render("Skills", False, 'white')
        text_rect = text_skills.get_rect(centerx=rect_.centerx, y=120)
        self.display_surface.blit(text_skills, text_rect)

        pygame.draw.rect(self.display_surface, 'white', rect_, 2)

        for skill in equipment_manager.skills:
            row = equipment_manager.skills.index(skill) // 10
            col = equipment_manager.skills.index(skill) % 10
            skill_surface = skill.image
            skill_rect = skill_surface.get_rect(
                left=self.display_surface.width - 400 + 40 * col, top=150 + 40 * row)
            self.display_surface.blit(skill_surface, skill_rect)
            
            mouse_pos = pygame.mouse.get_pos()
            if skill_rect.collidepoint(mouse_pos):
                self.selecting_skill_from_sidepanel = skill
                self.hovering_over_skill[skill.name] = True
                pygame.draw.rect(self.display_surface, 'white', skill_rect, 2)
                self.draw_message_text(f"{skill.name}: {skill.description}")
            else:
                self.hovering_over_skill[skill.name] = False
            

                    
