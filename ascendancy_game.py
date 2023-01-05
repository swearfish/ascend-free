import sys

import pygame as pg

from cob import CobArchive
from settings import SCREEN_SIZE, GAME_NAME


class AscendancyGame:

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(SCREEN_SIZE)
        pg.mouse.set_visible(True)
        pg.display.set_caption(GAME_NAME, GAME_NAME)

        self.cobs = [
            CobArchive('../assets/ascend00.cob'),
            CobArchive('../assets/ascend01.cob'),
            CobArchive('../assets/ascend02.cob')
            ]
        bg_data = self.cobs[1].read_file('data/0opening.gif')
        self.bg = pg.image.load('../assets/cob01/data/0opening.gif')

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
            pg.display.flip()

    def close(self):
        for cob in self.cobs:
            cob.close()

    def update(self):
        pass

    def draw(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.bg, (0, 0))
        pass

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
