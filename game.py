# Import statements
import data
from data import Colours

"""call every method here """

class MUDGame:
    def __init__(self):
        """This class encapsulates data for MUDGame
                    
        Attributes
        -----------
        + self.end: contains the final room number
        + self.player: contains the Player class
        + self.map: contains json file with rooms and their characteristics
        + self.inventory: contins the inventory class
        + self.player_inventory: contains the player's inventory
        + self.boss: contains the Boss class
        """
        self.end = '10'
        self.player = data.Player()
        self.map = data.map
        # self.inventory = data.inventory
        self.player_inventory = data.player_inventory
        self.boss = data.Boss()

    def game_over(self) -> bool:
        """returns True if player's hp is less than 0
        otherwise returns False
        """
        return self.player.hp < 0

    def enemy_presence(self, enemy_list):
        """checks if any enemies is present in the room
        """
        return enemy_list != []

    def item_presence(self, items_list):
        """checks if any items are present in the room
        """
        return items_list != []

    def room_10(self):
        """checks if player is at room 10
        """
        return self.player.current == self.end

    def input(self, prompt: str) -> str:
        """strips the empty spaces and changes the input to lower case
        """
        return input(prompt).strip().lower()

    def prompt_valid_choice(self, options, question, errormsg, col):
        """Prompt the user with a question.
        If the choice is not in options, display errormsg and re-prompt the user.
        If the choice is valid, return player choice.
        """
        choice = self.input(question)
        while choice not in options:
            print(Colours.colourised(Colours.RED, errormsg))
            choice = self.input(Colours.colourised(col, question))
        return choice

        
    def movement(self): # can change after game is working
        """Displays the direction that the player can travel in
        If there are more than one paths in that direction, prompts user to select a path
        Prints the name of the room
        """
    
        #change if zonemap keys of keys has been edited
        keys = ['up', 'down', 'left', 'right']
        available = []
        #extracting up, down, left, right
        
        # remove name and description from choices
        choices = list(self.map[self.player.current].values())[2:]
        
        print(Colours.colourised(Colours.BLUE,'\nYou can move in the following directions: \n'))
        for i, choice in enumerate(choices):
            if choice != [None]:
                print(f'- {keys[i]}')
                available.append(keys[i])
        direction_choice = self.prompt_valid_choice(
            available,
            question='\nWhich direction do you wish to go to?: ',
            errormsg='\nYou can only move in the above stated direction(s)!',
            col = Colours.BLUE
        )
        numpaths = len(choices[keys.index(direction_choice)])
        if numpaths == 1:
            path_choice = 0
        else:    
            path_choices = [str(i) for i in range(1, numpaths + 1)]
            question = f'\nYou entered a corridor, and there are {numpaths} doors...\n'
            question += '\nThe following are the paths that can be taken: '
            for i in path_choices:
                question += f'\npath {i}'
            question += '\nWhich path do you wish to take? Type the path number: '
            path_choice = self.prompt_valid_choice(path_choices, question, '\nYou can only take the above stated path(s)!', col=Colours.BLUE)
        self.player.current = self.map[self.player.current][direction_choice][int(path_choice) - 1] #  updating the player position 
        print(Colours.colourised(Colours.DARK_GRAY,'\n' * 3 + 'You are now in the '+ self.map[self.player.current]["name"] + '!\n')) # printing the name of the room

    
    def intro(self):
        """prints the introduction to the game"""
        with open('content/intro.txt', 'r') as f:
            for line in f:
                print(Colours.colourised(Colours.DARK_GRAY, line), end= '')

    def ask_username(self):
        """prompts and sets the player's username"""
        name = self.input('What would you like to be called: ')
        self.player.name = name

    def room_desc(self, Player):
        """prints the description for the room the player is in
        """
        desc = self.map[self.player.current]['description']
        print(Colours.colourised(Colours.BROWN, f'\n{desc}'))

    def is_equipped(self):
        """if player wishes to equip another weapon, 
        unquip the initial one and equip the new one 
        """
        for i in self.player_inventory:
            if i.status == True:
                i.status = False
        return 
        
 
    def inventory_consume_item(self) -> None:
        """Display the inventory to the player
        Prompt the player if they want to comsume any items from their inventory.
        """
        if self.player_inventory == []:
            print(Colours.colourised(Colours.RED, "\nNothing in inventory!\n"))
            return
        self.player_inventory.show()
        consume = self.prompt_valid_choice(
            options=['y', 'n'],
            question="Would you like to equip/consume any item?(y/n)?: ",
            errormsg='\nNot a valid response!\n',
            col= Colours.LIGHT_GREEN
        )
        
        if consume == 'n':
            return None

        else: 
            attributes = [i.name for i in self.player_inventory]
            item = self.prompt_valid_choice(
                options=attributes,
                question="Which item would you like to equip/consume?: ",
                errormsg='Invalid item!',
                col=Colours.LIGHT_GREEN
            )
            
            item_index = attributes.index(item)
            used_item = self.player_inventory[item_index]
            if used_item.consumable == True:
                print(Colours.colourised(Colours.BLUE, (f'{used_item.name} has been consumed!')))
                if used_item.type == 'hp':
                    self.player.hp += int(used_item.magnitude)
                    print(Colours.colourised(Colours.BLUE, (f'{used_item.type} has been increased by {used_item.magnitude}. {used_item.type} is now {self.player.hp}')))
                elif used_item.type == 'attack':
                    self.player.attack_punch += int(used_item.magnitude)
                    print(Colours.colourised(Colours.BLUE, (f'punch attack has been increased by {used_item.magnitude}. punch attack is now {self.player.attack_punch}')))
                    
                self.player_inventory.pop(item_index)
                    
            else:
                print(Colours.colourised(Colours.BLUE, (f'{used_item.name} has been equipped!')))
                if used_item.type == 'weapon':
                    self.is_equipped()
                    prev = self.player.attack_weapon
                    self.player.attack_weapon = used_item.magnitude
                    used_item.status = True
                    print(Colours.colourised(Colours.BLUE, (f'weapon attack was {prev}. weapon attack is now {self.player.attack_weapon}')))
            
    def fight(self, enemy_list):
        #if enemy_presence -> choose whether to consume an item -> player attack enemy first then enemy attack player -> if player hp reaches 0 before enemy, player looses -> else continue
        """
        The player and enemy take turns to attack each other until one of their hp is less than 0
        """
        for i in range(len(enemy_list)):
            
            while self.player.hp > 0 and enemy_list[i].hp > 0:
                print(Colours.colourised(Colours.PURPLE, (f'\n{self.player.name} hp: {self.player.hp}')))
                print(Colours.colourised(Colours.GREEN, (f'enemy hp: {enemy_list[i].hp}')))
                choice = self.prompt_valid_choice(
                    options=['1', '2'],
                    question='\nThe enemy is now in front of you! You can choose to \n1. punch \n2. attack with existing weapons: ',
                    errormsg='\nInvalid option!',
                    col=Colours.LIGHT_GREEN
                )
            
    
                if choice == '1':
                    self.player.attack_p(enemy_list[i])
                elif choice == '2':
                    self.player.attack_w(enemy_list[i])
                
                enemy_list[i].atk(self.player)
    
                if enemy_list[i].hp <= 0:
                    print(Colours.colourised(Colours.LIGHT_WHITE, ('\nYou have defeated the enemy!\n')))
                    if i < len(enemy_list) - 1:
                        print("Another enemy has entered...")
                    
        
    def pick_item(self, items): 
        """Displays the item available in the room"""
        for i in items:
            item = Colours.colourised(Colours.YELLOW, i.name)
        #print(self.colour...item)
            choice = self.prompt_valid_choice(
                options=['y', 'n'],
                question=f'\n{item} found! Collect it to help increase your chances of defeating the monsters!(y/n):',
                errormsg='\ninvalid option!\n',
                col= Colours.LIGHT_GREEN
            )

            if choice.lower() == "y":
                data.player_inventory_temp.add_item(i)
                
                
    
    def final_room(self):
        """Display the story text for the final room.
        Prompt the player if they would like to consume any items.
        Make the player fight the enemy
        """
        with open('content/finaldesc.txt', 'r') as f:
            for line in f:
                print(Colours.colourised(Colours.DARK_GRAY, (line.strip())))

    def final_boss_fight(self):
        """player and final boss take turns to attack each other""" 
        print(Colours.colourised(Colours.PURPLE, (f'{self.player.name} hp: {self.player.hp}')))           
        print(Colours.colourised(Colours.GREEN, (f'boss hp: {self.boss.hp}\n')))
        while self.player.hp > 0 and self.boss.hp > 0:
            choice = self.prompt_valid_choice(
                options=['1','2'],
                question = 'The enemy is now in front of you! You can choose to \n1. punch \n2. attack with existing weapons: ',
                errormsg='\nInvalid option\n',
                col= Colours.LIGHT_GREEN
                )
            
            if choice == '1':
                self.player.attack_p(self.boss)
            else:
                self.player.attack_w(self.boss)

            self.boss.atk(self.player)

            if self.boss.hp <= 0:
                print(Colours.colourised(Colours.PURPLE, (f'\n{self.player.name} hp: {self.player.hp}')))
                print(Colours.colourised(Colours.GREEN, 'The boss is dead!'))
            else:
                print(Colours.colourised(Colours.PURPLE, (f'\n{self.player.name} hp: {self.player.hp}')))
                print(Colours.colourised(Colours.GREEN, (f'boss hp: {self.boss.hp}\n')))

    def win(self) -> bool:
        """Prints winning plot when boss hp is less than 0, returns True
        Otherwise returns False
        """
        if not self.game_over():
            if self.boss.hp <= 0:
                print(Colours.colourised(Colours.LIGHT_WHITE, ("\nThe boss has been defeated!\n")))
                with open('content/win_desc.txt', 'r') as f:
                    for line in f: 
                        print(Colours.colourised(Colours.DARK_GRAY, (line.strip())))
                    return True
            else:
                return False
        return False
    
    def run(self) -> str:
        """ Begin the game loop.
        
        1. method to call story intro
        2. set username
        3. movement
        4. if room has enemy then fight (method to check if enemy is inside) , if not pick item
        5. finish fighting -> pick item if any
        6. repeat 3-5 but before 4. ask if want to consume item (need method to call inventory)
        7. when reach room 10, fight the final boss. If the player is defeated before the enemy is over, prompt game over.
        """
        self.intro()
        print('\n')
        self.ask_username()
        while not self.game_over()  and not self.room_10():
            self.movement()
            self.room_desc(data.Player())
            enemy_list = data.generate_enemy()
            if self.enemy_presence(enemy_list):                    
                print(Colours.colourised(Colours.BROWN, ('\nThere is a monster in the room. Defeat them to rescue your family from the grasp of dark magic!')))
                self.inventory_consume_item()
                self.fight(enemy_list)
            else:
                print(Colours.colourised(Colours.LIGHT_GRAY, ("\nGreat save! There are no enemies in this room.\n")))
            if not self.game_over():
                items_list = data.generate_items()
                if self.item_presence(items_list):
                    self.pick_item(items_list)
                    self.player_inventory.show()
                else:
                    print(Colours.colourised(Colours.LIGHT_GRAY, ("Aww too bad, there are no items in this room :(")))
                    
        self.final_room()
        self.inventory_consume_item()
        self.final_boss_fight()
        
                
        if not self.win():
            print(Colours.colourised(Colours.DARK_GRAY, ("You have been defeated >_<")))