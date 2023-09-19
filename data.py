# Import statements
import json
import random as r


with open('content/zonemap.json', 'r') as f:
    map = json.load(f)


# Class Implementation

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
    + self.set_username(name: str) -> None
    + self.attack_p(target: object) -> None: player punch target (object)
    + self.attack_w(target: object) -> None: player weapon target (object)
    """
    def __init__(self) -> None: # map in json
        self.name = ''
        self.hp = 1000
        self.attack_punch = 10
        self.attack_weapon = 10
        self.current = '0'

    def attack_p(self, target: object) -> None: # Enemy object
        target.hp -= self.attack_punch
            
    def attack_w(self, target: object) -> None:
        target.hp -= self.attack_weapon


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


inventory = []
with open("content/items.csv", 'r') as f:
    f.readline()
    for line in f:
        line = line.strip().split(',')
        item = _Item(line[0].strip(), line[1].strip(), bool(True if line[2].strip() == 'True' else False), bool(True if line[3].strip() == 'True' else False), line[4].strip()) #convert strings from csv file to bool
        inventory.append(item)


class _PlayerInventory:
    """
    This class encapsulates data for Player inventory
    
    Attributes
    ----------
    - data: list[Item]
   
    Methods
    -------
    + self.consume_item(item: object) -> None: remove item from inventory upon consumption
    + self.add_item(item: object) -> None: add item to inventory
    """
    def __init__(self) -> None:
        self._data = []

    def add_item(self, item: object) -> None:
        self._data.append(item)
        
    def consume_item(self, item: object) -> bool:
        item = item.lower()
        flag = True
        while flag:
            if item in self._data:
                item_index = self._data.index(item)
                self._data.pop(item_index)
                flag = False 
        else:
            print('Invalid item')
            
    def show(self):
        """displays the player's inventory"""
        used = []
        print(Colours.colourised(Colours.LIGHT_WHITE, ('╔═══════════════════════════════════════════════════════╗')))
        print(Colours.colourised(Colours.LIGHT_WHITE, ('║                   Inventory Display                   ║')))
        print(Colours.colourised(Colours.LIGHT_WHITE, ('╟───────────────────────────────────────────────────────╢')))
        for j in self._data:
            if j.name not in used:
                used.append(j.name)
                if j.consumable == True:
                    status = 'Usable'
                else:
                    if j.status == True:
                        status = 'Equipped'
                    else:
                        status = 'carriable'
                count = self._data.count(j)
                print(Colours.colourised(Colours.LIGHT_WHITE, (f'║{j.name:<20}x{count:<4}{"["+status+"]":<15}{j.magnitude:<5}{"["+j.type+"]":<10}║'))) # formating for inventory
              
        print(Colours.colourised(Colours.LIGHT_WHITE, ('╚═══════════════════════════════════════════════════════╝')))

    def unequip_all(self) -> None:
        for item in self._data:
            if item.status == True:
                item.status = False

        

def generate_items() -> list:
    """
    generate random items from 0 to 5, using the game inventory
    """
    num_of_items = r.randint(0, 5)
    items_list = []
    for i in range(num_of_items):
        items_list.append(r.choice(inventory))

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
