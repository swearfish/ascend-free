from pygame import Surface

from engine.gui.control import Control
from engine.text.text_render import TextRenderer
from foundation.area import Area
from foundation.vector import Vec2


class Label(Control):
    def __init__(self, parent, area: Area, text: str, font: TextRenderer, flags: int = 0, line_spacing = 0):
        super().__init__(parent, area)
        self.text = text
        self.font = font
        self.flags = flags
        self.line_spacing = line_spacing

    def on_draw(self, screen: Surface, pos: Vec2):
        self.font.draw_text(self.text, screen, self.area.new_origin(pos), self.flags, self.line_spacing)