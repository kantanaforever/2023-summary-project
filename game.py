# Import statements
import data

"""call every method here """

class MUDGame:
    def __init__(self):
        self.end = 10
        self.player = data.Player(data.map)
        self.enemy = data.Enemy()
        self.map = data.map
        self.inventory = data.Inventory()

    def movement(self):
        """ only up down left right, dont show room number"""
        if self.player.current == self.end:
                print("You have reached the end!")
        else:
            for i in range(10):
                rooms = []
                if self.player.current == self.map.keys(i):
                    rooms.append(self.map[str(i)])
            print("You can move to room(s)"+ str(rooms)+'.')
            next = input("Which room do you wish to move to?")
            if next not in str(rooms):
                print("Unable to move here!")
            else:
                self.move(next)

    def intro(self):
        pass

    def set_username():
        pass

    def desc():
        pass

    def enemy_presence():
        pass
        
    def inventory_consume_item():
        """ show inventory"""
        pass

     def fight(self, Player, Enemy):
        while self.player.hp > 0 and self.enemy.hp > 0:
                self.player.attack(self.enemy)
                self.enemy.attack(self.player)
    def pick_item():
        pass
        
    def __location__():
        pass
        
    def final_room():
        pass

    def game_over():
        pass
    
    def run(self, Player, Enemy):
        """ 
        1. method to call cool intro
        2. set username
        3. movement
        4. if room has enemy then fight (method to check if enemy is inside) , if not pick item
        5. finish fighting -> pick item if any
        6. repeat 3-5 but beffore 4. ask if want to consume item (need method to call inventory)
        7. when reach room 10, fight big big boss -> game over!! 
        """
        self.player.set_username()
        while self.player.hp != 0:
            self.player.movement()
        
            print("YOU HAVE DEFEATED THE ENEMY!")
            self.player.pick_item()
            self.player.consume_item()
        
            
            
            

                
        return "GAME OVER!"
        
        
                    
               
        
        
                

   