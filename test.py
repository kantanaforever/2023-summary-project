# Import statements
from main import game
import data


def test_game():
    # Write code to test the game object here
    # Raise an error if the test fails
    game.movement()
    game.intro()
    game.room_desc(data.Player())
    game.set_username(data.Player())
    game.inventory_show()
    game.inventory_consume_item()
    game.final_room()
    game.final_boss_fight()
    # game.run()
    print('There is no error in the code.')
    pass


test_game()