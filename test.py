from game import MUDGame
import data

def test_game():
    # Write code to test the game object here
    # Raise an error if the test fails
    game = MUDGame()
    game.movement()
    game.intro()
    game.room_desc()
    game.inventory_consume_item()
    game.final_room()
    game.final_boss_fight()
    game.run()
    print('There is no error in the code.')

def test_inventory_show():
    game = MUDGame()
    for item in data.generate_items():
        game.player.take_item(item)
    game.player.inventory.show()
    
test_game()
test_inventory_show()
