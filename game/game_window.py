import argparse

import pygame

from foundation.gcom import gcom_instance
from foundation.vector_2d import Vec2
from game.game import AscendancyGame
from settings import GAME_NAME, SCREEN_SIZE


class GameWindow:

    def __init__(self):

        super().__init__()
        pygame.init()

        pygame.mouse.set_visible(True)
        pygame.display.set_caption(GAME_NAME, GAME_NAME)

        args = parse_command_line_args()
        gcom_instance.set_config('assets_dir', args.assets_dir)
        gcom_instance.set_config('cache_dir', args.cache_dir)
        screen_size = Vec2(SCREEN_SIZE[0], SCREEN_SIZE[1])
        gcom_instance.set_config('screen_size', screen_size)
        gcom_instance.set_config('display_size', screen_size * args.display_scale)
        gcom_instance.set_config('display_scale', args.display_scale)
        gcom_instance.set_config('skip_logo', args.skip_logo)

        self.game: AscendancyGame = gcom_instance.get(AscendancyGame)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def run(self):
        while self.check_events():
            self.on_draw()

    def on_draw(self):
        self.game.draw()
        pygame.display.flip()

    def close(self):
        gcom_instance.shutdown()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.on_back_button()
                else:
                    self.game.on_key_press(event)
        return True


def parse_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-logo", action="store_true", help="Skip displaying the logo")
    parser.add_argument("--display-scale", type=float, default=1.5, help="Scale factor for display")
    parser.add_argument("--assets-dir", default="../assets", help="Path to COB files")
    parser.add_argument("--cache-dir", default="../assets/cache", help="Writable path to intermediate files")

    args = parser.parse_args()
    return args
