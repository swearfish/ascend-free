import pygame

from engine import FileSystem, Jukebox
from engine.game_engine import the_engine
from engine.resource_manager import ResourceManager
from engine.scene_manager import SceneManager
from game.logo_scene import LogoScene
from game.main_menu import MainMenu
from settings import GAME_NAME, SCREEN_SIZE, SCREEN_SCALE


class GameWindow:

    def __init__(self):
        super().__init__()
        pygame.init()

        self.screen_size = (int(SCREEN_SIZE[0] * SCREEN_SCALE), int(SCREEN_SIZE[1] * SCREEN_SCALE))
        self.display = pygame.display.set_mode(self.screen_size)
        self.backbuffer = pygame.surface.Surface(SCREEN_SIZE)
        self.frontbuffer = pygame.surface.Surface(self.screen_size)
        the_engine.register(pygame.Surface, self.backbuffer)

        pygame.mouse.set_visible(True)
        pygame.display.set_caption(GAME_NAME, GAME_NAME)

        self.file_system: FileSystem = the_engine.register(FileSystem, init_args=['../assets'])
        self.resource_manager: ResourceManager = the_engine.register(ResourceManager)
        self.jukebox: Jukebox = the_engine.register(Jukebox)
        self.scene_manager: SceneManager = the_engine.register(SceneManager, init_args=[self.backbuffer])

        self.time = pygame.time.get_ticks()
        self.scene_manager.register_scene('logo', LogoScene)
        self.scene_manager.register_scene('main_menu', MainMenu)
        self.scene_manager.enter_scene('logo')

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
        pygame.transform.smoothscale(self.backbuffer, self.screen_size, self.frontbuffer)
        self.display.blit(self.frontbuffer, (0,0))
        pygame.display.flip()
        pass

    def close(self):
        self.file_system.close()

    @staticmethod
    def check_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                return False
        return True
