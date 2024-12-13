from dungeonmax.items.item import Item

class HealthPotion(Item):
    def __init__(self, x, y, anims):
        super().__init__(x, y, 'HealthPotion', anims)

class EnergyPotion(Item):
    def __init__(self, x, y, anims):
        super().__init__(x, y, 'EnergyPotion', anims)