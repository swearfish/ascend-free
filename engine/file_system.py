import ntpath
import os.path
from os import PathLike
from typing import AnyStr

from cob import CobArchive
from cob.shape import extract_shapes, read_palette
from engine.binary_reader import open_binary_reader


class FileSystem:
    def __init__(self, assets_dir: str | PathLike[str], cache_dir: str | PathLike[str] | None = None):
        self.assets_dir = assets_dir
        self.cache_dir = cache_dir if cache_dir is not None else os.path.join(assets_dir, 'cache')
        os.makedirs(self.cache_dir, exist_ok=True)
        self.cobs = [CobArchive(os.path.join(self.assets_dir, f'ascend0{x}.cob')) for x in range(3)]
        self.export_all(convert=True)

    def close(self):
        for cob in self.cobs:
            cob.close()

    def export_all(self, convert: bool = True):
        if convert:
            palette_file = self.get_as_file('data/game.pal')
            with open_binary_reader(palette_file) as br:
                palette = read_palette(br)

        for i in range(len(self.cobs)):
            cob = self.cobs[i]
            for name in cob.files:
                cache_file = self.get_as_file(name, i)
                if convert and (name.endswith('.shp') or name.endswith('.tmp')):
                    palette_file = self.get_as_file('data/game.pal')
                    extract_shapes(cache_file, palette)

    def read_file(self, name: str, cob: int | None = None) -> AnyStr:
        if cob is None:
            for i in range(len(self.cobs)):
                if self.cobs[i].exists(name):
                    return self.read_file(name, i)
            raise FileNotFoundError(f'{name}')
        return self.cobs[cob].read_file(name)

    def get_as_file(self, name: str, cob: int | None = None) -> ntpath:
        parts = name.split('/')
        cache_dir = self.cache_dir
        for i in range(0, len(parts) - 1):
            cache_dir = os.path.join(cache_dir, parts[i])
        os.makedirs(cache_dir, exist_ok=True)
        cache_file = os.path.join(cache_dir, parts[-1])
        if not os.path.exists(cache_file):
            content = self.read_file(name, cob)
            with open(cache_file, "wb") as f:
                f.write(content)
        return cache_file
