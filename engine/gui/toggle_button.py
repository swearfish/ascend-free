import pygame.draw
from pygame import Surface

from engine.gui import Button
from engine.gui.colors import COLOR_BUTTON_BG, COLOR_BUTTON_BG_HIGH, COLOR_BUTTON_BG_ON
from foundation.area import Area
from foundation.vector_2d import Vec2


class ToggleButton(Button):
    def __init__(self, parent, name: str, area: Area,
                 help_index: str = None, message: any = None,
                 initial_state: bool = False):
        super().__init__(parent, name, area, help_index, message, mouse_focus=True)
        self.state = initial_state

    def on_draw(self, screen: Surface, pos: Vec2):
        if self._mouse_focus:
            pygame.draw.rect(screen, COLOR_BUTTON_BG_HIGH, self.area.new_origin(pos).as_tuple())
        elif self.state:
            pygame.draw.rect(screen, COLOR_BUTTON_BG_ON, self.area.new_origin(pos).as_tuple())
        else:
            pygame.draw.rect(screen, COLOR_BUTTON_BG, self.area.new_origin(pos).as_tuple())

    def on_mouse_click(self, mouse_pos: Vec2) -> bool:
        result = super().on_mouse_click(mouse_pos)
        self.state = not self.state
        self.invoke_listener(lambda l: l.on_toggle(self, self._message, self.state))
        return result

    def __str__(self):
        return f'TGL-BUTTON {self.name} @ [{self.area}] :: {self._message}'
