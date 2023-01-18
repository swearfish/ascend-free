import pygame.mouse
from pygame import Surface, KMOD_SHIFT

from engine.gcom import gcom
from engine.gui.button import Button
from engine.gui.gui_builder import AscendancyGui
from engine.gui.listener import Listener
from engine.resource_manager import ResourceManager
from engine.sound_manager import SoundManager
from foundation.vector import Vec2
from settings import SCREEN_SCALE


class Scene(Listener):
    def __init__(self, scene_manager, state_index: int = -1):
        self.resource_manager: ResourceManager = gcom.get(ResourceManager)
        self.screen: Surface = gcom.get(Surface)
        self.scene_manager = scene_manager
        self.gui_manager: AscendancyGui = gcom.get(AscendancyGui)
        self.sound_manager: SoundManager = gcom.get(SoundManager)
        if 0 <= state_index:
            self.state_frame = self.gui_manager.states[state_index]
            self.state_frame.listener = self
        pass

    def on_click(self, sender, message) -> bool:
        if isinstance(sender, Button):
            self.sound_manager.play('button')
        return False

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, total_time: float, frame_time: float):
        pass

    def draw(self):
        if self.state_frame is not None:
            self.state_frame.handle_draw(self.screen, Vec2(0, 0))
            mouse_buttons = pygame.mouse.get_pressed()
            mods = pygame.key.get_mods()
            shift = mods & KMOD_SHIFT == KMOD_SHIFT
            mouse_pos = Vec2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) / SCREEN_SCALE
            self.state_frame.update_mouse(mouse_pos, mouse_buttons, shift)

    # noinspection PyMethodMayBeStatic
    def handle_back_key(self) -> bool:
        return False
