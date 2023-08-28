from pygame import Surface

from foundation.area import Area
from foundation.vector_2d import Vec2
from .control import Control


class Canvas(Control):
    """
    Canvas is a Control that has its own surface
    """

    def __init__(self, parent, area: Area):
        super().__init__(parent, area)
        self._surface: Surface | None = None

    def handle_draw(self, screen: Surface, pos: Vec2):
        if self._surface is None or \
                self._surface.get_width() != self.area.width or \
                self._surface.get_height() != self.area.height:
            self._surface = Surface(self.area.size.as_tuple())
        super().handle_draw(self._surface, Vec2(0, 0))
        screen.blit(self._surface, pos.as_tuple())
