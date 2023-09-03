import pygame
from pygame import Surface

from engine.gui import Control
from engine.gui.colors import COLOR_BUTTON_BG_HIGH, COLOR_BUTTON_BG
from engine.resource_manager import ResourceManager
from foundation import Area, Vec2
from foundation.area import area_with_size
from foundation.gcom import auto_wire


@auto_wire
class ScrollBar(Control):
    resource_manager: ResourceManager

    def __init__(self, parent, area: Area, offset: int, max: int, items_per_page: int):
        super().__init__(parent, area, listener=parent)
        large = area.width > 15
        offset = 0 if large else 2
        self._highlight_top = False
        self._highlight_bottom = False
        self.area_top = area_with_size(0, 0, area.width, area.height / 2)
        self.area_bottom = area_with_size(0, area.height / 2, area.width, area.height / 2)
        self.shp_up = self.resource_manager.renderer_from_shape_or_gif('data/listbox.shp', offset)
        self.shp_down = self.resource_manager.renderer_from_shape_or_gif('data/listbox.shp', offset+1)
        self.offset = offset
        self._max = max
        self._items_per_page = items_per_page

    def handle_draw(self, screen: Surface, pos: Vec2):
        super().handle_draw(screen, pos)
        pygame.draw.rect(screen, COLOR_BUTTON_BG_HIGH if self._highlight_top and self._mouse_focus else COLOR_BUTTON_BG,
                         self.area_top.move_by(pos).as_tuple())
        pygame.draw.rect(screen, COLOR_BUTTON_BG_HIGH if self._highlight_bottom and self._mouse_focus else COLOR_BUTTON_BG,
                         self.area_bottom.move_by(pos).as_tuple())
        self.shp_up.draw(screen, pos, center=False)
        self.shp_down.draw(screen, Vec2(pos.x, pos.y + self.area.height-self.shp_up.height), center=False)

    def handle_mouse_move(self, mouse_pos: Vec2) -> bool:
        result = super().handle_mouse_move(mouse_pos)
        self._highlight_top = self._mouse_focus and mouse_pos.y < self.area.height / 2
        self._highlight_bottom = self._mouse_focus and mouse_pos.y >= self.area.height / 2
        return result

    def on_mouse_click(self, mouse_pos: Vec2) -> bool:
        if self._highlight_bottom and self.offset < self._max - self._items_per_page:
            self.offset += 1
            self._invoke_listener(lambda l: l.on_scroll(self, 1, self.offset))
        if self._highlight_top and self.offset > 0:
            self.offset -= 1
            self._invoke_listener(lambda l: l.on_scroll(self, -1, self.offset))
        return False

