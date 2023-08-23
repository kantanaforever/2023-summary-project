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

    def enemy_presence(self, enemy_list):
        return enemy_list != []

    def item_presence(self, items_list):
        return items_list != []

    def not_room_10(self):
        if self.player.current != 10:
            return True
        return False
        
    def movement(self): # can change after game is working
        """ only up down left right, dont show room number"""
    
        #change if zonemap keys of keys has been edited
        keys = ['up', 'down', 'left', 'right']
        available = []
        #extracting up, down, left, right
        choices = [i for i in self.map[self.player.current].values()];choices.pop(0);choices.pop(0)
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

    def intro(self):
        with open('content/intro.txt', 'r') as f:
            for line in f:
                print(line.strip())

    def set_username(self, Player):
        self.player.set_username()

    def room_desc(self, Player):
        desc = self.map[self.player.current]['description']
        print(desc)

    def generate_items(self):
        return data.generate_items()

    def generate_enemy(self):
        return data.generate_enemy()
        
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
        if self.player_inventory == []:
            return "Nothing in inventory!"
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
                    self.player.hp += int(used_item.magnitude)
                    print(f'{used_item.type} has been increased by {used_item.magnitude}. {used_item.type} is now {self.player.hp}')
                elif used_item.type == 'attack':
                    self.player.attack_punch += int(used_item.magnitude)
                    print(f'punch attack has been increased by {used_item.magnitude}. punch attack is now {self.player.attack_punch}')
                    
                self.player_inventory.pop(item_index)
                    
            else:
                print(f'{used_item.name} has been equipped!')
                if used_item.type == 'weapon':
                    prev = self.player.attack_weapon
                    self.player.attack_weapon = used_item.magnitude
                    used_item.status = True
                    print(f'weapon attack was {prev}. weapon attack is now {self.player.attack_weapon}')
            

    def fight(self, enemy_list):
        #if enemy_presence --> choose whether to consume an item --> player attack enemy first then enemy attack player --> if player hp reaches 0 before enemy, player looses --> else continue
        for i in range(len(enemy_list)):
            while self.player.hp > 0 and enemy_list[i].hp > 0:
                choice = input('The enemy is now in front of you! You can choose to \n1. punch \n2. attack with existing weapons: ')
                
                while choice not in ['1', '2']:
                    print('Invalid option!')
                    choice = input('The enemy is now in front of you! You can choose to 1. punch 2. attack with existing weapons: ')

                print(f'{self.player.name} hp: {self.player.hp}')
                print(f'enemy hp: {enemy_list[i].hp}')
                
    
                if choice == '1':
                    self.player.attack_p(enemy_list[i])
                elif choice == '2':
                    self.player.attack_w(enemy_list[i])
    
                enemy_list[i].atk(self.player)
    
                if enemy_list[i].hp <= 0:
                    print('You have defeated the enemy!')
                    
        if self.player.hp < 0:
            self.game_over = True
        
    def pick_item(self, items): # need change
        """ display items in the room"""
        for i in items:
            print(i.name)
            choice = input('found! Collect it to help increase your chances of defeating the monsters!(y/n): ').lower()
            while choice not in ['y', 'n']:
                print('invalid option!')
                choice = input('found! Collect it to help increase your chances of defeating the monsters!(y/n): ').lower()
            if choice.lower() == "y":
                data.player_inventory_temp.add_item(i)
                
                
    
    def final_room(self):
        """ print essay -> consume item -> fight"""
        with open('content/finaldesc.txt', 'r') as f:
            for line in f:
                print(line.strip())

    def win(self) -> str:
        if self.player.current == 10:
            if self.enemy.hp <= 0:
                with open('content/win_desc.txt', 'r') as f:
                    for line in f:
                        print(line.strip())
            return True
        return False
    
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
        self.set_username(data.Player())
        while not self.game_over:
            if self.not_room_10():
                self.movement()
                self.room_desc(data.Player())
                enemy_list = self.generate_enemy()
                if self.enemy_presence(enemy_list):
                    print('There is a monster in the room. Defeat them to rescue your sibling from the grasp of dark magic!')
                    self.inventory_consume_item()
                    self.fight(enemy_list)
                if not self.game_over:
                    items_list = self.generate_items()
                    if self.item_presence(items_list):
                        self.pick_item(items_list)
                        self.inventory_show()
                        
            else:
                self.final_room()
                
        if not self.win():
            print("You have been defeated >_<")

            return
           
        
        
            
            
    
                    
               
        
        
                

   