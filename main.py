import re
import pygame

from dungeonmax.animation_repository import AnimationRepository
from dungeonmax.equipment_manager import EquipmentManager
from dungeonmax.gods.gods_enum import GodsRepository
from dungeonmax.gods.trog import Trog
from dungeonmax.screenfade import FadeType, ScreenFade
from dungeonmax.settings import *
from dungeonmax.skills.flame.fireball import Fireball
from dungeonmax.skills.warrior.warriors_resolve import WarriorsResolve
from dungeonmax.tiles.stage import Stage
from dungeonmax.tiles.tile_loader import TileLoader
from dungeonmax.ui.damage_text import DamageText
from dungeonmax.ui.ui import UI
from dungeonmax.weapons.bows import RecruitsBow
from dungeonmax.weapons.swords import RecruitsSword
from dungeonmax.button import Button

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [atoi(c) for c in re.split(r'(\d+)', text) ]

def distance(rect_1, rect_2):
    return pygame.Vector2(rect_1.center).distance_to(rect_2.center)

def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)

    clock = pygame.time.Clock()

    restart_button_image = os.path.join("graphics", "buttons", "restart.png")

    _ = AnimationRepository()
    _ = TileLoader()
    _ = GodsRepository()

    stage_num = 1
    stage = Stage()
    stage.read_from_file(f"{stage_num}.csv")

    start_intro = True

    equipment_manager = EquipmentManager([], [])
    equipment_manager.add_weapon(RecruitsSword())
    equipment_manager.add_weapon(RecruitsBow())

    # equipment_manager.add_skill(Fireball())
    equipment_manager.add_skill(WarriorsResolve())

    # weapon = RecruitsBow()
    particles_group = pygame.sprite.Group()
    damage_text_group = pygame.sprite.Group()
    item_group = pygame.sprite.Group()
    enemy_projeciles_group = pygame.sprite.Group()

    all_enemies_dead = False

    def reset_level():
        particles_group.empty()
        damage_text_group.empty()
        item_group.empty()
        enemy_projeciles_group.empty()

        stage = Stage()
        return stage

    for item in stage.item_list:
        item_group.add(item)

    screen_scroll_x = 0
    screen_scroll_y = 0

    run = True

    moving_up = False
    moving_down = False
    moving_left = False
    moving_right = False

    ui = UI()

    ui_show_stats = False
    ui_show_religion_selection = False

    intro_fade = ScreenFade(FadeType.WHOLE_SCREEN, NamedColour.BLACK.value, 10)
    gameover_fade = ScreenFade(FadeType.CURTAIN_FALL, NamedColour.RED.value, 10)

    restart_button = Button(SCREEN_WIDTH // 2 - 74, SCREEN_HEIGHT // 2 - 74, restart_button_image)

    nearby_gods = set()

    paused = False

    current_god = None

    while run:
        current_weapon = equipment_manager.get_weapon()
        current_skill = equipment_manager.get_skill()

        for skill in equipment_manager.skills:
            skill.update()

        clock.tick(FPS)

        screen.fill(BG_COLOUR)

        player = stage.player

        god_tiles = stage.god_tiles

        if player.alive and not paused:
            if current_god is not None:
                if not current_god.active:
                    current_god = None

            dx, dy = 0, 0
            if moving_up:
                dy = -player.speed
            elif moving_down:
                dy = player.speed
            if moving_left:
                dx = -player.speed
            elif moving_right:
                dx = player.speed

            screen_scroll_x, screen_scroll_y, level_complete = player.move(dx, dy, stage.obstacle_tiles, stage.portal_tile)

            stage.update(screen_scroll_x, screen_scroll_y)
            item_group.update(player, screen_scroll_x, screen_scroll_y)

            enemies = stage.npc_list

            for enemy in enemies:
                projectile = enemy.ai(player, stage.obstacle_tiles, screen_scroll_x, screen_scroll_y)
                
                if projectile:
                    enemy_projeciles_group.add(projectile)
                
                enemy.update(player)

            all_enemies_dead = all([not enemy.alive for enemy in enemies])

            player.update(None)

            for god in GodsRepository.GODS:
                GodsRepository.GODS[god].set_player(player)
                if GodsRepository.GODS[god].active:
                    current_god = GodsRepository.GODS[god]
                if GodsRepository.GODS[god].active or GodsRepository.GODS[god].abandoned:
                    GodsRepository.GODS[god].update(equipment_manager, enemies, stage)

            particle = current_weapon.update(player)
            
            if particle:
                particles_group.add(particle)  
            for particle in particles_group:
                damage, damage_pos = particle.update(enemies, player, stage.obstacle_tiles, screen_scroll_x, screen_scroll_y)
                if damage > 0:
                    damage_text_group.add(
                        DamageText(damage_pos.centerx, damage_pos.y, damage, DAMAGE_TEXT_COLOUR)
                    )

            for enemy_projectile in enemy_projeciles_group:
                enemy_projectile.update(enemies, player, stage.obstacle_tiles, screen_scroll_x, screen_scroll_y)

            damage_text_group.update(screen_scroll_x, screen_scroll_y)

        stage.draw(screen)

        for enemy in enemies:
            if enemy.alive:
                enemy.draw(screen)
        player.draw(screen)
        current_weapon.draw(screen)

        for projectile in particles_group:
            projectile.draw(screen)

        for enemy_projectile in enemy_projeciles_group:
            enemy_projectile.draw(screen)

        item_group.draw(screen)
        damage_text_group.draw(screen)

        ui.draw_info(player, stage_num)
        ui.draw_message_box()

        god_rect = ui.draw_current_god(current_god)
        weapon_rect = ui.draw_current_weapon(current_weapon)
        skill_rect = ui.draw_current_skill(current_skill)
        ui.draw_weapon_tooltip(weapon_rect, current_weapon)
        ui.draw_skill_tooltip(skill_rect, current_skill)
        ui.draw_buffs(player)

        for god_tile in god_tiles:
            if distance(player.rect, god_tile[1]) <= 2 * TILE_SIZE:
                nearby_gods.add(god_tile[2])
                if len(nearby_gods) > 0:
                    
                    god_descriptions = ", ".join([
                        GodsRepository.GODS[g].altar_description for g in nearby_gods
                    ])
                    ui.draw_message_text("You see {}".format(god_descriptions))
            else:
                if god_tile[2] in nearby_gods:
                    nearby_gods.remove(god_tile[2])

        if level_complete:
            if all_enemies_dead:
                start_intro = True
                stage_num += 1
                stage = reset_level()
                stage.read_from_file(f"{stage_num}.csv")

                for god in GodsRepository.GODS:
                    GodsRepository.GODS[god].set_player(player)
                    if GodsRepository.GODS[god].active or GodsRepository.GODS[god].abandoned:
                        GodsRepository.GODS[god].update(equipment_manager, enemies, stage, event='new_stage')

                temp_health = player.health
                temp_energy = player.energy
                temp_strength = player.strength
                temp_intelligence = player.intelligence
                temp_dexterity = player.dexterity
                temp_total_xp = player.total_xp
                temp_xp_to_next_level = player.xp_to_next_level     
                temp_max_hp = player.max_hp
                temp_max_ep = player.max_ep
                temp_melee_attack = player.melee_attack
                temp_ranged_attack = player.ranged_attack
                temp_special_attack = player.special_attack
                temp_melee_defense = player.melee_defense
                temp_ranged_defense = player.ranged_defense
                temp_special_defense = player.special_defense
                temp_speed = player.speed
                temp_coins = player.coins
                temp_level = player.level
                temp_health_regen_rate = player.health_regen_rate
                temp_energy_regen_rate = player.energy_regen_rate

                player = stage.player
                enemies = stage.npc_list

                player.health = temp_health
                player.energy = temp_energy
                player.strength = temp_strength
                player.intelligence = temp_intelligence
                player.dexterity = temp_dexterity
                player.total_xp = temp_total_xp
                player.xp_to_next_level = temp_xp_to_next_level     
                player.max_hp = temp_max_hp
                player.max_ep = temp_max_ep
                player.melee_attack = temp_melee_attack
                player.ranged_attack = temp_ranged_attack
                player.special_attack = temp_special_attack
                player.melee_defense = temp_melee_defense
                player.ranged_defense = temp_ranged_defense
                player.special_defense = temp_special_defense
                player.speed = temp_speed
                player.coins = temp_coins
                player.level = temp_level
                player.health_regen_rate = temp_health_regen_rate
                player.energy_regen_rate = temp_energy_regen_rate

                for item in stage.item_list:
                    item_group.add(item)
            else:
                ui.draw_message_text("You must kill all enemies to proceed to the next stage")

        if start_intro:
            if intro_fade.fade(screen):
                start_intro = False
                intro_fade.fade_counter = 0

        if not player.alive:
            if gameover_fade.fade(screen):
                if restart_button.draw(screen):
                    gameover_fade.fade_counter = 0
                    start_intro = True
                    start_intro = True
                    stage_num = 1
                    stage = reset_level()
                    stage.read_from_file(f"{stage_num}.csv")
                    player = stage.player
                    enemies = stage.npc_list

                    current_god = None

                    for god in GodsRepository.GODS:
                        GodsRepository.GODS[god].reset()

                    for item in stage.item_list:
                        item_group.add(item)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    moving_left = True
                if event.key == pygame.K_d:
                    moving_right = True
                if event.key == pygame.K_w:
                    moving_up = True
                if event.key == pygame.K_s:
                    moving_down = True
                if event.key == pygame.K_TAB:
                    ui_show_stats = not ui_show_stats
                    paused = ui_show_stats
                if event.key == pygame.K_q:
                    equipment_manager.next_weapon()
                if event.key == pygame.K_e:
                    equipment_manager.next_skill()     
                if event.key == pygame.K_z:
                    ui_show_religion_selection = not ui_show_religion_selection   
                    paused = ui_show_religion_selection
                if event.key == pygame.K_f and ui.god_to_select:
                    if current_god is not None and current_god.name != ui.god_to_select:
                        GodsRepository.GODS[current_god.name].abandon_religion() 
                    GodsRepository.GODS[ui.god_to_select].join_religion()
                    paused = False
                    ui_show_stats = False
                    ui_show_religion_selection = False
                if event.key == pygame.K_x:
                    if current_god is not None:
                        GodsRepository.GODS[current_god.name].abandon_religion() 
                if event.key == pygame.K_ESCAPE:
                    paused = False
                    ui_show_stats = False
                    ui_show_religion_selection = False   
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    moving_left = False
                if event.key == pygame.K_d:
                    moving_right = False
                if event.key == pygame.K_w:
                    moving_up = False
                if event.key == pygame.K_s:
                    moving_down = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    particle = current_skill.on_cast(player)
                    player.deactivate_resting()
                    if particle:
                        particles_group.add(particle)
            
        if ui_show_stats:
            ui.draw_stats(player)

        if ui_show_religion_selection:
            ui.draw_religion_selection(nearby_gods)

        pygame.display.update()

if __name__ == '__main__':
    main()
