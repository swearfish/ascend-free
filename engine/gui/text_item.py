from pygame import Surface

from engine.gui.control import Control
from engine.text.text_render import TextRenderer, TEXT_VCENTER, TEXT_CENTER
from foundation.area import area_with_size_vec
from foundation.vector import Vec2


class TextItem(Control):
    def __init__(self, parent: Control, font: TextRenderer, text: str, pos: Vec2, flags: int):
        super().__init__(parent, area=area_with_size_vec(Vec2(0,0), parent.area.size))
        self.pos = pos
        self.text = text
        self.flags = flags
        self.font = font

    def on_draw(self, screen: Surface, pos: Vec2):
        center = self.area.size / 2
        text_pos = pos + center + self.pos
        self.font.text_out(self.text, screen, text_pos, TEXT_CENTER | TEXT_VCENTER)