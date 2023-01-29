import pygame

from engine import FileSystem, Jukebox
from foundation.gcom import gcom_instance
from game.vis.gui_builder import AscendancyGui
from engine.resource_manager import ResourceManager
from engine.scene_manager import SceneManager
from engine.sound_manager import SoundManager
from engine.text.font_manager import FontManager
from foundation.vector_2d import Vec2
from game.logic.star_map import StarMap
from game.vis.ascendancy_dialogs import AscendancyDialogs
from game.vis.logo_scene import LogoScene
from game.vis.main_menu import MainMenu
from settings import GAME_NAME, SCREEN_SIZE, SCREEN_SCALE


class GameWindow:

    def __init__(self):
        from ascendancy_assets.txt.windows_txt import parse_windows_txt

        super().__init__()
        pygame.init()

        self.screen_size = (int(SCREEN_SIZE[0] * SCREEN_SCALE), int(SCREEN_SIZE[1] * SCREEN_SCALE))
        self.display_surface = pygame.display.set_mode(self.screen_size)
        self.back_buffer = pygame.surface.Surface(SCREEN_SIZE)
        self.front_buffer = pygame.surface.Surface(self.screen_size)

        pygame.mouse.set_visible(True)
        pygame.display.set_caption(GAME_NAME, GAME_NAME)

        gcom_instance.set_config('assets_dir', '../assets')
        gcom_instance.set_config('screen', self.back_buffer)
        gcom_instance.set_config('screen_size', Vec2(SCREEN_SIZE[0], SCREEN_SIZE[1]))

        gcom_instance.register_all([FileSystem, ResourceManager, FontManager, SoundManager, Jukebox])
        file_system = gcom_instance.get(FileSystem)

        gcom_instance.set_config('windows_txt', parse_windows_txt(file_system.read_lines('windows.txt')))

        gcom_instance.register_all([SceneManager, AscendancyGui, AscendancyDialogs])

        self.dialogs: AscendancyDialogs = gcom_instance.get(AscendancyDialogs)
        self.scene_manager: SceneManager = gcom_instance.get(SceneManager)

        self.time = pygame.time.get_ticks()
        self.scene_manager.register_scene('logo', LogoScene)
        self.scene_manager.register_scene('main_menu', MainMenu)
        self.scene_manager.enter_scene('logo')

        sm = StarMap()
        pass

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
        gcom_instance.shutdown()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.scene_manager.back_button_press()
        return True
