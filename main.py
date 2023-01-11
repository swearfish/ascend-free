from game.ascendancy_game import AscendancyGame
from settings import GAME_NAME


def main():
    
    game = AscendancyGame()
    game.run()
    game.close()

    print(f'Thank you for playing {GAME_NAME}!')


if __name__ == "__main__":
    main()
