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

    animation_repository = AnimationRepository()

    player = Player(300, 400, AnimationRepository.MOB_ANIMS)
    
    equipment_manager = EquipmentManager([], [])
    equipment_manager.add_weapon(RecruitsSword())
    equipment_manager.add_weapon(RecruitsBow())

    equipment_manager.add_skill(Fireball())
    equipment_manager.add_skill(WarriorsResolve())

    enemies = []

    enemy = Blobble(200, 300, AnimationRepository.MOB_ANIMS)
    enemies.append(enemy)

    # weapon = RecruitsBow()
    particles_group = pygame.sprite.Group()
    damage_text_group = pygame.sprite.Group()
    item_group = pygame.sprite.Group()

    potion1 = HealthPotion(400, 600, AnimationRepository.ITEM_ANIMS)
    item_group.add(potion1)
    coin1 = Coin(200, 200, AnimationRepository.ITEM_ANIMS)
    item_group.add(coin1)

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

        dx, dy = 0, 0
        if moving_up:
            dy = -player.speed
        elif moving_down:
            dy = player.speed
        if moving_left:
            dx = -player.speed
        elif moving_right:
            dx = player.speed

        player.move(dx, dy)
        
        item_group.update(player)

        for enemy in enemies:
            enemy.update()
        player.update()

        particle = current_weapon.update(player)
        
        if particle:
            particles_group.add(particle)  
        for particle in particles_group:
            damage, damage_pos = particle.update(enemies, player)
            if damage > 0:
                damage_text_group.add(
                    DamageText(damage_pos.centerx, damage_pos.y, damage, DAMAGE_TEXT_COLOUR)
                )
        damage_text_group.update()

        for enemy in enemies:
            if enemy.alive:
                enemy.draw(screen)
        player.draw(screen)
        current_weapon.draw(screen)

        print(player.melee_defense)

        for arrow in particles_group:
            arrow.draw(screen)

        item_group.draw(screen)
        damage_text_group.draw(screen)

        ui.draw_info(player)
        ui.draw_current_weapon(current_weapon)
        ui.draw_current_skill(current_skill)
        ui.draw_buffs(player)

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
