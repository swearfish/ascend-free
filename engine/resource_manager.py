import pygame.image

from ascendancy import Palette
from engine import FileSystem
from engine.game_engine import the_engine


class ResourceManager:
    def __init__(self):
        self.fs: FileSystem = the_engine.get(FileSystem)
        self.game_pal = self.read_palette('data/game.pal')

    def read_palette(self, name: str) -> Palette:
        with self.fs.open_file(name) as f:
            return Palette(f)

    def read_gif(self, name: str):
        physical_file = self.fs.get_as_file(name)
        return pygame.image.load(physical_file)
