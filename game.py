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
        # later
        print("intro supposed to be here")

    def set_username(self, Player):
        self.player.set_username()

    def room_desc():
        # later
        print("room description supposed to be here")

    def enemy_presence(self):
        return self.map[str(self.player.current)]["enemy"]
        
    def inventory_consume_item(self, Inventory) -> None:
        """ show inventory"""
        if self.player.current != 0:
            print(self.inventory)
            item = input("Which item would you like to consume?")
            self.player.consume_item(item)

    def fight(self, Player, Enemy):
        while self.player.hp > 0 and self.enemy.hp > 0:
                self.player.attack(self.enemy)
                self.enemy.attack(self.player)

    def item_presence(self):
        return self.map[str(self.player.current)]["item"]
        
    def pick_item(self, Player):
        """ display items in the room"""
        item = self.map[str(self.player.current)]["item"]
        input = (str(item) + 'found! Would you like to keep them?')
        if input.upper() == "YES":
            self.player.pick_item(item)
        
    def __location__(self, Player) -> int:
        location = self.player.current
        return location 
    
    def final_room(self, Player):
        """ print essay -> consume item -> fight"""
        print("final room stuff supposed to be here")

    def game_over(self, Player, Enemy) -> str:
        if self.player.current == 10:
            if self.enemy.hp == 0:
                return "You win!"
    
    def run(self, Player, Enemy, Inventory) -> str:
        """ 
        1. method to call cool intro
        2. set username
        3. movement
        4. if room has enemy then fight (method to check if enemy is inside) , if not pick item
        5. finish fighting -> pick item if any
        6. repeat 3-5 but before 4. ask if want to consume item (need method to call inventory)
        7. when reach room 10, fight big big boss -> game over!! 
        """
        self.intro()
        self.set_username(Player)
        while self.player.hp > 0:
            if self.player.current != 10:
                self.movement()
                self.room_desc()
                if self.enemy_presence():
                    self.inventory_consume_item(Inventory)
                    self.fight(Player, Enemy)
                if self.item_presence():
                    self.pick_item(Player)
            else:
                self.final_room(Player)
            return self.game_over(Player, Enemy)
        return "You have been defeated >_<"
           
        
        
        
                
            
            
    
                    
               
        
        
                

   