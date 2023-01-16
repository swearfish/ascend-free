from game.game_window import GameWindow
from settings import GAME_NAME, COPYRIGHT, LICENSE, ORIGINAL_TITLE


def run_game():
    print('')
    print(f'{GAME_NAME}')
    print('')
    print(f'{COPYRIGHT}')
    print(f'Licensed under terms of {LICENSE}, for further details read LICENSE file in the source folder')
    if ORIGINAL_TITLE:
        print('')
        print(f'This remake is based on original PC game:')
        print('')
        print(f'\t{ORIGINAL_TITLE["game_name"]}')
        print(f'\t{ORIGINAL_TITLE["copyright"]}')
        print('\tAll rights reserved!')
    print('')
    with GameWindow() as wnd:
        wnd.run()

    print('')
    print(f'Thank you for playing {GAME_NAME}.')
    print('')
    print('')
