class Inventory:
    def __init__(self):
        self.items = {}
        self.item_instances = {}

    def add_item(self, item):
        if item.name in self.items:
            self.items[item.name] += 1
            # You can have atmost 99 units of each item
            if self.items[item.name] >= 99:
                self.items[item.name] = 99
        else:
            self.items[item.name] = 1
        self.item_instances[item.name] = item
    
    def update(self, player):
        for item in list(self.items.items()):
            if item[1] == 0:
                del self.items[item[0]]
                del self.item_instances[item[0]]

    def get_item_names(self):
        return list(self.items.keys())
    
    def use_item(self, name, player, enemies, equipment_manager, ui):
        if name in self.items:
            used = self.item_instances[name].use(player, enemies, equipment_manager, ui)
            if used:
                self.items[name] -= 1
            self.update(player)

    def remove_item(self, item, player):
        if item.name in self.items:
            self.items[item.name] = 0
            self.update(player)