from pygame import Surface

from engine.shape import Shape
from foundation import Area, Vec2
from game.vis.ascendancy_control import AscendancyControl


class TurnCount(AscendancyControl):

    def __init__(self, parent, area: Area, shape: Shape = 0):
        super().__init__(parent, area)
        self.shape = shape
        self.turns = 0

    def on_draw(self, screen: Surface, pos: Vec2):
        super().on_draw(screen, pos)
        if not self.shape:
            return
        self.shape.draw(screen, pos, 67)
        number = self.turns
        digit_width = 32
        digit_pos = pos + Vec2(digit_width * 4, 0)
        for i in range(0, 5):
            digit = number % 10
            number = number // 10
            self.shape.draw(screen, digit_pos, digit + 55)
            digit_pos -= Vec2(digit_width, 0)
