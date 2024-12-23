from dungeonmax.items.item import Item

class HealthPotion(Item):
    def __init__(self, x, y, anims):
        super().__init__(x, y, 'HealthPotion', anims, "Health Potion: A potion that restores 20 health points")

    def use(self, player, enemies, equipment_manager, ui):
        if player.health == player.max_hp:
            return False
        player.health += 20
        if player.health > player.max_hp:
            player.health = player.max_hp
        return True

class EnergyPotion(Item):
    def __init__(self, x, y, anims):
        super().__init__(x, y, 'EnergyPotion', anims, "Energy Potion: A potion that restores 20 energy points")

    def use(self, player, enemies, equipment_manager):
        if player.energy == player.max_ep:
            return False
        player.energy += 20
        if player.energy > player.max_ep:
            player.energy = player.max_ep
        return True