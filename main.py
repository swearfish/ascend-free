from game.ascendancy_game import AscendancyGame
from settings import GAME_NAME, ORIGINAL_TITLE, COPYRIGHT, LICENSE


def main():
    
    print('')
    print(f'{GAME_NAME}')
    print('')
    print(f'{COPYRIGHT}')
    print(f'Licensed under terms of {LICENSE}, for further details read LICENSE file in the source folder')
    if ORIGINAL_TITLE:
        print('')
        print(f'Based on original PC game:')
        print('')
        print(f'\t{ORIGINAL_TITLE["game_name"]}')
        print(f'\t{ORIGINAL_TITLE["copyright"]}')
        print('\tAll rights reserved!')
    print('')
    game = AscendancyGame()
    game.run()
    game.close()

    print('')
    print(f'Thank you for playing {GAME_NAME}.')
    print('')
    print('')


if __name__ == "__main__":
    main()
