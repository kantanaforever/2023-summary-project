# Import statements
import csv
import json
import random

import color


with open('content/zonemap.json', 'r') as f:
    map = json.load(f)


# Class Implementation

# Items
class Item:
    """This class encapsulates data for Item

    Attributes
    -----------
    self.name: (str) name of item
    self.type: (str) type of item
    self.equipped: (str) whether item is equipped
    self.magnitude: (str) magnitude of items
    """
    def __init__(self, name: str, magnitude: int) -> None:
        self.name  = name
        self.equipped = False
        self.magnitude = magnitude


class Consumable(Item):
    """A Consumable is removed from inventory when used"""


class HP(Consumable):
    """HP items increase HP when consumed"""
    def __init__(self, name: str, magnitude: int) -> None:
        super().__init__(name, magnitude)
    

class Attack(Consumable):
    """Attack items increase attack when consumed"""
    def __init__(self, name: str, magnitude: int) -> None:
        super().__init__(name, magnitude)
    

class Equippable(Item):
    """An Equippable is equipped in inventory when used"""


class Weapon(Equippable):
    """A weapon boosts the user's attack when equipped"""
    def __init__(self, name: str, magnitude: int) -> None:
        super().__init__(name, magnitude)


inventory = []
with open("content/items.csv", 'r') as f:
    for record in csv.DictReader(f):
        # Record is a dict with column headers as keys, row data as values
        # The ** operator unpacks a dict into keyword arguments
        consumable = bool(record.pop("consumable"))
        type_ = record.pop("type")
        record["magnitude"] = int(record["magnitude"])        
        if consumable:
            if type_ == "hp":
                item = HP(**record)
            elif type_ == "attack":
                item = Attack(**record)
            else:
                item = Consumable(**record)
        else:
            if type_ == "weapon":
                item = Weapon(**record)
            else:
                item = Equippable(**record)
        inventory.append(item)


class Inventory:
    """This class encapsulates data for Player inventory
    
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
        
    def get_item(self, name: str) -> Item | None:
        """Returns the first item matching name, without removing it
        from inventory.
        """
        for item in self._data:
            if item.name == name:
                return item
        return None

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def item_names(self) -> list[str]:
        """Returns a list of item names in the inventory"""
        return [item.name for item in self._data]

    def show(self):
        """displays the player's inventory"""
        used = []
        print(color.light_white('╔═══════════════════════════════════════════════════════╗'))
        print(color.light_white('║                   Inventory Display                   ║'))
        print(color.light_white('╟───────────────────────────────────────────────────────╢'))
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
                print(color.light_white(f'║{j.name:<20}x{count:<4}{"["+status+"]":<15}{j.magnitude:<5}{"["+j.type+"]":<10}║')) # formating for inventory
              
        print(color.light_white('╚═══════════════════════════════════════════════════════╝'))

    def unequip_all(self) -> None:
        for item in self._data:
            if item.equipped == True:
                item.equipped = False

    def use_item(self, name: str) -> Item | None:
        """Finds the first item matching name.
        Removes it from inventory if consumable.
        Equips it if equippable.
        Returns the item if found, otherwise returns None.
        """
        for i, item in enumerate(self._data):
            if item.name == name:
                if isinstance(item, Consumable):
                    del self._data[i]
                elif isinstance(item, Equippable):
                    item.equipped = True
                return item
        return None


class Combatant:
    """A combatant has HP and is dead when HP drops to 0 or below.

    Attributes
    ----------
    + name: str
      Combatant's name
    + hp: int
      Combatant's hit points (health)

    Methods
    -------
    + is_dead() -> bool:
    + take_damage(dmg: int) -> None
    """
    def __init__(self, name: str, hp: int):
        self.name = name
        self.hp = hp

    def is_dead(self) -> bool:
        return self.hp <= 0

    def take_damage(self, dmg: int) -> None:
        # In future, might want to do validation here
        self.hp -= dmg


class Player(Combatant):
    """This class encapsulates data for Player
    
    Attributes
    ----------
    + self.name: (str) Player username
    + self.attack_punch: (int) Player punch damage per hit
    + self.attack_weapon: (int) Player attack damage per hit
    + self.current: (int) Room number (player position)
   

    Methods
    -------
    + self.set_username(name: str) -> None
    + self.attack_p(target: object) -> None: player punch target (object)
    + self.attack_w(target: object) -> None: player weapon target (object)
    """
    def __init__(self, name: str, hp: int) -> None: # map in json
        super().__init__(name, hp)
        self.attack_punch = 10
        self.attack_weapon = 10
        self.current = '0'
        self.inventory = Inventory()

    def take_item(self, item: Item) -> None:
        self.inventory.add_item(item)

    def use_item(self, name: str) -> Item | None:
        """Use item with the given name, applying its effects to the player.
        Return the item used, or None if not found.
        """
        item = self.inventory.use_item(name)
        if isinstance(item, HP):
            self.hp += item.magnitude
        elif isinstance(item, Attack):
            self.attack_punch += item.magnitude
        elif isinstance(item, Weapon):
            self.inventory.unequip_all()
            self.attack_weapon = item.magnitude
        return item


# Enemy     
class Enemy(Combatant):
    """This class encapsulates data for Enemy
    
    Attributes
    -----------
    + self.attack: (int) enemy damage per hit
    """
    def __init__(self, name: str = "enemy", hp: int = 200, attack: int = 5):
        super().__init__(name, hp)
        self.attack = attack


def generate_items() -> list[Item]:
    """generate random items from 0 to 5, using the game inventory"""
    num_of_items = random.randint(0, 5)
    items_list = []
    for i in range(num_of_items):
        items_list.append(random.choice(inventory))

    return items_list
    

def generate_enemy() -> list[Enemy]:
    """generate random enemies in a room"""
    enemy_list = []
    num_of_enemies = random.randint(0, 5)
    for i in range(num_of_enemies):
        enemy_list.append(Enemy(random.randint(100, 200), random.randint(0, 5)))
    return enemy_list
