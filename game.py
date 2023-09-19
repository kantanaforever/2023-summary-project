# Import statements
import data
from data import Colours
import text

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
        + self.boss: contains the Boss class
        """
        self.end = '10'
        self.player = data.Player(hp=1000)
        self.map = data.map
        self.boss = data.Enemy(hp=500, attack=10)

    def game_over(self) -> bool:
        """returns True if player's hp is less than 0
        otherwise returns False
        """
        return self.player.is_dead()

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
        
        print(Colours.colourised(Colours.BLUE, f'\n{text.direction_instruction} \n'))
        for i, choice in enumerate(choices):
            if choice != [None]:
                print(f'- {keys[i]}')
                available.append(keys[i])
        direction_choice = self.prompt_valid_choice(
            available,
            question=f'\n{text.direction_prompt}: ',
            errormsg=f'\n{text.direction_error}',
            col = Colours.BLUE
        )
        numpaths = len(choices[keys.index(direction_choice)])
        if numpaths == 1:
            path_choice = 0
        else:    
            path_choices = [str(i) for i in range(1, numpaths + 1)]
            question = text.path_instruction(path_choices)
            path_choice = self.prompt_valid_choice(path_choices, question, f'\n{text.path_error}', col=Colours.BLUE)
        self.player.current = self.map[self.player.current][direction_choice][int(path_choice) - 1] #  updating the player position 
        print(Colours.colourised(Colours.DARK_GRAY,'\n' * 3 + 'You are now in the '+ self.map[self.player.current]["name"] + '!\n')) # printing the name of the room

    
    def intro(self):
        """prints the introduction to the game"""
        print(Colours.colourised(Colours.DARK_GRAY, text.intro), end= '')

    def ask_username(self):
        """prompts and sets the player's username"""
        name = self.input('What would you like to be called: ')
        self.player.name = name

    def room_desc(self, Player):
        """prints the description for the room the player is in
        """
        desc = self.map[self.player.current]['description']
        print(Colours.colourised(Colours.BROWN, f'\n{desc}'))

    def inventory_consume_item(self) -> None:
        """Display the inventory to the player
        Prompt the player if they want to comsume any items from their inventory.
        """
        if self.player.inventory.is_empty():
            print(Colours.colourised(Colours.RED, f"\n{text.inventory_empty}\n"))
            return
        self.player.inventory.show()
        consume = self.prompt_valid_choice(
            options=['y', 'n'],
            question=f"{text.use_item_prompt}: ",
            errormsg=f'\n{text.use_item_error}\n',
            col= Colours.LIGHT_GREEN
        )
        
        if consume == 'n':
            return None

        else: 
            name = self.prompt_valid_choice(
                options=self.player.inventory.item_names(),
                question=f"{text.choose_item_prompt}: ",
                errormsg=text.choose_item_error,
                col=Colours.LIGHT_GREEN
            )
            used_item = self.player.use_item(name)
            if isinstance(used_item, data.Consumable):
                print(Colours.colourised(Colours.BLUE, (f'{used_item.name} has been consumed!')))
                
                if isinstance(used_item, data.HP):
                    print(Colours.colourised(Colours.BLUE, (f'HP increased by {used_item.magnitude}. HP is now {self.player.hp}')))
                elif isinstance(used_item, data.Attack):
                    print(Colours.colourised(Colours.BLUE, (f'punch attack has been increased by {used_item.magnitude}. punch attack is now {self.player.attack_punch}')))
                    
            else:
                print(Colours.colourised(Colours.BLUE, (f'{used_item.name} has been equipped!')))
                if isinstance(used_item, data.Weapon):
                    print(Colours.colourised(Colours.BLUE, (f'weapon attack is now {self.player.attack_weapon}')))
            
    def fight(self, enemy_list):
        #if enemy_presence -> choose whether to consume an item -> player attack enemy first then enemy attack player -> if player hp reaches 0 before enemy, player looses -> else continue
        """
        The player and enemy take turns to attack each other until one of their hp is less than 0
        """
        for i in range(len(enemy_list)):
            
            while not self.player.is_dead() and not enemy_list[i].is_dead():
                print(Colours.colourised(Colours.PURPLE, text.hp_report(self.player.name, self.player.hp)))
                print(Colours.colourised(Colours.GREEN, text.hp_report("enemy", enemy.hp)))
                choice = self.prompt_valid_choice(
                    options=['1', '2'],
                    question=f'\n{text.combat_prompt}',
                    errormsg=f'\n{text.combat_error}',
                    col=Colours.LIGHT_GREEN
                )
            
    
                if choice == '1':
                    enemy_list[i].take_damage(self.player.attack_punch)
                elif choice == '2':
                    enemy_list[i].take_damage(self.player.attack_weapon)
                self.player.take_damage(enemy_list[i].attack)
    
                if enemy_list[i].is_dead():
                    print(Colours.colourised(Colours.LIGHT_WHITE, (f'\n{text.enemy_defeated}\n')))
                    if i < len(enemy_list) - 1:
                        print(text.enemy_enter)
                    
        
    def pick_item(self, items): 
        """Displays the item available in the room"""
        for i in items:
            item = Colours.colourised(Colours.YELLOW, i.name)
        #print(self.colour...item)
            choice = self.prompt_valid_choice(
                options=['y', 'n'],
                question=f'\n{text.loot_prompt(item.name)}',
                errormsg=f'\n{text.loot_error}\n',
                col= Colours.LIGHT_GREEN
            )

            if choice.lower() == "y":
                self.player.inventory.add_item(i)
                
                
    
    def final_room(self):
        """Display the story text for the final room.
        Prompt the player if they would like to consume any items.
        Make the player fight the enemy
        """
        print(Colours.colourised(Colours.DARK_GRAY, text.final_room))

    def final_boss_fight(self):
        """player and final boss take turns to attack each other""" 
        print(Colours.colourised(Colours.PURPLE, text.hp_report(self.player.name, self.player.hp)))
        print(Colours.colourised(Colours.GREEN, text.hp_report("boss", boss.hp)))
        while not self.player.is_dead() and not self.boss.is_dead():
            choice = self.prompt_valid_choice(
                options=['1','2'],
                question = text.combat_prompt,
                errormsg=f'\n{text.combat_error\n',
                col= Colours.LIGHT_GREEN
                )
            
            if choice == '1':
                self.boss.take_damage(self.player.attack_punch)
            else:
                self.boss.take_damage(self.player.attack_weapon)
            self.player.take_damage(boss.attack)

            if self.boss.is_dead():
                print(Colours.colourised(Colours.PURPLE, (f'\n{text.hp_report(self.player.name, self.player.hp)}')))
                print(Colours.colourised(Colours.GREEN, text.boss_dead))
            else:
                print(Colours.colourised(Colours.PURPLE, (f'\n{self.player.name} hp: {self.player.hp}')))
                print(Colours.colourised(Colours.GREEN, (f'{text.hp_report("boss", boss.hp)}\n')))

    def win(self) -> bool:
        """Prints winning plot when boss hp is less than 0, returns True
        Otherwise returns False
        """
        if not self.game_over():
            if self.boss.hp <= 0:
                print(Colours.colourised(Colours.LIGHT_WHITE, (f"\n{text.boss_defeated}\n")))
                print(Colours.colourised(Colours.DARK_GRAY, text.game_won))
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
                print(Colours.colourised(Colours.BROWN, (f'\n{text.enemy_present}')))
                self.inventory_consume_item()
                self.fight(enemy_list)
            else:
                print(Colours.colourised(Colours.LIGHT_GRAY, (f"\n{text.enemy_absent}\n")))
            if not self.game_over():
                items_list = data.generate_items()
                if self.item_presence(items_list):
                    self.pick_item(items_list)
                    self.player.inventory.show()
                else:
                    print(Colours.colourised(Colours.LIGHT_GRAY, text.item_absent))
                    
        self.final_room()
        self.inventory_consume_item()
        self.final_boss_fight()
        
                
        if not self.win():
            print(Colours.colourised(Colours.DARK_GRAY, text.game_lost))