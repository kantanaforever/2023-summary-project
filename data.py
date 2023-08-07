# Import statements
import json


# Class Implementation

# Zonemap
class Zonemap:
    def __init__(self, file: str) -> None:
        with open(file, 'r') as f:
            self.map = json.load(f)

# Player
class Player:
    def __init__(self, map: dict) -> None: # map in json
        self.name = '' # user input
        self.hp = 100
        self.attack = 10
        self.current = 0
        self.turn = False
        self.map = map

    def attack(self, target): # Enemy object
        if self.turn:
            target.hp -= self.attack

    def set_username(self):
        self.name = input('What would you like to be called')

    def move(self, direction: str): # up down left right
        self.current = self.map[str(self.current)][direction]

    def consume_item(self):
        pass

    def pick_item(self):
        pass

# Inventory
class Inventory:
    def __init__(self):
        with open("content/items.json", 'r') as f:
            self.items = json.load(f)
        self.inventory = []
        # self.equip = None

    

    def use(self, item):
        self.inventory.pop(self.inventory.index(item))

    def get_items(self, item: tuple):
        self.inventory.append(self.items[item[1]][item[0]])


    

# Items
class Item:
    def __init__(self):
        pass

# Enemy     
class Enemy:
    def __init__(self):
        self.hp = 200
        self.attack = 5
        self.turn = False

    def attack(self, player):
        if self.turn:
            player.hp -= self.attack

class Enemy1(Enemy):
    def __init__(self):
        super().__init__()
    
    def attack(self, player):
        super().attack(player)


# Zonemap callout
map = Zonemap()

# Class instantiation
myPlayer = Player(map)

