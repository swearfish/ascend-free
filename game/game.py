import pygame

from engine.scene_manager import SceneManager
from foundation.gcom import Component, auto_gcom, gcom_instance
from foundation.vector_2d import Vec2
from game.vis.ascendancy_dialogs import AscendancyDialogs
from game.vis.gui_builder import AscendancyGuiBuilder
from game.vis.logo.logo_scene import LogoScene
from game.vis.main_menu.main_menu import MainMenu
from game.vis.new_game.new_game_scene import NewGameScene
from game.vis.new_game.start_scene import StartScene
from game.vis.galaxy.galaxy_scene import GalaxyScene


@auto_gcom
class AscendancyGame(Component):
    gui_builder: AscendancyGuiBuilder
    dialogs: AscendancyDialogs
    scene_manager: SceneManager
    screen_size: Vec2
    display_size: Vec2

    def __init__(self):
        super().__init__()
        self.time = pygame.time.get_ticks()
        self.display_surface = pygame.display.set_mode(self.display_size.as_tuple())
        self.back_buffer = pygame.surface.Surface(self.screen_size.as_tuple())
        self.front_buffer = pygame.surface.Surface(self.display_size.as_tuple())
        gcom_instance.set_config('screen', self.back_buffer)
        self._inited = False

    def _late_init(self):
        self.scene_manager.register_scene('logo', LogoScene)
        self.scene_manager.register_scene('main_menu', MainMenu)
        self.scene_manager.register_scene('new_game', NewGameScene)
        self.scene_manager.register_scene('start', StartScene)
        self.scene_manager.register_scene('galaxy', GalaxyScene)
        self.scene_manager.enter_scene('logo')

    def draw(self):
        if not self._inited:
            self._late_init()
            self._inited = True
        old_time = self.time
        self.time = pygame.time.get_ticks()
        dt = self.time - old_time
        self.scene_manager.update(dt)
        self.scene_manager.draw()
        pygame.transform.smoothscale(self.back_buffer, self.display_size.as_tuple(), self.front_buffer)
        self.display_surface.blit(self.front_buffer, (0, 0))

    def on_back_button(self):
        self.scene_manager.back_button_press()

    # noinspection PyMethodMayBeStatic
    def on_key_press(self, ev):
        if ev.key == pygame.K_x and ev.mod & pygame.KMOD_ALT:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
