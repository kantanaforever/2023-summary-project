# Import statements
import json

class Item:
    def __init__(self):
        pass

class Creatures:
    def __init__(self):
        pass

with open("content/items.json", 'r') as f:
    items = json.load(f)