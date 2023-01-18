from abc import abstractmethod
from typing import Optional

from pygame import Surface

from foundation.vector import Vec2

TEXT_CENTER = 2
TEXT_VCENTER = 1


class TextRenderer:
    def measure_text(self, text: str | list[str], line_separator: Optional[str] = None) -> Vec2:
        if isinstance(text, str):
            if line_separator is not None and line_separator in text:
                lines = text.split(line_separator)
                return self.measure_text(lines, line_separator=None)
            else:
                text = [text]
        width = 0
        height = 0
        for line in text:
            size = self._measure_line(line)
            height += size.y
            width = max(width, size.x)
        return Vec2(width, height)

    def text_out(self, text: str, screen: Surface, pos: Vec2, mode: int = 0):
        if mode != 0:
            size = self.measure_text(text)
        else:
            size = (0, 0)
        if mode & TEXT_CENTER:
            pos.x -= size.x / 2
        if mode & TEXT_VCENTER:
            pos.y -= size.y / 2
        self._text_out(text, screen, pos)

    @abstractmethod
    def _measure_line(self, text: str) -> Vec2:
        pass

    @abstractmethod
    def _text_out(self, text: str, screen: Surface, pos: Vec2):
        pass


