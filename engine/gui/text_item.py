from pygame import Surface

from engine.gui.button_item import ButtonItem
from engine.gui.control import Control
from engine.text.text_render import TextRenderer
from foundation.vector_2d import Vec2


class TextItem(ButtonItem):
    def __init__(self, parent: Control, font: TextRenderer, text: str, pos: Vec2, flags: int):
        super().__init__(parent, pos, flags)
        self.text = text
        self.font = font
        self.centered = True

    def draw_item(self, screen: Surface, pos: Vec2):
        self.font.text_out(self.text, screen, pos, self.flags)
