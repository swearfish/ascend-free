from pygame import Surface

from foundation.area import Area
from foundation.vector import Vec2

MOUSE_BUTTON_LEFT = 1
MOUSE_BUTTON_RIGHT = 2
MOUSE_SHIFT_KEY = 4


class Control:
    def __init__(self, parent, area: Area, name: str = None):
        self.children: list[Control] = []
        self.name = name
        self.area = area
        self.parent: Control | None = parent
        self.active_control: Control | None = None
        self.mouse_focus = False
        if self.parent is not None:
            self.parent.children.append(self)
        pass

    def on_draw(self, screen: Surface, pos: Vec2):
        pass

    def on_mouse_enter(self):
        pass

    def on_mouse_leave(self):
        pass

    def on_mouse_click(self, mouse_pos: Vec2) -> bool:
        return False

    def on_mouse_down(self, button: int, mouse_pos: Vec2) -> bool:
        return False

    def on_mouse_up(self, button: int, mouse_pos: Vec2) -> bool:
        return False

    def on_mouse_move(self, mouse_pos: Vec2) -> bool:
        return False

    def handle_mouse_move(self, mouse_pos: Vec2) -> bool:
        handled = False
        for c in self.children:
            if c.area.contains(mouse_pos):
                if not c.mouse_focus:
                    c.on_mouse_enter()
                    c.mouse_focus = True
                handled = c.handle_mouse_move(mouse_pos - c.area.top_left)
            else:
                if c.mouse_focus and self.active_control != c:
                    c.on_mouse_leave()
                    c.mouse_focus = False
        if not handled:
            handled = self.on_mouse_move(mouse_pos)
        return handled

    def handle_mouse_down(self, button: int, mouse_pos: Vec2):
        handled = False
        for c in self.children:
            if c.area.contains(mouse_pos):
                if button & MOUSE_BUTTON_LEFT:
                    self.active_control = c
                handled = c.handle_mouse_down(button, mouse_pos - c.area.top_left)
        if not handled:
            handled = self.on_mouse_down(button, mouse_pos)
        return handled

    def handle_mouse_up(self, button: int, mouse_pos: Vec2):
        handled = False
        if self.active_control is not None:
            if button & MOUSE_BUTTON_LEFT:
                if self.active_control.area.contains(mouse_pos):
                    handled = handled or self.active_control.on_mouse_click(mouse_pos)
                handled = handled or self.active_control.handle_mouse_up(button, mouse_pos - self.active_control.area.top_left)
                self.active_control.mouse_focus = False
                self.active_control = None
        else:
            for c in self.children:
                if c.area.contains(mouse_pos):
                    handled = c.handle_mouse_up(button, mouse_pos - c.area.top_left)
        if not handled:
            handled = self.on_mouse_up(button, mouse_pos)
        return handled

    def handle_draw(self, screen: Surface, pos: Vec2):
        self.on_draw(screen, pos)
        for c in self.children:
            c.handle_draw(screen, pos + c.area.top_left)
