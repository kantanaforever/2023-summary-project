# Import statements
from typing import Tuple

import color
import data
import text


def linebreak() -> None:
    print()


def show_text(text: str,
              break_before: bool = True,
              break_after: bool = False) -> None:
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
        + self.player: contains the Player class
        + self.map: contains json file with rooms and their characteristics
        + self.inventory: contins the inventory class
        + self.boss: contains the Boss class
        """
        self.player = data.Player("player", hp=1000)
        self.boss = data.Enemy("boss", hp=500, attack=10)
        self.current_room = data.get_room(data.FIRST_ROOM)

    def game_over(self) -> bool:
        """returns True if player's hp is less than 0
        otherwise returns False
        """
        return self.player.is_dead()

    def last_room(self):
        """checks if player is at last room
        """
        return self.current_room == data.get_room(data.LAST_ROOM)

    def input(self, prompt: str) -> str:
        """strips the empty spaces and changes the input to lower case
        """
        return input(prompt).strip().lower()

    def prompt_valid_choice(
        self,
        options: list,
        question: str,
        errormsg: str,
        colorise=color.black
    ):
        """Prompt the user with a question.
        If the choice is not in options, display errormsg and re-prompt the user.
        If the choice is valid, return player choice.
        colorise is an optional
        """
        linebreak()
        choice = self.input(question + ": ")
        while choice not in options:
            linebreak()
            print(color.red(errormsg))
            choice = self.input(colorise(question + ": "))
        return choice

    def prompt_movement(self) -> str:  # can change after game is working
        """Displays the direction that the player can travel in
        If there are more than one paths in that direction, prompts user to select a path
        Returns the room key (numerical str)
        """
        show_text(color.blue(text.direction_instruction))
        for direction in self.current_room.directions():
            print(f'- {direction}')
        choice = self.prompt_valid_choice(
            self.current_room.directions(),
            question=text.direction_prompt,
            errormsg=text.direction_error,
            colorise=color.blue)
        path_choice = self.current_room.paths[choice]
        if isinstance(path_choice, list):
            # Pick from available paths
            path_choice = self.prompt_valid_choice(
                path_choice,
                text.path_instruction(path_choice),
                text.path_error,
                colorise=color.blue
            )
        return path_choice
            

    def move(self, path: str):
        self.current_room = data.get_room(path)
        show_text(color.dark_gray(
            f'You are now in the {self.current_room.name}!'
        ))

    def show_intro(self):
        """prints the introduction to the game"""
        show_text(color.dark_gray(text.intro), break_after=False)

    def prompt_username(self):
        """prompts and sets the player's username"""
        name = self.input('What would you like to be called: ')
        self.player.name = name

    def show_room_description(self, room: data.Room):
        """prints the description for the room
        """
        show_text(color.brown(room.description), break_after=False)

    def prompt_use_item(self) -> str | None:
        """Display the inventory to the player
        Prompt the player if they want to comsume any items from their inventory.
        Return the name of the item if player picked one, otherwise None
        """
        if self.player.inventory.is_empty():
            show_text(color.red(text.inventory_empty))
            return
        self.player.inventory.show()
        choice = self.prompt_valid_choice(options=['y', 'n'],
                                           question=text.use_item_prompt,
                                           errormsg=text.use_item_error,
                                           colorise=color.light_green)

        if choice == 'n':
            return None
        name = self.prompt_valid_choice(
            options=self.player.inventory.item_names(),
            question=text.choose_item_prompt,
            errormsg=text.choose_item_error,
            colorise=color.light_green
        )
        return name

    def use_item(self, name: str | None) -> None:
        """Use the given item"""
        if name is None:
            return
        
        used_item = self.player.use_item(name)
        if isinstance(used_item, data.Consumable):
            show_text(color.blue(
                f'{used_item.name} has been consumed!'
            ))

        if isinstance(used_item, data.HP):
            show_text(color.blue(
                f'HP increased by {used_item.magnitude}. HP is now {self.player.hp}'
            ))
        elif isinstance(used_item, data.Attack):
            show_text(color.blue(
                f'punch attack has been increased by {used_item.magnitude}. punch attack is now {self.player.attack_punch}'
            ))
        elif isinstance(used_item, data.Equippable):
                
            show_text(color.blue(
                    
                f'{used_item.name} has been equipped!'
            ), break_after=False)
        if isinstance(used_item, data.Weapon):
            show_text(color.blue(
                f'weapon attack is now {self.player.attack_weapon}'
            ))

    @staticmethod
    def hp_report(combatant: data.Combatant) -> None:
        """Display the HP status of a combatant."""
        if isinstance(combatant, data.Player):
            show_text(color.purple(text.hp_report(combatant.name,
                                                  combatant.hp)),
                      break_after=False)
        if isinstance(combatant, data.Enemy):
            show_text(color.green(text.hp_report(combatant.name,
                                                 combatant.hp)),
                      break_after=False)

    @staticmethod
    def trade_blows(choice: str, player: data.Player,
                    enemy: data.Enemy) -> None:
        """Trade blows based on player's choice"""
        if choice == '1':
            enemy.take_damage(player.attack_punch)
        elif choice == '2':
            enemy.take_damage(player.attack_weapon)
        player.take_damage(enemy.attack)

    def combat_choice(self, player: data.Player, enemy: data.Enemy) -> str:
        """Present choice of combat options to user."""
        self.hp_report(player)
        self.hp_report(enemy)
        choice = self.prompt_valid_choice(options=['1', '2'],
                                          question=text.combat_prompt,
                                          errormsg=text.combat_error,
                                          colorise=color.light_green)
        return choice

    def fight(self, enemies: list[data.Enemy]):
        #if enemy_presence -> choose whether to consume an item -> player attack enemy first then enemy attack player -> if player hp reaches 0 before enemy, player looses -> else continue
        """
        The player and enemy take turns to attack each other until one of them is dead
        """
        if not enemies:
            show_text(color.light_gray(text.enemy_absent))
            return
        else:
            show_text(color.brown(text.enemy_present))
        
        while enemies:
            enemy = enemies.pop(0)

            while not self.player.is_dead() and not enemy.is_dead():
                choice = self.combat_choice(self.player, enemy)
                self.trade_blows(choice, self.player, enemy)

            # What if player is dead?
            if enemy.is_dead():
                show_text(color.light_white(text.enemy_defeated))
            if enemies:
                show_text(text.enemy_enter)

    def pick_item(self, items: list[data.Item]) -> None:
        """Displays the available items for player to pick"""
        if not items:
            show_text(color.light_gray(text.item_absent))
            return

        for item in items:
            choice = self.prompt_valid_choice(options=['y', 'n'],
                                              question=text.loot_prompt(
                                                  color.yellow(item.name)),
                                              errormsg=text.loot_error,
                                              colorise=color.light_green)

            if choice.lower() == "y":
                self.player.inventory.add_item(item)
        self.player.inventory.show()

    def show_final_room(self) -> None:
        """Display the story text for the final room.
        Prompt the player if they would like to consume any items.
        Make the player fight the enemy
        """
        print(color.dark_gray(text.final_room))

    def final_boss_fight(self) -> None:
        """player and final boss take turns to attack each other"""
        while not self.player.is_dead() and not self.boss.is_dead():
            choice = self.combat_choice(self.player, self.boss)
            self.trade_blows(choice, self.player, self.boss)

        # What if player is dead?
        if self.boss.is_dead():
            show_text(color.purple(
                text.hp_report(self.player.name, self.player.hp)),
                      break_after=False)
            show_text(color.green(text.boss_dead))
        else:
            show_text(color.purple(
                text.hp_report(self.player.name, self.player.hp)),
                      break_after=False)
            show_text(color.green(text.hp_report(self.boss.name,
                                                 self.boss.hp)))

    def has_won(self) -> bool:
        """Prints winning plot when boss is dead, returns True
        Otherwise returns False
        """
        if not self.game_over():
            if self.boss.is_dead():
                show_text(color.light_white(text.boss_defeated),
                          break_after=False)
                show_text(color.dark_gray(text.game_won))
                return True
            else:
                return False
        return False

    def run(self) -> None:
        """ Begin the game loop.
        
        1. method to call story intro
        2. set username
        3. movement
        4. if room has enemy then fight (method to check if enemy is inside) , if not pick item
        5. finish fighting -> pick item if any
        6. repeat 3-5 but before 4. ask if want to consume item (need method to call inventory)
        7. when reach last room, fight the final boss. If the player is defeated before the enemy is over, prompt game over.
        """
        self.show_intro()
        linebreak()
        self.prompt_username()
        while not self.game_over() and not self.last_room():
            path = self.prompt_movement()
            self.move(path)
            self.show_room_description(self.current_room)
            item_name = self.prompt_use_item()
            self.use_item(item_name)
            enemies = data.generate_enemy()
            self.fight(enemies)
            if self.game_over():
                break
            items = data.generate_items()
            self.pick_item(items)

        self.show_final_room()
        self.prompt_use_item()
        self.final_boss_fight()

        if not self.has_won():
            show_text(color.dark_gray(text.game_lost))
