import os
from typing import Optional

import pygame.image
import pygame.transform

from ascendancy_assets import FntFile
from engine import FileSystem
from foundation.gcom import gcom_instance
from engine.text.text_utils import _scale, _scale_tuple
from foundation.vector_2d import Vec2


class BitmapFont:
    def __init__(self, font: FntFile, atlas=None, char_map=None):
        self.file_system: FileSystem = gcom_instance.get(FileSystem)
        self.font = font
        atlas_file_name = self.file_system.get_cached_name(font.name + '.png')
        if not os.path.isfile(atlas_file_name):
            font.export_to_png(atlas_file_name)
        self.atlas = pygame.image.load(atlas_file_name) if atlas is None else atlas
        self.char_map: dict = self.font.char_map if char_map is None else char_map
        self.atlas.set_colorkey(self.font.transparent_color)

    def measure_text(self, text: str) -> Vec2:
        width = 0
        height = 0
        for ch in text:
            if ch not in self.char_map or self.char_map[ch] is None:
                continue
            area = self.char_map[ch]
            width += area.width
            height = max(height, area.height)
        return Vec2(width, height)

    def scale(self, size: Optional[float]):
        if size is None or size == 1:
            return self
        return self._scale_atlas(size)

    def _scale_atlas(self, font_size: Optional[float]):
        scaled_size = (_scale(self.atlas.get_width(), font_size),
                       _scale(self.atlas.get_height(), font_size))
        scaled_chars = {}
        for ch, area in self.char_map.items():
            if area is None:
                continue
            scaled_area = _scale_tuple(area, font_size)
            scaled_chars[ch] = scaled_area
        scaled_atlas = pygame.transform.scale(self.atlas, scaled_size)
        return BitmapFont(self.font, scaled_atlas, scaled_chars)
