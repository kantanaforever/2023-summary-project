# Import statements
from game import MUDGame

game = MUDGame()

if __name__ == "__main__":
    import data
    for item in data.generate_items():
        game.player.take_item(item)
    game.player.inventory.show()
    # game.run()
