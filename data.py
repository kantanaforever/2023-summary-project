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
    + self.attack_punch: (int) Player punch damage per hit
    + self.attack_weapon: (int) Player attack damage per hit
    + self.current: (int) Room number (player position)
   

    Methods
    -------
    + self.set_username() -> None: set self.name to input by user
    + self.attack_p(target: object) -> None: player punch target (object)
    + self.attack_w(target: object) -> None: player weapon target (object)
    """
    def __init__(self) -> None: # map in json
        self.name = '' # user input
        self.hp = 1000
        self.attack_punch = 10
        self.attack_weapon = 10
        self.current = '0'

    def attack_p(self, target: object) -> None: # Enemy object
        target.hp -= self.attack_punch
            
    def attack_w(self, target: object) -> None:
        target.hp -= self.attack_weapon

    def set_username(self) -> None:
        self.name = input('What would you like to be called: ')


    

# Inventory
class _Inventory:
    """ 
    This class encapsulates data for game inventory
    
    Attributes
    -----------
    + self.items: (dicts in dict) Contains contents of json file with items and their characteristics (all items in the game NOT THE PLAYER INVENTORY)
    """
    def __init__(self) -> None:
        self.items = []
        with open("content/items.csv", 'r') as f:
            f.readline()
            for line in f:
                line = line.strip().split(',')
                item = _Item(line[0].strip(), line[1].strip(), bool(True if line[2].strip() == 'True' else False), bool(True if line[3].strip() == 'True' else False), line[4].strip()) #convert strings from csv file to bool
                self.items.append(item)

# Items
class _Item:
    """
    This class encapsulates data for _Item

    Attributes
    -----------
    self.name: (str) name of item
    self.type: (str) type of item
    self.consumable: (str) whether the item is consumable
    self.status: (str) whether item is equipped
    self.magnitude: (str) magnitude of items
    """
    def __init__(self, name: str, type: str, consumable: str, status: str, magnitude: str) -> None:
        self.name  = name
        self.type = type
        self.consumable = consumable
        self.status = status
        self.magnitude = int(magnitude)


class _PlayerInventory:
    """
    This class encapsulates data for Player inventory
    
    Attributes
    ----------
    + self.player_inventory: (objects in a list)
   
    Methods
    -------
    + self.consume_item(item: object) -> None: remove item from inventory upon consumption
    + self.add_item(item: object) -> None: add item to inventory
    """
    def __init__(self) -> None:
        self.player_inventory = []

    def consume_item(self, item: object) -> bool:
        item = item.lower()
        flag = True
        while flag:
            if item in self.player_inventory:
                item_index = self.player_inventory.index(item)
                self.player_inventory.pop(item_index)
                flag = False 
        else:
            print('Invalid item')
            

    def add_item(self, item: object) -> None:
        self.player_inventory.append(item)
        
        

def generate_items() -> list:
    """
    generate random items from 0 to 5, using the game inventory
    """
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
    This class encapsulates data for Enemy
    
    Attributes
    -----------
    + self.hp: (int) enemy hit points (health)
    + self.attack: (int) enemy damage per hit

    Methods
    -------
    + self.atk(Player: class) enemy attack player
    """
    def __init__(self):
        self.hp = 200
        self.attack = 5

    def atk(self, player):
        player.hp -= self.attack

class Enemy1(Enemy):
    """
    This class encapsulates data for Enemy1 and inherits from the enemy class.
    
    Attributes
    -----------
    + self.hp: (int) enemy hit points (health)
    + self.attack: (int) enemy damage per hit

    Methods
    -------
    + self.atk(Player: class) enemy attack player
    """
    def __init__(self):
        super().__init__()
        self.hp = r.randint(100, 200)
        self.attack = r.randint(0, 5)
    
    def atk(self, player):
        super().atk(player)

class Enemy2(Enemy):
    """
    This class encapsulates data for Enemy2 and inherits from the enemy class.
    
    Attributes
    -----------
    + self.hp: (int) enemy hit points (health)
    + self.attack: (int) enemy damage per hit

    Methods
    -------
    + self.atk(Player: class) enemy attack player
    """
    def __init__(self):
        super().__init__()
        self.hp = r.randint(100, 200)
        self.attack = r.randint(0, 5)
    
    def atk(self, player):
        super().atk(player)
        

def generate_enemy() -> list:
    """
    generate random enemies in a room
    """
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
    
class Boss(Enemy):
    """
    Inherited from the Enemy class
    This class encapsulates data for Boss
    
    Attributes
    -----------
    + self.hp: (int) enemy hit points (health)
    + self.attack: (int) enemy damage per hit

    Methods
    -------
    + self.atk(Player: object) enemy attack player
    """
    def __init__(self):
        self.hp = 500
        self.attack = 10

    def atk(self, player: object):
        super().atk(player)
    
class Colours:
    """
    ANSI color codes
    used for UX
    """
    # class attributes
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"

    @staticmethod # functions of the class such that there is no need to insantiate the object
    def colourised(colour, text):
        return colour + text
        
# Zonemap callout
map = _Zonemap('content/zonemap.json').map

# Inventory callout
player_inventory_temp = _PlayerInventory()
player_inventory = player_inventory_temp.player_inventory

inventory = _Inventory().items
