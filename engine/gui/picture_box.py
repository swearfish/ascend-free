from pygame import Surface

from engine.gui.control import Control
from engine.sprite import Sprite
from engine.surface_renderer import SurfaceRenderer
from foundation.area import Area
from foundation.vector_2d import Vec2


class PictureBox(Control):
    def __init__(self, parent, area: Area, shape: SurfaceRenderer):
        super().__init__(parent, area)
        self.shape = shape

    def on_draw(self, screen: Surface, pos: Vec2):
        self.shape.draw(screen, pos)
