import os

import pygame
from dungeonmax.buffs.defense_boost import MeleeDefenseBoost
from dungeonmax.particles.skill.warriors_resolve import WarriorsResolveParticle
from dungeonmax.animation_repository import AnimationRepository
from dungeonmax.skills.skill import Skill


class WarriorsResolve(Skill):
    DAMAGE = 0
    COOLDOWN = 10
    CODENAME = "WarriorsResolve"
    SKILL_CATEGORY = "warrior"
    UI_GRAPHIC = os.path.join("graphics", "skills", SKILL_CATEGORY, f"{CODENAME}.png")
    COST = 10
    NAME = "Warrior's Resolve"
    PROJECTILE_SPEED = 0
    DESCRIPTION = "Steel your nerves to increase your melee defense by 30% for 5 seconds"

    EFFECT_DURATION = 5000
    BOOST_PERCENTAGE = 30

    def __init__(self):
        super().__init__(
            self.UI_GRAPHIC, self.NAME, self.SKILL_CATEGORY, 
            self.CODENAME, self.COOLDOWN, self.COST, self.DESCRIPTION
        )

    def on_cast(self, player):
        particle = None
        if player.energy >= self.cost and self.can_be_used:
            super().on_cast(player)
            player.energy = max(player.energy - self.cost, 0)
            self.last_used = pygame.time.get_ticks()
            self.can_be_used = False
            boost = player.melee_defense * 0.30
            buff = MeleeDefenseBoost(player, self.EFFECT_DURATION, boost)
            buff.active = True
            player.add_buff(buff)
            particle = WarriorsResolveParticle(player.rect.centerx, player.rect.centery, player, duration=self.EFFECT_DURATION)

        return particle

    