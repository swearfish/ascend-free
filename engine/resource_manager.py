import os.path

import pygame.image

from ascendancy_assets import Palette, ShapeFile
from ascendancy_assets.fnt_file import FntFile
from engine import FileSystem
from engine.gcom import gcom
from engine.sprite import Sprite
from engine.text.text_render import TextRenderer


class ResourceManager:
    def __init__(self):
        self.fs: FileSystem = gcom.get(FileSystem)
        self.fonts: dict[str, TextRenderer] = {}
        self.palette: dict[str, Palette] = {}

        self.game_pal = self.get_palette('data/game.pal')
        self.shapes: dict[str, ShapeFile] = {}

    def get_palette(self, name: str, start=0, size=256) -> Palette:
        if name in self.palette:
            return self.palette[name]
        with self.fs.open_file(name) as f:
            result = self.palette[name] = Palette(f, start, size)
            return result

    def read_gif(self, name: str):
        physical_file = self.fs.get_as_file(name)
        return pygame.image.load(physical_file)

    def read_shape(self, name: str, index: int = 1):
        if name not in self.shapes:
            with self.fs.open_file(name) as shp_file:
                shape = ShapeFile(shp_file, self.game_pal)
                self.shapes[name] = shape
        return self.shapes[name].images[index - 1]

    def image_from_shape(self, name: str, index: int = 1):
        extracted_name = f'{name}.ext/{index}.png'
        full_extracted_path = self.fs.get_cached_name(extracted_name)
        if not os.path.exists(full_extracted_path):
            self.read_shape(name, index).export_to_png(full_extracted_path)
        return pygame.image.load(full_extracted_path)

    def sprite_from_shape(self, name: str, index: int = -1, size=None):
        return Sprite(self.image_from_shape(name, index), size=size)

    def sprite_from_gif(self, name: str, size=None) -> Sprite:
        return Sprite(self.read_gif(name), size=size)

    def get_font(self, name: str, palette: Palette = None) -> TextRenderer:
        from engine.text.bitmap_font import BitmapFont
        from engine.text.bitmap_text_render import BitmapTextRenderer
        if name in self.fonts:
            return self.fonts[name]
        if palette is None:
            palette = self.game_pal
        with self.fs.open_file(name) as f:
            fnt_file = FntFile(name, f, palette)
            bitmap_font = BitmapFont(fnt_file)
            renderer = BitmapTextRenderer(bitmap_font)
            self.fonts[name] = renderer
            return renderer
