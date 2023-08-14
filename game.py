# Import statements
import data

class MUDGame:
    def __init__(self):
        self.start = 0
        self.end = 10
        self.player = data.Player(data.)
        self.enemy = data.Enemy()
        self.map = data.Zonemap()
        self.inventory = data.Inventory()

    def movement(self):
        if self.start == self.end:
                print("You have reached the end!")
        else:
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
        
        while self.hp > 0:
            self.player.attack(self.enemy)
        self.player.pick_item()
        
        self.inventory.use()
        self.inventory.get_items()
        self.player.consume_item()
        
        self.enemy.attack(self.player)
        
        
        
                    
               
        
        
                

   