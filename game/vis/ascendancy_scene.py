from typing import Optional

import pygame
from pygame import KMOD_SHIFT

from engine.gui.button import Button
from engine.gui.control import Control
from engine.gui.ui_event_listener import UiEventListener
from engine.scene import Scene
from foundation.gcom import auto_wire
from foundation.vector_2d import Vec2
from game.vis.ascendancy_dialogs import AscendancyDialogs
from game.vis.gui_builder import AscendancyGuiBuilder


@auto_wire
class AscendancyScene(Scene, UiEventListener):
    dialogs: AscendancyDialogs
    gui_builder: AscendancyGuiBuilder
    display_scale: float

    def __init__(self, state_index: int = -1,
                 template_file: Optional[str] = None,
                 template_index: int = 1):
        super().__init__()
        self.state_frame = self.gui_builder.build_frame(state_index)
        if self.state_frame:
            self.state_frame.listener = self
        if template_file:
            self.background = self.resource_manager.renderer_from_shape_or_gif(template_file, template_index-1)
        else:
            self.background = None
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
        if self.background:
            self.background.draw(self.screen, Vec2(0, 0))
        if self.state_frame is not None:
            self.state_frame.handle_draw(self.screen, Vec2(0, 0))

    def update(self, total_time: float, frame_time: float):
        if self.state_frame is not None:
            self.state_frame.handle_update(total_time, frame_time)
            self._update_gui_input()

    def _update_gui_input(self):
        mouse_buttons = pygame.mouse.get_pressed()
        mods = pygame.key.get_mods()
        shift = mods & KMOD_SHIFT == KMOD_SHIFT
        mouse_pos = Vec2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) / self.display_scale
        self.state_frame.update_mouse(mouse_pos, mouse_buttons, shift)
