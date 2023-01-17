import pygame

from engine import FileSystem, Jukebox
from engine.gcom import gcom
from engine.gui.gui_builder import AscendancyGui
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
        self.display_surface = pygame.display.set_mode(self.screen_size)
        self.back_buffer = pygame.surface.Surface(SCREEN_SIZE)
        self.front_buffer = pygame.surface.Surface(self.screen_size)
        gcom.register(pygame.Surface, self.back_buffer)

        pygame.mouse.set_visible(True)
        pygame.display.set_caption(GAME_NAME, GAME_NAME)

        self.file_system: FileSystem = gcom.register(FileSystem, init_args=['../assets'])
        self.resource_manager: ResourceManager = gcom.register(ResourceManager)
        self.jukebox: Jukebox = gcom.register(Jukebox)

        from ascendancy_assets.txt.windows_txt import parse_windows_txt
        windows = parse_windows_txt(self.file_system.read_lines('windows.txt'))
        gcom.register(AscendancyGui, init_args=[windows])

        self.scene_manager: SceneManager = gcom.register(SceneManager, init_args=[self.back_buffer])

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
        pygame.transform.smoothscale(self.back_buffer, self.screen_size, self.front_buffer)
        self.display_surface.blit(self.front_buffer, (0, 0))
        pygame.display.flip()
        pass

    def close(self):
        self.file_system.close()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.scene_manager.back_button_press()
        return True
