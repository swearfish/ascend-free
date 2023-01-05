import sys

import pygame as pg

from settings import SCREEN_SIZE, GAME_NAME


class AscendancyGame:

    def __init__(self):
        pg.init()
        pg.display.set_mode(SCREEN_SIZE)
        pg.mouse.set_visible(True)
        pg.display.set_caption(GAME_NAME, GAME_NAME)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

    def update(self):
        pass

    def draw(self):
        pass

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
