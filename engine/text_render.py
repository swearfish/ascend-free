import os.path
from typing import Optional

import pygame.image
from pygame import Surface

from ascendancy.fnt import Font
from engine import FileSystem
from engine.game_engine import the_engine
from engine.lin_alg import Vec2

TEXT_CENTER = 1
TEXT_VCENTER = 2


class TextRenderer:
    def __init__(self, font: Font):
        self.file_system: FileSystem = the_engine.get(FileSystem)
        self.font = font
        atlas_file_name = self.file_system.get_cached_name(font.name + '.png')
        if not os.path.isfile(atlas_file_name):
            font.export_to_png(atlas_file_name)
        self.atlas: dict[int, Surface] = {
            10: pygame.image.load(atlas_file_name)
        }
        self.chars: dict[int, dict] = {
            10: self.font.chars
        }
        self.atlas[10].set_colorkey(self.font.transparent_color)

    def measure_text(self, text: str | list[str], size: int = 10, line_separator: Optional[str] = None) -> Vec2:
        if isinstance(text, str):
            if line_separator is not None and line_separator in text:
                lines = text.split(line_separator)
                return self.measure_text(lines, line_separator=None)
            else:
                text = [text]
        width = 0
        height = 0
        for line in text:
            height += self.font.character_height
            line_width = self.font.measure_text(line)[0]
            width = max(width, line_width)
        if size == 10:
            return Vec2(width, height)
        else:
            return Vec2(int(width * size / 10.0), int(height * size / 10.0))

    def text_out(self, text: str, screen: Surface, pos: Vec2, font_size: int = 10, mode: int = 0):
        if mode != 0:
            size = self.measure_text(text, size=font_size)
        else:
            size = (0, 0)
        if mode and TEXT_CENTER:
            pos.x -= size[0] / 2
        if mode and TEXT_VCENTER:
            pos.y -= size[1] / 2
        if font_size not in self.atlas:
            self._scale_atlas(font_size)
        atlas = self.atlas[font_size]
        chars = self.chars[font_size]
        for ch in text:
            if ch not in chars:
                continue
            area = chars[ch]
            screen.blit(atlas, pos.to_tuple(), area)
            pos.x += area[2]

    def _scale_atlas(self, font_size):
        atlas_size = (self._scale(self.atlas[10].get_width(), font_size),
                      self._scale(self.atlas[10].get_height(), font_size))
        scaled_chars = {}
        for ch, area in self.font.chars.items():
            if area is None: continue
            scaled_area = self._scale_tuple(area, font_size)
            scaled_chars[ch] = scaled_area
        self.atlas[font_size] = pygame.transform.scale(self.atlas[10], atlas_size)
        self.chars[font_size] = scaled_chars

    def _scale(self, value, size: int) -> int:
        return int(value * size / 10.0)

    def _scale_tuple(self, values: tuple, size: int) -> list[int]:
        result = []
        for value in values:
            result.append(self._scale(value, size))
        return result
