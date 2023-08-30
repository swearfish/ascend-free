import os.path

import pygame.image

from ascendancy_assets import Palette, ShapeFile, ShapeImage
from engine import FileSystem
from engine.sprite import Sprite
from engine.shape import Shape
from engine.surface_renderer import SurfaceRenderer
from foundation import Vec2
from foundation.gcom import Component, auto_gcom


@auto_gcom
class ResourceManager(Component):
    file_system: FileSystem

    def __init__(self):
        super().__init__()
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

    def read_shape_file(self, name: str) -> ShapeFile:
        if name not in self.shapes:
            with self.file_system.open_file(name) as shp_file:
                shape = ShapeFile(shp_file, self.game_pal)
                self.shapes[name] = shape
        return self.shapes[name]

    def read_shape_image(self, name: str, index: int = 1) -> ShapeImage:
        shape = self.read_shape_file(name)
        return shape.images[index - 1]

    def _surface_from_shape_image(self, shape_name: str, index: int, shape_image: ShapeImage):
        extracted_name = f'{shape_name}.ext/{index}.png'
        full_extracted_path = self.file_system.get_cached_name(extracted_name)
        if not os.path.exists(full_extracted_path):
            shape_image.export_to_png(full_extracted_path)
        return pygame.image.load(full_extracted_path)

    def surface_from_shape_file(self, name: str, index: int = 1):
        shape_image = self.read_shape_image(name, index)
        return self._surface_from_shape_image(name, index, shape_image)

    def shape_from_file(self, name: str, center=Vec2(0, 0), size=None) -> Shape:
        shape_file = self.read_shape_file(name)
        surfaces = []
        for image in shape_file.images:
            index = len(surfaces)
            if image:
                surface = self._surface_from_shape_image(name, index, image)
            else:
                surface = None
            surfaces.append(surface)
        return Shape(surfaces, center, size)

    def sprite_from_shape_file(self, name: str, center = Vec2(0, 0), size=None) -> Sprite:
        template = self.shape_from_file(name, center, size)
        return Sprite(template)

    def renderer_from_shape_or_gif(self, name: str, index: int = 1, size=None) -> SurfaceRenderer:
        if name.lower().endswith('.gif'):
            return SurfaceRenderer(self.surface_from_gif(name), size=size)
        else:
            return SurfaceRenderer(self.surface_from_shape_file(name, index), size=size)

    def sprite_from_gif(self, name: str, size=None) -> Sprite:
        return Sprite(self.surface_from_gif(name), size=size)

    def cache_all(self):
        for file in self.file_system.get_all_files():
            full_path = self.file_system.get_as_file(file)
            try:
                if file.lower().endswith('shp') or file.lower().endswith('tmp'):
                    shape = self.shape_from_file(file)
            except Exception as e:
                print(f'Failed to process file: {file}@{full_path} -- {e}')
