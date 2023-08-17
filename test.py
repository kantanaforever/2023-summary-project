# Import statements
from main import game
import data


def test_game():
    # Write code to test the game object here
    # Raise an error if the test fails
    print(data.map)
    print(game.MUDGame.run())
    pass

test_game()