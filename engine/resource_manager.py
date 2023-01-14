import os.path

import pygame.image

from ascendancy import Palette, Shape
from engine import FileSystem
from engine.game_engine import the_engine
from engine.sprite import Sprite

COLOR_BUTTON_BG = (12, 32, 49)
COLOR_BUTTON_BG_HIGH = (16, 69, 77)

class ResourceManager:
    def __init__(self):
        self.fs: FileSystem = the_engine.get(FileSystem)
        self.game_pal = self.read_palette('data/game.pal')
        self.shapes: dict[str, Shape] = {}
        from ascendancy.windows_txt import load_windows_txt
        self.windows = load_windows_txt(self.fs.read_lines('windows.txt'))
        pass

    def read_palette(self, name: str) -> Palette:
        with self.fs.open_file(name) as f:
            return Palette(f)

    def read_gif(self, name: str):
        physical_file = self.fs.get_as_file(name)
        return pygame.image.load(physical_file)

    def read_shape(self, name: str, index: int = 1):
        if name not in self.shapes:
            with self.fs.open_file(name) as shp_file:
                shape = Shape(shp_file, self.game_pal)
                self.shapes[name] = shape
        return self.shapes[name].images[index-1]

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
