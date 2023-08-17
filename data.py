# Import statements
import json


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
    def __init__(self, map: dict) -> None: # map in json
        self.name = '' # user input
        self.hp = 100
        self.attack = 10
        self.current = 0
        self.turn = False
        self.map = map

    def attack(self, target: object) -> None: # Enemy object
        """
        player deal damage to target
        """
        if self.turn:
            target.hp -= self.attack

    def set_username(self) -> None:
        """
        set self.name to input by user
        """
        self.name = input('What would you like to be called: ')

    def consume_item(self, item):
        self.inventory.pop(self.inventory.index(item))

    def pick_item(self, item):
        self.inventory.append(self.items[item[1]][item[0]])

# Inventory
class Inventory:
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
        with open("content/items.json", 'r') as f:
            self.items = json.load(f)
        self.inventory = []
        # self.equip = None
    

# Items
class Item:
    def __init__(self):
        pass

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
map = _Zonemap('content/zonemap.json')
