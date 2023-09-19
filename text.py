with open('content/intro.txt', 'r') as f:
    intro = f.read()

with open('content/finaldesc.txt', 'r') as f:
    final_rooom = f.read()

with open('content/win_desc.txt', 'r') as f:
    game_won = f.read()

game_lost = "You have been defeated >_<"

direction_instruction = "You can move in the following directions:"
direction_prompt = "Which direction do you wish to go to?"
direction_error = "You can only move in the above stated direction(s)!"

def path_instruction(choices: list[str]) -> str:
    prompt = f"""You entered a corridor, and there are {len(choices)} doors...
The following are the paths that can be taken:"""
    for choice in choices:
        prompt += f'\npath {choice}'
    prompt += "\nWhich path do you wish to take? Type the path number:"
path_error = "You can only take the above stated path(s)!"

combat_prompt = """The enemy is now in front of you! You can choose to
1. punch
2. attack with existing weapons:"""
combat_error = "Invalid option!"

def loot_prompt(item_name: str) -> str:
    return f"{item_name} found! Collect it to help increase your chances of defeating the monsters!(y/n):"
loot_error = "invalid option!"

boss_dead = "The boss is dead!"
boss_defeated = "The boss has been defeated!"

def hp_report(name: str, hp: int) -> str:
    return f"{name} hp: {hp}"

enemy_present = "There is a monster in the room. Defeat them to rescue your family from the grasp of dark magic!"
enemy_absent = "Great save! There are no enemies in this room."
enemy_defeated = "You have defeated the enemy!"
enemy_enter = "Another enemy has entered..."
item_absent = "Aww too bad, there are no items in this room :("

inventory_empty = "Nothing in inventory!"

use_item_prompt = "Would you like to equip/consume any item?(y/n)?"
use_item_error = "Not a valid response!"
choose_item_prompt = "Which item would you like to equip/consume?"
choose_item_error = "Invalid item!"