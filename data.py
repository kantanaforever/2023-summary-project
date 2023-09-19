# Import statements
import csv
import json
import random

import color
from text import title_box


# Constants
DIRECTIONS = ('up', 'down', 'left', 'right')
WIDTH = 55
FIRST_ROOM = "0"
LAST_ROOM = "10"


class Room:
    """Encapsulates data for a game location.

    Attributes
    ----------
    + name: str
    + description: str
    + paths: dict[str, str | list]
    """
    def __init__(self, name: str, description: str, paths: dict={}):
        self.name = name
        self.description = description
        self.paths = paths


def room_from_dict(record: dict) -> Room:
    name = record.pop("name")
    description = record.pop("description")
    # Remaining keys should be directions only
    return Room(name, description, paths=record)
    

with open('content/zonemap.json', 'r') as f:
    map_data = json.load(f)

map = {}
for key, record in map_data.items():
    map[key] = room_from_dict(record)

def get_room(key: str) -> Room:
    return map[key]


# Items
class Item:
    """This class encapsulates data for Item

    Attributes
    -----------
    + name: str
      name of item
    + magnitude: int
      magnitude of items

    Methods
    -------
    + status() -> str
    """
    def __init__(self, name: str, magnitude: int) -> None:
        self.name  = name
        self.magnitude = magnitude

    def status(self) -> str:
        return self.name


class Consumable(Item):
    """A Consumable is removed from inventory when used"""


class HP(Consumable):
    """HP items increase HP when consumed"""
    

class Attack(Consumable):
    """Attack items increase attack when consumed"""
    

class Equippable(Item):
    """An Equippable is equipped in inventory when used

    Attributes
    ----------
    + equipped: bool
      whether item is equipped
    """
    def __init__(self, name: str, magnitude: int) -> None:
        super().__init__(name, magnitude)
        self.equipped = False

    def status(self) -> str:
        return self.name + (" (Equipped)" if self.equipped else "")


class Weapon(Equippable):
    """A weapon boosts the user's attack when equipped"""


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
    + add_item(item: Item) -> None
    + get_item(name: str) -> Item | None
    + has_item(name: str) -> int
    + is_empty() -> bool
    + item_names() -> list[str]
    + show() -> None
    + unequip_all() -> None
    + use_item(name: str) -> Item | None
    """
    def __init__(self) -> None:
        self._data = []

    def add_item(self, item: object) -> None:
        self._data.append(item)
        
    def count_item(self, name: str) -> int:
        """Returns the number of items with the name in inventory."""
        count = 0
        for item in self._data:
            if item.name == name:
                count += 1
        return count

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

    def item_report(self, item: Item) -> str:
        """Return a detailed item report"""
        return f'{self.count_item(item.name):>4}× {item.status()} (strength: {item.magnitude})'

    def show(self) -> None:
        """displays the player's inventory"""
        contents = [self.item_report(item) for item in self._data]
        print(color.light_white(
            title_box("Inventory Display ", contents, width=WIDTH)
        ))

    def unequip_all(self) -> None:
        for item in self._data:
            if item.equipped is True:
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
    for _ in range(num_of_enemies):
        enemy_list.append(Enemy(
            name="enemy",
            hp=random.randint(100, 200),
            attack=random.randint(0, 5),
        ))
    return enemy_list
