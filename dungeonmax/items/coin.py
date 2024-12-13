from dungeonmax.items.item import Item

class Coin(Item):
    def __init__(self, x, y, anims):
        super().__init__(x, y, 'Coin', anims)