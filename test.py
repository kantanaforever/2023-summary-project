# Import statements
from main import game
import data


def test_game():
    # Write code to test the game object here
    # Raise an error if the test fails
    test_obj = game.MUDGame()
    test_obj.movement()
    pass

test_game()