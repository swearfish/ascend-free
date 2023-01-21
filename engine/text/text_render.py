import copy
from abc import abstractmethod

from pygame import Surface

from foundation.area import Area
from foundation.vector_2d import Vec2

TEXT_VCENTER = 1 << 0
TEXT_CENTER = 1 << 1
TEXT_WRAP = 1 << 2


class TextRenderer:
    def text_out(self, text: str, screen: Surface, pos: Vec2, mode: int = 0):
        screen_pos = copy.copy(pos)
        if mode != 0:
            size = self._measure_line(text)
        else:
            size = (0, 0)
        x, y = screen_pos.x, screen_pos.y
        if mode & TEXT_CENTER:
            x -= size.x / 2
        if mode & TEXT_VCENTER:
            y -= size.y / 2
        self._text_out(text, screen, Vec2(x, y))

    def measure_text(self, text: str, max_width: int, line_spacing=0, line_separator='\n') -> Vec2:
        lines, max_width = self._split_lines(text, max_width, line_separator)
        if len(lines) == 0:
            return Vec2(0, 0)
        if len(lines) == 1:
            return self._measure_line(lines[0])
        line_height, total_height = self._calc_height(len(lines), line_spacing)
        return Vec2(max_width, total_height)

    def draw_text(self, text: str, screen: Surface, area: Area, mode: int = 0, line_spacing=0, line_separator='\n'):
        lines, max_width = self._split_lines(text, area.width, line_separator)
        line_height, total_height = self._calc_height(len(lines), line_spacing)
        x, y = area.left, area.top
        flags = 0
        if mode & TEXT_CENTER:
            x += area.width // 2
            flags |= TEXT_CENTER
        if mode & TEXT_VCENTER:
            y += area.height // 2 - total_height // 2
        for line in lines:
            self.text_out(line, screen, Vec2(x, y), flags)
            y += line_height

    def _calc_height(self, num_lines: int, line_spacing: int) -> tuple[int, int]:
        line_height = self._measure_line('A').y + line_spacing
        total_height = num_lines * line_height - line_spacing
        return line_height, total_height

    def _split_lines(self, text: str, max_width: int, line_separator: str = '\n') -> tuple[list[str], int]:
        lines = []
        line = ""
        line_width = 0
        max_line_width = 0
        space_width = self._measure_line(' ').w
        while 0 < len(text):
            next_space = text.find(' ')
            if next_space > 0:
                word = text[0:next_space]
                text = text[next_space + 1:]
            else:
                word = text
                text = ""
            start_new_line = False
            if text.startswith(line_separator):
                start_new_line = True
                text = text[len(line_separator):]
            word_width = self._measure_line(word).w
            new_width = line_width + word_width
            if 0 < len(line):
                new_width += space_width
            if 0 < line_width and max_width < new_width:
                start_new_line = True
            if start_new_line:
                lines.append(line)
                line = word
                max_line_width = max(max_line_width, line_width)
                line_width = word_width
            else:
                line_width = new_width
                if 0 < len(line):
                    line = line + ' ' + word
                else:
                    line = word
        if line != "":
            max_line_width = max(max_line_width, line_width)
            lines.append(line)
        return lines, max_line_width

    @abstractmethod
    def _measure_line(self, text: str) -> Vec2:
        pass

    @abstractmethod
    def _text_out(self, text: str, screen: Surface, pos: Vec2):
        pass
