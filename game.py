# Import statements
import data

class MUDGame:
    def __init__(self):
        self.start = 0
        self.end = 10
        self.player = data.Player(data.map)
        self.enemy = data.Enemy()
        self.map = data.map
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
        """ defeat boss -> pick item  -> give option to use on next boss ?? """
        self.player.set_username()
        while self.player.hp != 0:
            self.player.movement()
            while self.enemy.hp > 0:
                self.player.attack(self.enemy)
                self.enemy.attack(self.player)
            print("YOU HAVE DEFEATED THE ENEMY!")
            
            

                
        return "GAME OVER!"
        
        
                    
               
        
        
                

   