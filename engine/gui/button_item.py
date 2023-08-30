from pygame import Surface

from engine.gui.control import Control
from engine.text.text_render import TextRenderer
from foundation.area import area_with_size_vec
from foundation.vector_2d import Vec2


class ButtonItem(Control):
    def __init__(self, parent: Control, pos: Vec2, flags: int):
        super().__init__(parent, area=area_with_size_vec(Vec2(0, 0), parent.area.size))
        self.pos = pos
        self.flags = flags
        self.centered = False

    def draw_item(self, screen: Surface, pos: Vec2):
        pass

    def on_draw(self, screen: Surface, pos: Vec2):
        if self.centered:
            center = self.area.size / 2
            left = center.x if self.pos.x == 0 else self.pos.x
            top = center.y if self.pos.y == 0 else self.pos.y
            item_pos = pos + Vec2(left, top)
        else:
            item_pos = pos + self.pos
        self.draw_item(screen, item_pos)
