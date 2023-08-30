from pygame import Surface

from engine.gui.button_item import ButtonItem
from engine.gui.control import Control
from engine.resource_manager import ResourceManager
from foundation.gcom import auto_wire
from foundation.vector_2d import Vec2


@auto_wire
class ShapeItem(ButtonItem):
    resource_manger: ResourceManager

    def __init__(self, parent: Control, frame: int, shape: str, pos: Vec2, flags: int):
        super().__init__(parent, pos, flags)
        self.frame = frame
        self.shape = self.resource_manger.shape_from_file(shape)

    def draw_item(self, screen: Surface, pos: Vec2):
        if 0 < self.frame:
            self.shape.draw(screen, pos, self.frame)
