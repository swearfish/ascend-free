import sys

import pygame as pg

from engine import FileSystem
from settings import SCREEN_SIZE, GAME_NAME


class AscendancyGame:

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(SCREEN_SIZE)
        pg.mouse.set_visible(True)
        pg.display.set_caption(GAME_NAME, GAME_NAME)
        self.fs = FileSystem('../assets')

        self.bg = pg.image.load(self.fs.get_as_file('data/0opening.gif', 1))

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
            pg.display.flip()

    def close(self):
        self.fs.close()

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
