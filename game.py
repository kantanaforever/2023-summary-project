# Import statements
from data import Player, Zonemap

class MUDGame:
    def __init__(self):
        self.start = 0
        self.end = 10
        self.player = Player()
        self.map = Zonemap()
    

    def movement(self):
        if self.start == self.end:
                print("You have reached the end!")
        for i in range(10):
            rooms = []
            if self.start == self.map.keys():
                rooms.append(self.map[str(i)])
        print("You can move to room(s)"+ str(rooms)+'.')
        next = input("Which room do you wish to move to?")
        if next not in str(rooms):
            print("Unable to move here!")
        else:
            self.start = int(next)

    
                    
               
        
        
                

   