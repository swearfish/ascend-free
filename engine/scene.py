import pygame.mouse
from pygame import Surface, KMOD_SHIFT

from engine.gcom import gcom
from engine.gui.button import Button
from engine.gui.control import Control
from engine.gui.gui_builder import AscendancyGui
from engine.gui.ui_event_listener import UiEventListener
from engine.resource_manager import ResourceManager
from engine.sound_manager import SoundManager
from engine.text.font_manager import FontManager
from foundation.vector import Vec2
from settings import SCREEN_SCALE


class Scene:
    def __init__(self, scene_manager, state_index: int = -1):
        self.resource_manager: ResourceManager = gcom.get(ResourceManager)
        self.font_manager: FontManager = gcom.get(FontManager)
        self.screen: Surface = gcom.get(Surface)
        self.scene_manager = scene_manager
        self.sound_manager: SoundManager = gcom.get(SoundManager)

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, total_time: float, frame_time: float):
        pass

    def draw(self):
        pass

    # noinspection PyMethodMayBeStatic
    def handle_back_key(self) -> bool:
        return False
