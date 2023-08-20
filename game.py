# Import statements
import data

"""call every method here """

class MUDGame:
    def __init__(self):
        self.end = 10
        self.player = data.Player()
        self.map = data.map
        self.inventory = data.inventory
        self.player_inventory = data.player_inventory
        self.game_over = False
        

    def movement(self): # can change after game is working
        """ only up down left right, dont show room number"""
    
        #change if zonemap keys of keys has been edited
        keys = ['up', 'down', 'left', 'right']
        available = []
        #extracting up, down, left, right
        choices = [i for i in self.map[self.player.current].values()];choices.pop(0);choices.pop()
        print('You can move in the following directions: ')
        for index, i in enumerate(choices):
            if i != [None]:
                print(f'- {keys[index]}')
                available.append(keys[index])
        direction_choice = input('Which direction do you wish to go to?: ').strip().lower()
        while direction_choice not in available:
            print('You can only move in the above stated direction(s)!')
            direction_choice = input('Which direction do you wish to go to?: ').strip().lower()
        numpaths = len(choices[keys.index(direction_choice)])
        if numpaths > 1:
            print(f'You entered a corridor, and there are {numpaths} doors...')
            print('The following are the paths that can be taken: ')
            for i in range(1, numpaths + 1):
                print(f'path {i}')
            path_choice = input('Which path do you wish to take? Type the path number: ').strip().lower()
            while path_choice not in [str(i) for i in range(1, numpaths + 1)]:
                print('You can only take the above stated path(s)!')
                path_choice = input('Which path do you wish to take? Type the path number: ').strip().lower()
            self.player.current = self.map[self.player.current][direction_choice][int(path_choice) - 1]
        else:
            self.player.current = self.map[self.player.current][direction_choice][0]
        print(self.player.current)

    def intro(self):
        # later
        print("intro supposed to be here")

    def set_username(self, Player):
        self.player.set_username()

    def room_desc():
        # later
        print("room description supposed to be here")

    def enemy_presence(self):
        return self.map[self.player.current]["enemy"]

    def inventory_show(self): # can seperately implement in a class
        # 57
        used = []
        print('╔══════════════════════════════════════════════════════════╗')
        print('║                   Inventory Display                      ║')
        print('╟──────────────────────────────────────────────────────────╢')
        for i, j in enumerate(self.player_inventory):
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
                count = self.player_inventory.count(j)
                print(f'║{i+1:<6}{name:<16}x{count:<4}{"["+status+"]":<19}{"["+j.type+"]":<12}║')
              
        print('╚══════════════════════════════════════════════════════════╝')
    
    def inventory_consume_item(self) -> None:
        """ show inventory"""
        if True: #enemy_presence
            self.inventory_show()
            consume = input("Would you like to consume any item?(y/n)?: ").lower()
            while consume not in ['y', 'n']:
                print('Not a valid response!')
                consume = input("Would you like to consume any item?(y/n)?: ").lower()
            if consume == 'n':
                return None

            else: 
                item = input("Which item would you like to consume?: ").lower()
                attributes = [i.name for i in self.player_inventory]
                while item not in attributes:
                    print('Invalid item!')
                    item = input("Which item would you like to consume?: ")
                item_index = attributes.index(item)
                used_item = self.player_inventory[item_index]
                if used_item.consumable == True:
                    print(f'{used_item.name} has been consumed!')
                    if used_item.type == 'hp':
                        self.player.hp += used_item.magnitude
                        print(f'{used_item.type} has been increased by {used_item.magnitude}. {used_item.type} is now {self.player.hp}')
                    elif used_item.type == 'attack':
                        self.player.attack_punch += used_item.magnitude
                        print(f'punch attack has been increased by {used_item.magnitude}. punch attack is now {self.player.attack_punch}')
                        
                    self.player_inventory.pop(item_index)
                        
                else:
                    print(f'{used_item.name} has been equipped!')
                    if used_item.type == 'weapon':
                        prev = self.player.attack_weapon
                        self.player.attack_weapon = used_item.magnitude
                        used_item.status = True
                        print(f'weapon attack was {prev}. weapon attack is now {self.player.attack_weapon}')
                

    def fight(self):
        #if enemy_presence --> choose whether to consume an item --> player attack enemy first then enemy attack player --> if player hp reaches 0 before enemy, player looses --> else continue
        enemy = data.Enemy()
        while self.player.hp > 0:
            choice = input('The enemy is now in front of you! You can choose to 1. punch 2. attack with existing weapons')
            
            while choice not in ['1', '2']:
                print('Invalid option!')
                choice = input('The enemy is now in front of you! You can choose to 1. punch 2. attack with existing weapons')

            if choice == '1':
                self.player.attack_punch(enemy)
            elif choice == '2':
                self.player.attack_weapon(enemy)

            enemy.attack(self.player)

            if enemy.hp <= 0:
                print('You have defeated the enemy!')
                return None

        self.game_over = True
    
    def item_presence(self):
        return self.map[str(self.player.current)]["item"]
        
    def pick_item(self, item_data): # need change
        """ display items in the room"""
        item = item_data["name"]
        input = (item + 'found! Would you like to keep it?')
        if input.lower() == "yes":
            self.player.pick_item(item)
        
    def __location__(self) -> int:
        location = self.player.current
        return location 
    
    def final_room(self):
        """ print essay -> consume item -> fight"""
        print("final room stuff supposed to be here")

    def win(self) -> str:
        if self.player.current == 10:
            if self.enemy.hp <= 0:
                return "You win!"
    
    def run(self) -> str:
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
        self.set_username()
        while not self.game_over:
            if self.player.current != 10:
                self.movement()
                self.room_desc()
                if self.enemy_presence():
                    self.inventory_consume_item()
                    self.fight()
                if self.item_presence():
                    self.pick_item()
            else:
                self.final_room()
            return self.win()
        return "You have been defeated >_<"
           
        
        
        
                
            
            
    
                    
               
        
        
                

   