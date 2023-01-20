import copy
from abc import abstractmethod
from typing import Optional

from pygame import Surface

from foundation.area import Area
from foundation.vector import Vec2

TEXT_VCENTER = 1 << 0
TEXT_CENTER = 1 << 1
TEXT_WRAP = 1 << 2

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
        screen_pos = copy.copy(pos)
        if mode != 0:
            size = self.measure_text(text)
        else:
            size = (0, 0)
        if mode & TEXT_CENTER:
            screen_pos.x -= size.x / 2
        if mode & TEXT_VCENTER:
            screen_pos.y -= size.y / 2
        self._text_out(text, screen, screen_pos)

    def draw_text(self, text: str, screen: Surface, area: Area, mode: int = 0, line_spacing = 0):
        lines = []
        line = ""
        line_width = 0
        space_width = self._measure_line(' ').x
        while 0 < len(text):
            next_space = text.find(' ')
            if next_space > 0:
                word = text[0:next_space]
                text = text[next_space+1:]
            else:
                word = text
                text = ""
            start_new_line = False
            if text.startswith('@@'):
                start_new_line = True
                text = text[2:]
            word_width = self._measure_line(word).x
            new_width = line_width + word_width
            if 0 < len(line):
                new_width += space_width
            if 0 < line_width and area.width < new_width:
                start_new_line = True
            if start_new_line:
                lines.append(line)
                line = word
                line_width = word_width
            else:
                line_width = new_width
                if 0 < len(line):
                    line = line + ' ' + word
                else:
                    line = word
        if line != "":
            lines.append(line)
        line_height = self._measure_line('A').y + line_spacing
        total_height = len(lines) * line_height - line_spacing
        pos = area.top_left
        flags = 0
        if mode & TEXT_CENTER:
            pos.x += area.width // 2
            flags |= TEXT_CENTER
        if mode & TEXT_VCENTER:
            pos.y += area.height // 2 - total_height // 2
        for line in lines:
            self.text_out(line, screen, pos, flags)
            pos.y += line_height


    @abstractmethod
    def _measure_line(self, text: str) -> Vec2:
        pass

    @abstractmethod
    def _text_out(self, text: str, screen: Surface, pos: Vec2):
        pass


