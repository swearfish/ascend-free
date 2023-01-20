import pygame
from pygame import KMOD_SHIFT

from engine.gcom import gcom
from engine.gui.button import Button
from engine.gui.control import Control
from engine.gui.gui_builder import AscendancyGui
from engine.gui.ui_event_listener import UiEventListener
from engine.scene import Scene
from foundation.vector import Vec2
from game.vis.ascendancy_dialogs import AscendancyDialogs
from settings import SCREEN_SCALE


class AscendancyScene(Scene, UiEventListener):
    def __init__(self, scene_manager, state_index: int = -1):
        super().__init__(scene_manager)
        self.gui_manager: AscendancyGui = gcom.get(AscendancyGui)
        self.dialogs: AscendancyDialogs = gcom.get(AscendancyDialogs)
        if 0 <= state_index:
            self.state_frame = self.gui_manager.states[state_index]
            self.state_frame.listener = self
        self.click_events: dict = {}

    def on_click(self, sender: Control, message) -> bool:
        if isinstance(sender, Button):
            self.sound_manager.play('button')
        if sender in self.click_events:
            self.click_events[sender](sender, message)
            return True
        elif sender.name in self.click_events:
            self.click_events[sender.name](sender, message)
            return True
        elif message in self.click_events:
            self.click_events[message](sender, message)
            return True
        return False

    def draw(self):
        super().draw()
        if self.state_frame is not None:
            self.state_frame.handle_draw(self.screen, Vec2(0, 0))
            self._update_gui_input()

    def _update_gui_input(self):
        mouse_buttons = pygame.mouse.get_pressed()
        mods = pygame.key.get_mods()
        shift = mods & KMOD_SHIFT == KMOD_SHIFT
        mouse_pos = Vec2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) / SCREEN_SCALE
        self.state_frame.update_mouse(mouse_pos, mouse_buttons, shift)
