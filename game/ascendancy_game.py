# import pygame as pygame
import pygame

from engine import FileSystem, Jukebox
from engine.game_engine import the_engine
from engine.resource_manager import ResourceManager
from engine.scene_manager import SceneManager
from game.logo_scene import LogoScene
from settings import GAME_NAME, SCREEN_SIZE


class AscendancyGame():

    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = the_engine.register(pygame.Surface, pygame.display.set_mode(SCREEN_SIZE))
        pygame.mouse.set_visible(True)
        pygame.display.set_caption(GAME_NAME, GAME_NAME)

        self.file_system: FileSystem = the_engine.register(FileSystem, init_args=['../assets'])
        self.resource_manager: ResourceManager = the_engine.register(ResourceManager)
        self.jukebox: Jukebox = the_engine.register(Jukebox)
        self.scene_manager: SceneManager = the_engine.register(SceneManager, init_args=[self.screen])

        self.jukebox.play_now(0)
        self.time = pygame.time.get_ticks()
        self.scene_manager.enter_scene(LogoScene())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def run(self):
        while self.check_events():
            self.on_draw()

    def on_draw(self):
        old_time = self.time
        self.time = pygame.time.get_ticks()
        dt = self.time - old_time
        self.scene_manager.update(dt)
        self.scene_manager.draw()
        pygame.display.flip()
        pass

    def close(self):
        self.file_system.close()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                return False
        return True
