import os.path

import pygame.image

from ascendancy_assets import Palette, ShapeFile
from engine import FileSystem
from engine.sprite import Sprite, ShapeRenderer
from foundation.gcom import component_resolve, Component


@component_resolve
class ResourceManager(Component):
    file_system: FileSystem

    def __init__(self):
        self.palette: dict[str, Palette] = {}

        self.game_pal = self.get_palette('data/game.pal')
        self.shapes: dict[str, ShapeFile] = {}

    def get_palette(self, name: str, start=0, size=256) -> Palette:
        if name in self.palette:
            return self.palette[name]
        with self.file_system.open_file(name) as f:
            result = self.palette[name] = Palette(f, start, size)
            return result

    def surface_from_gif(self, name: str):
        physical_file = self.file_system.get_as_file(name)
        return pygame.image.load(physical_file)

    def read_shape(self, name: str, index: int = 1):
        if name not in self.shapes:
            with self.file_system.open_file(name) as shp_file:
                shape = ShapeFile(shp_file, self.game_pal)
                self.shapes[name] = shape
        return self.shapes[name].images[index - 1]

    def surface_from_shape_file(self, name: str, index: int = 1):
        extracted_name = f'{name}.ext/{index}.png'
        full_extracted_path = self.file_system.get_cached_name(extracted_name)
        if not os.path.exists(full_extracted_path):
            self.read_shape(name, index).export_to_png(full_extracted_path)
        return pygame.image.load(full_extracted_path)

    def sprite_from_shape_file(self, name: str, index: int = -1, size=None) -> Sprite:
        return Sprite(self.surface_from_shape_file(name, index), size=size)

    def load_shape(self, name: str, index: int = -1, size=None) -> ShapeRenderer:
        if name.lower().endswith('.gif'):
            return ShapeRenderer(self.surface_from_gif(name), size=size)
        else:
            return ShapeRenderer(self.surface_from_shape_file(name, index), size=size)

    def sprite_from_gif(self, name: str, size=None) -> Sprite:
        return Sprite(self.surface_from_gif(name), size=size)
