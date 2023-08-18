from .control import Control, MOUSE_SHIFT_MOD
from .ui_event_listener import UiEventListener
from foundation.area import area_with_size_vec
from foundation.vector_2d import Vec2


class StateFrame(Control):
    def __init__(self, state_number: int, shape_name: str, size: Vec2):
        super().__init__(parent = None, area=area_with_size_vec(Vec2(0,0), size))
        self.state_number = state_number
        self.shape_name = shape_name
        self.mouse_buttons = 0
        self.mouse_pos: Vec2 | None = None

    def update_mouse(self, mouse_pos: Vec2, buttons: tuple, shift: bool) -> bool:
        if mouse_pos != self.mouse_pos:
            self.handle_mouse_move(mouse_pos)
            self.mouse_pos = mouse_pos
        shift_flag = MOUSE_SHIFT_MOD if shift else 0
        handled = False
        for i in range(3):
            mb_flag = 1 << i
            if (buttons[i]) and (not self.mouse_buttons & mb_flag):
                handled = self.handle_mouse_down(mb_flag | shift_flag, mouse_pos)
                self.mouse_buttons |= mb_flag
            if (not buttons[i]) and (self.mouse_buttons & mb_flag):
                handled = self.handle_mouse_up(mb_flag | shift_flag, mouse_pos)
                self.mouse_buttons &= ~mb_flag
        return handled
