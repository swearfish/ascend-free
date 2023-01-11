import sys

import pygame as pg

from engine import FileSystem, Jukebox
from engine.resource_manager import ResourceManager
from engine.scene_manager import SceneManager
from game.logo_scene import LogoScene
from settings import SCREEN_SIZE, GAME_NAME


class AscendancyGame:

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(SCREEN_SIZE)
        pg.mouse.set_visible(True)
        pg.display.set_caption(GAME_NAME, GAME_NAME)
        self.fs = FileSystem('../assets')
        self.res = ResourceManager(self.fs)
        self.scenes = SceneManager(LogoScene(), self.screen, self.res)
        self.jukebox = Jukebox(self.fs)
        self.jukebox.play_now(0)

    def run(self):
        while True:
            self.check_events()
            self.scenes.update()
            self.scenes.draw()
            pg.display.flip()

    def close(self):
        self.fs.close()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
