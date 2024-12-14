import os
import pprint
import re
import pygame

from dungeonmax.animation_repository import AnimationRepository
from dungeonmax.colour import NamedColour
from dungeonmax.equipment_manager import EquipmentManager
from dungeonmax.items.coin import Coin
from dungeonmax.items.potions import HealthPotion
from dungeonmax.mobs.enemies.blobble import Blobble
from dungeonmax.mobs.player import Player
from dungeonmax.settings import *
from dungeonmax.mobs.character import Character
from dungeonmax.skills.flame.fireball import Fireball
from dungeonmax.skills.warrior.warriors_resolve import WarriorsResolve
from dungeonmax.tiles.stage import Stage
from dungeonmax.tiles.tile_loader import TileLoader
from dungeonmax.ui.damage_text import DamageText
from dungeonmax.ui.ui import UI
from dungeonmax.weapons.bows import RecruitsBow
from dungeonmax.weapons.swords import RecruitsSword

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [atoi(c) for c in re.split(r'(\d+)', text) ]


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)

    clock = pygame.time.Clock()

    _ = AnimationRepository()
    _ = TileLoader()

    stage_num = 1
    stage = Stage()
    stage.read_from_file(f"{stage_num}.csv")

    equipment_manager = EquipmentManager([], [])
    equipment_manager.add_weapon(RecruitsSword())
    equipment_manager.add_weapon(RecruitsBow())

    equipment_manager.add_skill(Fireball())
    equipment_manager.add_skill(WarriorsResolve())

    # weapon = RecruitsBow()
    particles_group = pygame.sprite.Group()
    damage_text_group = pygame.sprite.Group()
    item_group = pygame.sprite.Group()
    enemy_projeciles_group = pygame.sprite.Group()

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

    while run:
        current_weapon = equipment_manager.get_weapon()
        current_skill = equipment_manager.get_skill()

        for skill in equipment_manager.skills:
            skill.update()


        clock.tick(FPS)

        screen.fill(BG_COLOUR)

        player = stage.player

        dx, dy = 0, 0
        if moving_up:
            dy = -player.speed
        elif moving_down:
            dy = player.speed
        if moving_left:
            dx = -player.speed
        elif moving_right:
            dx = player.speed

        screen_scroll_x, screen_scroll_y = player.move(dx, dy, stage.obstacle_tiles)

        stage.update(screen_scroll_x, screen_scroll_y)
        item_group.update(player, screen_scroll_x, screen_scroll_y)

        enemies = stage.npc_list

        for enemy in enemies:
            projectile = enemy.ai(player, stage.obstacle_tiles, screen_scroll_x, screen_scroll_y)
            
            if projectile:
                enemy_projeciles_group.add(projectile)
            
            enemy.update(player)
        player.update(None)

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
        weapon_rect = ui.draw_current_weapon(current_weapon)
        skill_rect = ui.draw_current_skill(current_skill)
        
        ui.draw_weapon_tooltip(weapon_rect, current_weapon)
        ui.draw_skill_tooltip(skill_rect, current_skill)

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
                if event.key == pygame.K_q:
                    equipment_manager.next_weapon()
                if event.key == pygame.K_e:
                    equipment_manager.next_skill()                
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
                    if particle:
                        particles_group.add(particle)
            

        if ui_show_stats:
            ui.draw_stats(player)

        pygame.display.update()

if __name__ == '__main__':
    main()