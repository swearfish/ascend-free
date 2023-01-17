from engine.gui.control import Control
from foundation.area import area_with_size_vec
from foundation.vector import Vec2


class StateFrame(Control):
    def __init__(self, state_number: int, shape_name: str, size: Vec2):
        super().__init__(parent = None, area=area_with_size_vec(Vec2(0,0), size))
        self.state_number = state_number
        self.shape_name = shape_name
