from typing import Optional

import pygame.draw
from pygame import Surface

from engine.gui.control import Control
from engine.gui.text_item import TextItem
from engine.text.text_render import TextRenderer
from foundation.area import Area
from foundation.vector import Vec2

COLOR_BUTTON_BG = (12, 32, 49)
COLOR_BUTTON_BG_HIGH = (16, 69, 77)


class Button(Control):
    def __init__(self, parent, name: str, area: Area, help_index: str = None):
        super().__init__(parent, area)
        self.name = name
        self.area = area
        self.help_index = help_index

    def add_text_item(self, font: TextRenderer, text: str, pos: Vec2, flags: int):
        item = TextItem(self, font, text, pos, flags)
        return item

    def on_draw(self, screen: Surface, pos: Vec2):
        if self.mouse_focus:
            pygame.draw.rect(screen, COLOR_BUTTON_BG_HIGH, self.area.to_tuple())
        else:
            pygame.draw.rect(screen, COLOR_BUTTON_BG, self.area.to_tuple())