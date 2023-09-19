from pygame import Surface

from .ui_event_listener import UiEventListener
from foundation.area import Area
from foundation.vector_2d import Vec2

MOUSE_BUTTON_LEFT = 1
MOUSE_BUTTON_RIGHT = 2
MOUSE_SHIFT_MOD = 128


class Control:
    def __init__(self, parent, area: Area, name: str = None, listener: UiEventListener = None):
        self.children: list[Control] = []
        self.name = name
        self.area = area
        self.parent: Control | None = parent
        self.visible = True
        self._active_control: Control | None = None
        self._mouse_focus = False
        self._message = None
        self._listener = listener
        self._modal: Control | None = None
        self._garbage = False
        if self.parent is not None:
            self.parent.children.append(self)
        self.on_click_handler = None

    @property
    def listener(self):
        if self._listener is not None:
            return self._listener
        if self.parent is not None:
            return self.parent._listener
        return None

    @listener.setter
    def listener(self, value):
        self._listener = value

    def invoke_listener(self, fn) -> bool:
        listener = self.listener
        if listener is not None:
            return fn(listener)
        return False

    def on_draw(self, screen: Surface, pos: Vec2):
        pass

    def on_update(self, total_time: float, frame_time: float):
        pass

    def on_mouse_enter(self):
        pass

    def on_mouse_leave(self):
        pass

    # noinspection PyUnusedLocal
    def on_mouse_click(self, mouse_pos: Vec2) -> bool:
        if self.on_click_handler is not None:
            self.on_click_handler(self, self._message)
        else:
            return self.invoke_listener(lambda listener: listener.on_click(self, self._message))

    # noinspection PyUnusedLocal,PyMethodMayBeStatic
    def on_mouse_down(self, button: int, mouse_pos: Vec2) -> bool:
        return False

    # noinspection PyUnusedLocal,PyMethodMayBeStatic
    def on_mouse_up(self, button: int, mouse_pos: Vec2) -> bool:
        return False

    # noinspection PyUnusedLocal,PyMethodMayBeStatic
    def on_mouse_move(self, mouse_pos: Vec2) -> bool:
        return False

    def handle_mouse_move(self, mouse_pos: Vec2) -> bool:
        if self._garbage or not self.visible:
            return False
        if self._modal is not None:
            if self._modal.area.contains(mouse_pos):
                return self._modal.handle_mouse_move(mouse_pos - self._modal.area.top_left)
            else:
                return False
        handled = False
        for c in self.children:
            if c.visible and c.area.contains(mouse_pos):
                if not c._mouse_focus:
                    c.on_mouse_enter()
                    c._mouse_focus = True
                handled = c.handle_mouse_move(mouse_pos - c.area.top_left)
            else:
                if c._mouse_focus and self._active_control != c:
                    c.on_mouse_leave()
                    c._mouse_focus = False
        if not handled:
            handled = self.on_mouse_move(mouse_pos)
        return handled

    def handle_mouse_down(self, button: int, mouse_pos: Vec2):
        if self._garbage or not self.visible:
            return False
        if self._modal is not None:
            if self._modal.area.contains(mouse_pos):
                return self._modal.handle_mouse_down(button, mouse_pos - self._modal.area.top_left)
            else:
                return False
        handled = False
        for c in self.children:
            if c.visible and c.area.contains(mouse_pos):
                if button & MOUSE_BUTTON_LEFT:
                    self._active_control = c
                handled = c.handle_mouse_down(button, mouse_pos - c.area.top_left)
        if not handled:
            handled = self.on_mouse_down(button, mouse_pos)
        return handled

    def handle_mouse_up(self, button: int, mouse_pos: Vec2):
        if self._garbage or not self.visible:
            return False
        if self._modal is not None:
            return self._modal.handle_mouse_up(button, mouse_pos - self._modal.area.top_left)
        handled = False
        if self._active_control is not None:
            if button & MOUSE_BUTTON_LEFT:
                if self._active_control.area.contains(mouse_pos):
                    handled = handled or self._active_control.on_mouse_click(
                        mouse_pos - self._active_control.area.top_left)
                if not handled:
                    handled = self._active_control.handle_mouse_up(button,
                                                                   mouse_pos - self._active_control.area.top_left)
                # self._active_control._mouse_focus = False
                self._active_control = None
        else:
            for c in self.children:
                if c.visible and c.area.contains(mouse_pos):
                    handled = c.handle_mouse_up(button, mouse_pos - c.area.top_left)
        if not handled:
            handled = self.on_mouse_up(button, mouse_pos)
        return handled

    def show_modal(self, modal_wnd):
        self._modal = modal_wnd
        self._modal.parent = self
        return

    def close(self):
        if self.parent is not None:
            if self.parent._modal == self:
                self.parent._modal = None
        self._garbage = True

    def handle_draw(self, screen: Surface, pos: Vec2):
        if self._garbage or not self.visible:
            return False
        self.on_draw(screen, pos)
        do_collect = False
        for c in self.children:
            if c._garbage:
                do_collect = True
            elif c.visible and self._modal != c:
                c.handle_draw(screen, pos + c.area.top_left)
        if self._modal is not None:
            if self._modal._garbage:
                self._modal = None
            else:
                self._modal.handle_draw(screen, pos + self._modal.area.top_left)
        if do_collect:
            # noinspection PyProtectedMember
            self.children = list(filter(lambda x: not x._garbage, self.children))

    def handle_update(self, total_time: float, frame_time: float):
        if self._garbage or not self.visible:
            return
        self.on_update(total_time, frame_time)
        for c in self.children:
            c.handle_update(total_time, frame_time)

    def get_children_of_class(self, clazz) -> list:
        result = []
        for item in self.children:
            if isinstance(item, clazz):
                result.append(item)
        return result

    def get_child_of_class(self, clazz):
        result = self.get_children_of_class(clazz)
        assert 0 < len(result)
        return result[0]
