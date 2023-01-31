import pygame

from foundation.gcom import gcom_instance
from foundation.vector_2d import Vec2
from game.game import AscendancyGame
from settings import GAME_NAME, SCREEN_SIZE, SCREEN_SCALE


class GameWindow:

    def __init__(self):

        super().__init__()
        pygame.init()

        pygame.mouse.set_visible(True)
        pygame.display.set_caption(GAME_NAME, GAME_NAME)

        gcom_instance.set_config('assets_dir', '../assets')
        screen_size = Vec2(SCREEN_SIZE[0], SCREEN_SIZE[1])
        gcom_instance.set_config('screen_size', screen_size)
        gcom_instance.set_config('display_size', screen_size * SCREEN_SCALE)

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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.on_back_button()
        return True
