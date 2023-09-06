from foundation.area import area_with_size_vec
from foundation.vector_2d import Vec2
from game.vis.ascendancy_control import AscendancyControl
from .control import Control, MOUSE_SHIFT_MOD


class StateFrame(AscendancyControl):
    def __init__(self, state_number: int, shape_name: str, shape_frame: int, size: Vec2):
        super().__init__(parent=None, area=area_with_size_vec(Vec2(0, 0), size))
        self.state_number = state_number
        self.shape_name = shape_name
        self.shape_frame = shape_frame
        self.mouse_buttons = 0
        self.mouse_pos: Vec2 | None = None
        self.controls: dict[str, Control] = {}
        if self.shape_name is not None and self.shape_name != "":
            self.shape = self.resource_manager.shape_from_file(self.shape_name)
        else:
            self.shape = None

    def update_mouse(self, mouse_pos: Vec2, buttons: tuple, shift: bool) -> bool:
        if mouse_pos != self.mouse_pos:
            self.handle_mouse_move(mouse_pos)
            self.mouse_pos = mouse_pos
        shift_flag = MOUSE_SHIFT_MOD if shift else 0
        handled = False
        for i in range(3):
            mb_flag = 1 << i
            if (buttons[i]) and (not self.mouse_buttons & mb_flag):
                print(f'MOUSE DOWN {mouse_pos.x}, {mouse_pos.y}')
                handled = self.handle_mouse_down(mb_flag | shift_flag, mouse_pos)
                self.mouse_buttons |= mb_flag
            if (not buttons[i]) and (self.mouse_buttons & mb_flag):
                handled = self.handle_mouse_up(mb_flag | shift_flag, mouse_pos)
                self.mouse_buttons &= ~mb_flag
        return handled
