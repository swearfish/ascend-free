from pygame import Surface

from engine import FileSystem
from engine.gcom import gcom
from engine.text.bitmap_font import BitmapFont
from engine.text.text_render import TextRenderer
from foundation.vector_2d import Vec2


class BitmapTextRenderer(TextRenderer):
    def __init__(self, font: BitmapFont):
        self.file_system: FileSystem = gcom.get(FileSystem)
        self.font = font

    def _measure_line(self, text: str) -> Vec2:
        return self.font.measure_text(text)

    def _text_out(self, text: str, screen: Surface, pos: Vec2):
        atlas = self.font.atlas
        char_map = self.font.char_map
        x, y = pos.x, pos.y
        for ch in text:
            if ch not in char_map:
                continue
            area = char_map[ch]
            screen.blit(atlas, (x, y), area.as_tuple())
            x += area.width
