# Import statements
import data
import color
import text


def linebreak() -> None:
    print()


def show_text(text: str, break_before: bool = True, break_after: bool = False) -> None:
    if break_before:
        linebreak()  # next line
    print(text)
    if break_after:
        linebreak()  # next line


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

    def prompt_valid_choice(self,
                            options: list,
                            question: str,
                            errormsg: str,
                            colorise=color.black):
        """Prompt the user with a question.
        If the choice is not in options, display errormsg and re-prompt the user.
        If the choice is valid, return player choice.
        colorise is an optional
        """
        linebreak()
        choice = self.input(question)
        while choice not in options:
            linebreak()
            print(color.red(errormsg))
            choice = self.input(colorise(question + ": "))
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
        
        show_text(color.blue(text.direction_instruction))
        for i, choice in enumerate(choices):
            if choice != [None]:
                print(f'- {keys[i]}')
                available.append(keys[i])
        direction_choice = self.prompt_valid_choice(
            available,
            question=text.direction_prompt,
            errormsg=text.direction_error,
            colorise=color.blue
        )
        numpaths = len(choices[keys.index(direction_choice)])
        if numpaths == 1:
            path_choice = 0
        else:
            path_choices = [str(i) for i in range(1, numpaths + 1)]
            question = text.path_instruction(path_choices)
            path_choice = self.prompt_valid_choice(path_choices,
                                                   question,
                                                   text.path_error,
                                                   colorise=color.blue)
        self.player.current = self.map[self.player.current][direction_choice][int(path_choice) - 1] #  updating the player position 
        linebreak()
        show_text(color.dark_gray('You are now in the ' + self.map[self.player.current]["name"] + '!')) # printing the name of the room

    
    def intro(self):
        """prints the introduction to the game"""
        show_text(color.dark_gray(text.intro), break_after=False)

    def ask_username(self):
        """prompts and sets the player's username"""
        name = self.input('What would you like to be called: ')
        self.player.name = name

    def room_desc(self):
        """prints the description for the room the player is in
        """
        desc = self.map[self.player.current]['description']
        show_text(color.brown(desc), break_after=False)

    def inventory_consume_item(self) -> None:
        """Display the inventory to the player
        Prompt the player if they want to comsume any items from their inventory.
        """
        if self.player.inventory.is_empty():
            show_text(color.red(text.inventory_empty))
            return
        self.player.inventory.show()
        consume = self.prompt_valid_choice(options=['y', 'n'],
                                           question=text.use_item_prompt,
                                           errormsg=text.use_item_error,
                                           colorise=color.light_green
        )
        
        if consume == 'n':
            return None

        else:
            name = self.prompt_valid_choice(
                options=self.player.inventory.item_names(),
                question=text.choose_item_prompt,
                errormsg=text.choose_item_error,
                colorise=color.light_green
            )
            used_item = self.player.use_item(name)
            if isinstance(used_item, data.Consumable):
                show_text(color.blue(f'{used_item.name} has been consumed!'))
                
                if isinstance(used_item, data.HP):
                    show_text(color.blue(f'HP increased by {used_item.magnitude}. HP is now {self.player.hp}'))
                elif isinstance(used_item, data.Attack):
                    show_text(color.blue(f'punch attack has been increased by {used_item.magnitude}. punch attack is now {self.player.attack_punch}'))
                    
            elif isinstance(used_item, data.Equippable):
                show_text(color.blue(f'{used_item.name} has been equipped!'), break_after=False)
                if isinstance(used_item, data.Weapon):
                    show_text(color.blue(f'weapon attack is now {self.player.attack_weapon}'))
            
    def fight(self, enemies: list[data.Enemy]):
        #if enemy_presence -> choose whether to consume an item -> player attack enemy first then enemy attack player -> if player hp reaches 0 before enemy, player looses -> else continue
        """
        The player and enemy take turns to attack each other until one of their hp is less than 0
        """
        while enemies:
            enemy = enemies.pop(0)
            
            while not self.player.is_dead() and not enemy.is_dead():
                show_text(color.purple(text.hp_report(self.player.name, self.player.hp)),
                          break_after=False)
                show_text(color.green(text.hp_report("enemy", enemy.hp)),
                          break_after=False)
                choice = self.prompt_valid_choice(
                    options=['1', '2'],
                    question=text.combat_prompt,
                    errormsg=text.combat_error,
                    colorise=color.light_green
                )
            
    
                if choice == '1':
                    enemy.take_damage(self.player.attack_punch)
                elif choice == '2':
                    enemy.take_damage(self.player.attack_weapon)
                self.player.take_damage(enemy.attack)
    
                if enemy.is_dead():
                    show_text(color.light_white(text.enemy_defeated))
                    if enemies:
                        show_text(text.enemy_enter)
                    
        
    def pick_item(self, items: list):
        """Displays the item available in the room"""
        for item in items:
            item = color.yellow(item.name)
        #print(self.colour...item)
            choice = self.prompt_valid_choice(
                options=['y', 'n'],
                question=text.loot_prompt(item.name),
                errormsg=text.loot_error,
                colorise=color.light_green
            )

            if choice.lower() == "y":
                self.player.inventory.add_item(i)
                
    def final_room(self):
        """Display the story text for the final room.
        Prompt the player if they would like to consume any items.
        Make the player fight the enemy
        """
        print(color.dark_gray(text.final_room))

    def final_boss_fight(self):
        """player and final boss take turns to attack each other""" 
        print(color.purple(text.hp_report(self.player.name, self.player.hp)))
        print(color.green(text.hp_report("boss", self.boss.hp)))
        while not self.player.is_dead() and not self.boss.is_dead():
            choice = self.prompt_valid_choice(
                options=['1','2'],
                question = text.combat_prompt,
                errormsg=text.combat_error,
                colorise=color.light_green
                )
            
            if choice == '1':
                self.boss.take_damage(self.player.attack_punch)
            else:
                self.boss.take_damage(self.player.attack_weapon)
            self.player.take_damage(self.boss.attack)

            if self.boss.is_dead():
                show_text(color.purple(text.hp_report(self.player.name, self.player.hp), break_after=False))
                show_text(color.green(text.boss_dead))
            else:
                show_text(color.purple(text.hp_report(self.player.name, self.player.hp)), break_after=False)
                show_text(color.green(text.hp_report("boss", boss.hp)))

    def win(self) -> bool:
        """Prints winning plot when boss hp is less than 0, returns True
        Otherwise returns False
        """
        if not self.game_over():
            if self.boss.is_dead():
                show_text(color.light_white(text.boss_defeated), break_after=False)
                show_text(color.dark_gray(text.game_won))
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
            self.room_desc()
            enemy_list = data.generate_enemy()
            if self.enemy_presence(enemy_list):
                show_text(color.brown(text.enemy_present))
                self.inventory_consume_item()
                self.fight(enemy_list)
            else:
                show_text(color.light_gray(text.enemy_absent))
            if not self.game_over():
                items_list = data.generate_items()
                if self.item_presence(items_list):
                    self.pick_item(items_list)
                    self.player.inventory.show()
                else:
                    show_text(color.light_gray(text.item_absent))
                    
        self.final_room()
        self.inventory_consume_item()
        self.final_boss_fight()
        
                
        if not self.win():
            show_text(color.dark_gray(text.game_lost))