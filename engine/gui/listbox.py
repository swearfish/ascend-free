import pygame
from pygame import Surface

from engine.gui import Control, UiEventListener
from engine.gui.colors import COLOR_BUTTON_BG_HIGH, COLOR_BUTTON_BG
from engine.gui.scroll_bar import ScrollBar
from foundation import Area, Vec2
from foundation.area import area_with_size


class ListBox(Control, UiEventListener):
    def __init__(self, parent, area: Area, small: bool = False, items: list = [], items_per_page: int = 3):
        super().__init__(parent, area)
        scroll_bar_width = 15 if small else 25
        scroll_bar_area = area_with_size(area.width - scroll_bar_width, 0, scroll_bar_width, area.height)
        self._item_height = self.area.height / items_per_page
        self._items = items
        self._first_item = 0
        self._items_per_page = items_per_page
        self._highlight_item = -1
        self.scroll_bar = ScrollBar(self, scroll_bar_area, 0, len(self._items), items_per_page)

    def on_scroll(self, sender, direction, offset):
        self._first_item = offset

    def on_draw(self, screen: Surface, pos: Vec2):
        super().on_draw(screen, pos)
        item_area = area_with_size(pos.x, pos.y, self.area.width - self.scroll_bar.area.width, self._item_height)
        pygame.draw.rect(screen, COLOR_BUTTON_BG, self.area.as_tuple())
        for i in range(self._first_item, self._first_item + self._items_per_page):
            if len(self._items) <= i:
                return
            if self._highlight_item == i and self._mouse_focus:
                pygame.draw.rect(screen, COLOR_BUTTON_BG_HIGH, item_area.as_tuple())
            self._invoke_listener(lambda l: l.on_listbox_draw_item(self, screen, item_area, self._items[i], i))
            item_area = item_area.move_by(Vec2(0, self._item_height))

    def on_mouse_move(self, mouse_pos: Vec2) -> bool:
        if self._mouse_focus and mouse_pos.x < self.area.width - self.scroll_bar.area.width:
            self._highlight_item = mouse_pos.y // self._item_height + self._first_item
        else:
            self._highlight_item = -1
        return True
