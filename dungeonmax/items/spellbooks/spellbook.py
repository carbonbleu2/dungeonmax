from dungeonmax.items.item import Item

from dungeonmax.skills.blood import *

class SpellBook(Item):
    def __init__(self, x, y, name, anims, description, spells):
        super().__init__(x, y, name, anims, description)
        self.spells = spells

    # def use(self, player, enemies, equipment_manager, ui):
    #     ui.show_spellbook = True
    #     ui.chosen_spellbook = self
    #     return True
        
    
class SpellBookOfBlood(SpellBook):
    def __init__(self, x, y, anims):
        super().__init__(x, y, 
                         'SpellBookOfBlood', anims, 
                         "Spellbook of Blood: A spellbook containing the blood magic",
                         [Berserk(), Haemorrhage()])
    