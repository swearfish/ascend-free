import pygame.draw
from pygame import Surface

from engine.gui.control import Control
from engine.gui.shape_item import ShapeItem
from engine.gui.text_item import TextItem
from engine.text.text_render import TextRenderer
from foundation.area import Area
from foundation.vector_2d import Vec2

COLOR_BUTTON_BG = (12, 32, 49)
COLOR_BUTTON_BG_HIGH = (16, 69, 77)


class Button(Control):
    def __init__(self, parent, name: str, area: Area,
                 help_index: str = None, message: any = None,
                 mouse_focus: bool = True):
        super().__init__(parent, area)
        self.name = name
        self.area = area
        self.help_index = help_index
        self._message = message
        self._highlight_on_focus = mouse_focus

    @property
    def title(self) -> str:
        item: TextItem = self.get_child_of_class(TextItem)
        return item.text

    @title.setter
    def title(self, value):
        item: TextItem = self.get_child_of_class(TextItem)
        item.text = value

    @property
    def shape_frame(self) -> int:
        item: ShapeItem = self.get_child_of_class(ShapeItem)
        return item.frame

    @shape_frame.setter
    def shape_frame(self, value):
        item: ShapeItem = self.get_child_of_class(ShapeItem)
        item.frame = value

    def add_text_item(self, font: TextRenderer, text: str, pos: Vec2, flags: int):
        item = TextItem(self, font, text, pos, flags)
        return item

    def add_shape_item(self, frame: int, shape: str, pos: Vec2, flags: int):
        item = ShapeItem(self, frame, shape, pos, flags)
        return item

    def on_draw(self, screen: Surface, pos: Vec2):
        if self._mouse_focus and self._highlight_on_focus:
            pygame.draw.rect(screen, COLOR_BUTTON_BG_HIGH, self.area.new_origin(pos).as_tuple())
        else:
            pygame.draw.rect(screen, COLOR_BUTTON_BG, self.area.new_origin(pos).as_tuple())

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'BUTTON {self.name} @ [{self.area}] :: {self._message}'
