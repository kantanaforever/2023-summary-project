# Import statements
import data
# import os

"""call every method here """

class MUDGame:
    def __init__(self):
        self.end = '10'
        self.player = data.Player()
        self.map = data.map
        self.inventory = data.inventory
        self.player_inventory = data.player_inventory
        self.boss = data.Boss()
        # self.game_over = False

    def game_over(self) -> bool:
        return self.player.hp < 0

    def enemy_presence(self, enemy_list):
        return enemy_list != []

    def item_presence(self, items_list):
        return items_list != []

    def room_10(self):
        return self.player.current == self.end

    def input(self, prompt: str) -> str:
        return input(prompt).strip().lower()

    def prompt_valid_choice(self, options, question, errormsg):
        """Prompt the user with a question.
        If the choice is not in options, display errormsg and re-prompt the user.
        If the choice is valid, return player choice.
        """
        choice = self.input(question)
        while choice not in options:
            print(errormsg)
            choice = self.input(question)
        return choice

        
    def movement(self): # can change after game is working
        """ only up down left right, dont show room number"""
    
        #change if zonemap keys of keys has been edited
        keys = ['up', 'down', 'left', 'right']
        available = []
        #extracting up, down, left, right
        
        # remove name and description from choices
        choices = list(self.map[self.player.current].values())[2:]
        
        print('You can move in the following directions: ')
        for i, choice in enumerate(choices):
            if choice != [None]:
                print(f'- {keys[i]}')
                available.append(keys[i])
        direction_choice = self.prompt_valid_choice(
            available,
            question='Which direction do you wish to go to?: ',
            errormsg='You can only move in the above stated direction(s)!'
        )
        # direction_choice = self.input('Which direction do you wish to go to?: ')
        # while direction_choice not in available:
        #     print('You can only move in the above stated direction(s)!')
        #     direction_choice = self.input('Which direction do you wish to go to?: ')
        numpaths = len(choices[keys.index(direction_choice)])
        if numpaths == 1:
            path_choice = 0
        else:    
            path_choices = [str(i) for i in range(1, numpaths + 1)]
            question = f'You entered a corridor, and there are {numpaths} doors...'
            question += '\nThe following are the paths that can be taken: '
            for i in path_choices:
                question += f'\npath {i}'
            question += '\nWhich path do you wish to take? Type the path number: '
            path_choice = self.prompt_valid_choice(path_choices, question, 'You can only take the above stated path(s)!')
        self.player.current = self.map[self.player.current][direction_choice][int(path_choice) - 1]

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
        # 62
        used = []
        print('╔═══════════════════════════════════════════════════════╗')
        print('║                   Inventory Display                   ║')
        print('╟───────────────────────────────────────────────────────╢')
        for j in self.player_inventory:
            if j.name not in used:
                used.append(j.name)
                if j.consumable == True:
                    status = 'Usable'
                else:
                    if j.status == True:
                        status = 'Equipped'
                    else:
                        status = 'carriable'
                count = self.player_inventory.count(j)
                print(f'║{j.name:<20}x{count:<4}{"["+status+"]":<15}{j.magnitude:<5}{"["+j.type+"]":<10}║')
              
        print('╚═══════════════════════════════════════════════════════╝')
 
    def inventory_consume_item(self) -> None:
        """ show inventory"""
        if self.player_inventory == []:
            return "Nothing in inventory!"
        self.inventory_show()
        consume = self.prompt_valid_choice(
            options=['y', 'n'],
            question="Would you like to consume any item?(y/n)?: ",
            errormsg='Not a valid response!'                                
        )
        
        if consume == 'n':
            return None

        else: 
            attributes = [i.name for i in self.player_inventory]
            item = self.prompt_valid_choice(
                options=attributes,
                question="Which item would you like to consume?: ",
                errormsg='Invalid item!'
            )
            
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
                choice = self.prompt_valid_choice(
                    options=['1', '2'],
                    question='The enemy is now in front of you! You can choose to \n1. punch \n2. attack with existing weapons: ',
                    errormsg='Invalid option!'
                )
            
                print(f'{self.player.name} hp: {self.player.hp}')
                print(f'enemy hp: {enemy_list[i].hp}')
                
    
                if choice == '1':
                    self.player.attack_p(enemy_list[i])
                elif choice == '2':
                    self.player.attack_w(enemy_list[i])
    
                enemy_list[i].atk(self.player)
    
                if enemy_list[i].hp <= 0:
                    print('You have defeated the enemy!')
                    
        # if self.player.hp < 0:
        #     self.game_over = True
        
    def pick_item(self, items): # need change
        """ display items in the room"""
        for i in items:
            print(i.name)
            choice = self.prompt_valid_choice(
                options=['y', 'n'],
                question='found! Collect it to help increase your chances of defeating the monsters!(y/n): ',
                errormsg='invalid option!'
                
                
            )

            if choice.lower() == "y":
                data.player_inventory_temp.add_item(i)
                
                
    
    def final_room(self):
        """ print essay -> consume item -> fight"""
        with open('content/finaldesc.txt', 'r') as f:
            for line in f:
                print(line.strip())

    def win(self) -> bool:
        if not self.game_over():
            if self.boss.hp <= 0:
                with open('content/win_desc.txt', 'r') as f:
                    for line in f:
                        print(line.strip())
                    return True
            else:
                return False
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
        # if os.environ.get('DEBUG'):
        #     self.player.current = "10"
        while not self.game_over()  and not self.room_10():
            self.movement()
            self.room_desc(data.Player())
            enemy_list = self.generate_enemy()
            if self.enemy_presence(enemy_list):                    
                print('There is a monster in the room. Defeat them to rescue your sibling from the grasp of dark magic!')
                self.inventory_consume_item()
                self.fight(enemy_list)
            else:
                print("Great save! There are no enemies in this room.")
            if not self.game_over():
                items_list = self.generate_items()
                if self.item_presence(items_list):
                    self.pick_item(items_list)
                    self.inventory_show()
                    print(self.player.current)
                else:
                    print("Aww too bad, there are no items in this room :(")
                    
        self.final_room()            
                
        if not self.win():
            print("You have been defeated >_<")
            return


            
            
    
                    
               
        
        
                

   