import pygame as pg

from ascendancy import Palette
from engine import FileSystem


class ResourceManager:
    def __init__(self, fs: FileSystem):
        self.fs = fs
        self.game_pal = self.read_palette('data/game.pal')
        pass

    def read_palette(self, name: str) -> Palette:
        with self.fs.open_file(name) as f:
            return Palette(f)

    def read_gif(self, name: str) -> pg.Surface:
        physical_file = self.fs.get_as_file(name)
        return pg.image.load(physical_file)