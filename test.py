# Import statements
from main import game
from data import Zonemap
import zonemap.json


def test_game():
    # Write code to test the game object here
    # Raise an error if the test fails
    Zonemap(zonemap.json)
    print(game.MUDGame.movement())
    pass

test_game()