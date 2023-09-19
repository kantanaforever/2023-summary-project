from main import game
import data

def test_game():
    # Write code to test the game object here
    # Raise an error if the test fails
    game.movement()
    game.intro()
    game.room_desc()
    game.inventory_consume_item()
    game.final_room()
    game.final_boss_fight()
    game.run()
    print('There is no error in the code.')
    
test_game()
