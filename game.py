# Import statements
from data import Player, Enemy, Zonemap, Inventory

class MUDGame:
    def __init__(self):
        self.start = 0
        self.end = 10
        self.player = Player()
        self.enemy = Enemy()
        self.map = Zonemap()
        self.inventory = Inventory()

    def movement(self):
        if self.start == self.end:
                print("You have reached the end!")
        for i in range(10):
            rooms = []
            if self.start == self.map.keys(i):
                rooms.append(self.map[str(i)])
        print("You can move to room(s)"+ str(rooms)+'.')
        next = input("Which room do you wish to move to?")
        if next not in str(rooms):
            print("Unable to move here!")
        else:
            self.start = int(next)

    def run(self, Player, Enemy):
        self.player.set_username()
        self.player.move()
        self.player.attack(self.enemy)
        self.player.consume_item()
        self.player.pick_item()
        
        self.inventory.use()
        self.inventory.get_items()
        
        self.enemy.attack(self.player)
        
        
        
                    
               
        
        
                

   