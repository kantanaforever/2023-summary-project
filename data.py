# Import statements
import json
import random as r


# Class Implementation

# Zonemap
class _Zonemap:
    """
    This class encapsulates data for Zonemap
    
    Attributes
    -----------
    + self.map: (dicts in dict) contains contents of json file with rooms and their characteristics
    """
    def __init__(self, file: str) -> None:
        with open(file, 'r') as f:
            self.map = json.load(f)

# Player
class Player:
    """
    This class encapsulates data for Player
    
    Attributes
    ----------
    + self.name: (str) Player username
    + self.hp: (int) Player hit points (health)
    + self.attack: (int) Player damage per hit
    + self.current: (int) Room number (player position)
    + self.turn: (bool) Whether it is player turn
    + self.map: (dicts in dict) Contains contents of json file with rooms and their characteristics

    Methods
    -------
    + self.attack(target: object) -> None: player deal damage to target
    + self.set_username() -> None: set self.name to input by user
    + self.move(direction: str) -> None: shift player to desired room (up, down, left or right), update self.current based on room number
    + self.consume_item(item: tuple, inventory: object) -> None: Use the item specified, removing the item from the inventory
    + self.pick_item(item: tuple, inventory: object) -> None: Pick up item specified, adding the item to the inventory
    """
    def __init__(self) -> None: # map in json
        self.name = '' # user input
        self.hp = 1000
        self.attack_punch = 10
        self.attack_weapon = 10
        self.current = '0'

    def attack_p(self, target: object) -> None: # Enemy object
        """
        player deal damage to target
        """
        target.hp -= self.attack_punch
            
    def attack_w(self, target: object) -> None:
        target.hp -= self.attack_weapon

    def set_username(self) -> None:
        """
        set self.name to input by user
        """
        self.name = input('What would you like to be called: ')


    

# Inventory
class _Inventory:
    """
    This class encapsulates data for...
    Attributes
    -----------
    + self.items: (dicts in dict) Contains contents of json file with items and their characteristics (all items in the game NOT THE PLAYER INVENTORY)
    + self.inventory: (list) contains items that users have picked up

    Methods
    --------
    + self.use(item: tuple) -> None: use items from inventory
    + self.get_items(item: tuple) -> None: pick up items in rooms
    """
    def __init__(self):
        self.items = []
        with open("content/items.csv", 'r') as f:
            f.readline()
            for line in f:
                line = line.strip().split(',')
                item = _Item(line[0].strip(), line[1].strip(), bool(line[2].strip()), bool(line[3].strip()), line[4].strip())
                self.items.append(item)
                
        
        
        # self.equip = None
    

# Items
class _Item:
    def __init__(self, name, type, consumable, status, magnitude):
        self.name  = name
        self.type = type
        self.consumable = consumable
        self.status = status
        self.magnitude = magnitude


class _PlayerInventory:
    def __init__(self):
        self.player_inventory = []

    def consume_item(self, item):
        item = item.lower()
        flag = True
        while flag:
            if item in self.player_inventory:
                item_index = self.player_inventory.index(item)
                self.player_inventory.pop(item_index)
                flag = False
        else:
            print('Invalid item')
            

    def add_item(self, item_data):
        # item_data is in the following format: {'name':'elixer', 'type':'hp', 'consumable':True, 'status':False}
        # item = _Item(line[0], line[1], line[2], line[3], line[4])
        # return item
        
        self.player_inventory.append(item_data)
        
        

def generate_items():
    inventory = _Inventory()
    game_inventory = inventory.items
    num_of_items = r.randint(0,5)
    items_list = []
    for i in range(num_of_items):
        items_list.append(r.choice(game_inventory))

    return items_list
    

# Enemy     
class Enemy:
    """
    This class encapsulates data for...
    Attributes
    -----------
    + self.hp: (int) enemy hit points (health)
    + self.attack: (int) enemy damage per hit

    """
    def __init__(self):
        self.hp = 200
        self.attack = 5

    def atk(self, player):
        player.hp -= self.attack

class Enemy1(Enemy):
    def __init__(self):
        super().__init__()
        self.hp = r.randint(100, 200)
        self.attack = r.randint(0, 5)
    
    def atk(self, player):
        super().atk(player)

class Enemy2(Enemy):
    def __init__(self):
        super().__init__()
        self.hp = r.randint(100, 200)
        self.attack = r.randint(0, 5)
    
    def atk(self, player):
        super().atk(player)
        

def generate_enemy() -> list:
    """generate random enemies in a room"""
    enemy_list = []
    enemy1 = Enemy1()
    enemy2 = Enemy2()
    num_of_enemies = r.randint(0, 5)
    for i in range(num_of_enemies):
        flag = r.choice([True, False])
        if flag:
            enemy_list.append(enemy1)
        else:
            enemy_list.append(enemy2)
    return enemy_list
    
    

# Zonemap callout
map = _Zonemap('content/zonemap.json')
map = map.map

# Inventory callout
player_inventory_temp = _PlayerInventory()
player_inventory = player_inventory_temp.player_inventory

inventory = _Inventory()
inventory = inventory.items
