# Import statements
import data

"""call every method here """

class MUDGame:
    def __init__(self):
        self.end = 10
        self.player = data.Player(data.map)
        self.enemy = data.Enemy()
        self.inventory = data.Inventory()

    def movement(self): # can change after game is working
        """ only up down left right, dont show room number"""
    
        #change if zonemap keys of keys has been edited
        keys = ['up', 'down', 'left', 'right']
        #extracting up, down, left, right
        choices = [i for i in self.player.map[self.player.current].values()].pop(0).pop()
        print('You can move in the following directions: ')
        for index1, i in enumerate(keys):
            print(f'{index1+1}. {i}')
        direction_choice = input('Which direction do you wish to go to?: ').strip().lower()
        while direction_choice not in keys:
            print('You can only move up, down, left or right!')
            direction_choice = input('Which direction do you wish to go to?: ').strip().lower()
        numpaths = len(choices[keys.find(direction_choice)])
        if numpaths > 1:
            print(f'You entered a corridor, and there are {numpaths} doors...')
            print('The following are the paths that can be taken')
            for i in range(1, len(numpaths) + 1):
                print(f'path {i}')
            path_choice = input('Which path do you wish to take? Type the path number.').strip().lower()
            while path_choice not in keys:
                print('You can only take the above paths listed!')
                path_choice = input('Which path do you wish to take? Type the path number.').strip().lower()
            self.player.current = self.player.map[self.player.current][direction_choice][int(path_choice) - 1]
        else:
            self.player.current = self.player.map[self.player.current][direction_choice][0]

    def intro(self):
        # later
        print("intro supposed to be here")

    def set_username(self, Player):
        self.player.set_username()

    def room_desc():
        # later
        print("room description supposed to be here")

    def enemy_presence(self):
        return self.player.map[self.player.current]["enemy"]

    def inventory_show(self): # can seperately implement in a class
        # 56
        used = []
        print('╔══════════════════════════════════════════════════════════╗')
        print('║                   Inventory Display                      ║')
        print('╟──────────────────────────────────────────────────────────╢')
        for i, j in enumerate(self.inventory.inventory):
            name = j.name
            if name not in used:
                used.append(name)
                if j.consumable == True:
                    status = 'Usable'
                else:
                    if j.status == True:
                        status = 'Equipped'
                    else:
                        status = 'carriable'
                desc = self.inventory.items[j.type][j.name][j.description]
                count = self.inventory.inventory.count(j)
                print(f'║{i+1:<6}{name:<16}x{count:<4}{"["+status+"]":<12}{desc:^19}║')
              
    print('╚══════════════════════════════════════════════════════════╝')
    
    def inventory_consume_item(self, Inventory) -> None:
        """ show inventory"""
        if self.enemy_presence():
            self.inventory_show()
            item = input("Which item would you like to consume?")
            self.player.consume_item(item)

    def fight(self, Player, Enemy):
        while self.player.hp > 0 and self.enemy.hp > 0:
                self.player.attack(self.enemy)
                self.enemy.attack(self.player)

    def item_presence(self):
        return self.map[str(self.player.current)]["item"]
        
    def pick_item(self, Player): # need change
        """ display items in the room"""
        item = self.map[str(self.player.current)]["item"]
        input = (str(item) + 'found! Would you like to keep them?')
        if input.upper() == "YES":
            self.player.pick_item(item)
        
    def __location__(self) -> int:
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
           
        
        
        
                
            
            
    
                    
               
        
        
                

   