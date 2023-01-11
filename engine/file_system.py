import ntpath
import os.path
from os import PathLike
from typing import AnyStr

from ascendancy import CobArchive, CobFile
from foundation import BinaryReader, binary_reader_from_buffer


class FileSystem:
    def __init__(self, assets_dir: str | PathLike[str], cache_dir: str | PathLike[str] | None = None):
        self.assets_dir = assets_dir
        self.cache_dir = cache_dir if cache_dir is not None else os.path.join(assets_dir, 'cache')
        os.makedirs(self.cache_dir, exist_ok=True)
        self.cobs = [CobArchive(os.path.join(self.assets_dir, f'ascend0{x}.cob')) for x in range(3)]

    def close(self):
        for cob in self.cobs:
            cob.close()

    def find_file(self, name: str, cob_index: int | None = None) -> CobFile:
        name = name.replace('\\', '/')
        if cob_index is None:
            for cob in self.cobs:
                if cob.exists(name):
                    return cob.get_file(name)
        else:
            cob = self.cobs[cob_index]
            if cob.exists(name):
                return cob.get_file(name)
        raise FileNotFoundError(f'{name}')

    def read_file(self, name: str, cob: int | None = None) -> AnyStr:
        file = self.find_file(name, cob)
        return file.read_all()

    def read_text(self, name: str, cob: int | None = None) -> str:
        return self.read_file(name, cob).decode('utf-8')

    def read_lines(self, name: str, cob: int | None = None, line_ending: str = '\r\n') -> list[str]:
        return self.read_text(name, cob).split(line_ending)

    def open_file(self, name: str, cob: int | None = None, buffered: bool = False) -> BinaryReader:
        if buffered:
            buffer = self.read_file(name, cob)
            return binary_reader_from_buffer(buffer, 'LITTLE_ENDIAN')
        else:
            return self.find_file(name, cob).open_reader()

    def get_cached_name(self, name: str) -> ntpath:
        name = name.replace('\\', '/')
        parts = name.split('/')
        cache_dir = self.cache_dir
        for i in range(0, len(parts) - 1):
            cache_dir = os.path.join(cache_dir, parts[i])
        os.makedirs(cache_dir, exist_ok=True)
        cache_file = os.path.join(cache_dir, parts[-1])
        return cache_file

    def get_as_file(self, name: str, cob: int | None = None) -> ntpath:
        cache_file = self.get_cached_name(name)
        if not os.path.exists(cache_file):
            content = self.read_file(name, cob)
            with open(cache_file, "wb") as f:
                f.write(content)
        return cache_file
