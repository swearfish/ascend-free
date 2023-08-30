import ntpath
import os.path
from typing import AnyStr, Optional

from ascendancy_assets import CobArchive, CobFile
from foundation import BinaryReader, binary_reader_from_buffer
from foundation.gcom import Component, auto_gcom


@auto_gcom
class FileSystem(Component):
    assets_dir: str
    cache_dir: Optional[str] = None

    def __init__(self):
        super().__init__()
        if self.cache_dir is None:
            self.cache_dir = os.path.join(self.assets_dir, 'cache')
        os.makedirs(self.cache_dir, exist_ok=True)
        self.cobs = [CobArchive(os.path.join(self.assets_dir, f'ascend0{x}.cob')) for x in range(3)]

    def close(self):
        for cob in self.cobs:
            cob.close()

    def find_file(self, name: str, cob_index: int | None = None) -> CobFile:
        name = name.replace('\\', '/').lower()
        if cob_index is None:
            for cob in self.cobs:
                if cob.exists(name):
                    return cob.get_file(name)
        else:
            cob = self.cobs[cob_index]
            if cob.exists(name):
                return cob.get_file(name)
        raise FileNotFoundError(f'{name}')

    def get_all_files(self):
        result = set()
        for cob in self.cobs:
            for file in cob.files:
                result.add(file)
        return result

    def read_file(self, name: str, cob: int | None = None) -> AnyStr:
        file = self.find_file(name, cob)
        return file.read_all()

    def read_text(self, name: str, cob: int | None = None) -> str:
        return self.read_file(name, cob).decode('utf-8')

    def read_lines(self, name: str, cob: int | None = None, line_ending: str = '\r\n', skip_empty_lines: bool = False) -> list[str]:
        result = self.read_text(name, cob).split(line_ending)
        if skip_empty_lines:
            result = list(filter(lambda x: x is not None and 0 < len(x), result))
        return result

    def open_file(self, name: str, cob: int | None = None, buffered: bool = False) -> BinaryReader:
        if buffered:
            buffer = self.read_file(name, cob)
            return binary_reader_from_buffer(buffer, 'LITTLE_ENDIAN')
        else:
            return self.find_file(name, cob).open_reader()

    def get_cached_name(self, name: str, include_cache_path=True) -> ntpath:
        name = name.replace('\\', '/')
        parts = name.split('/')
        cache_dir = self.cache_dir
        for i in range(0, len(parts) - 1):
            cache_dir = os.path.join(cache_dir, parts[i])
        os.makedirs(cache_dir, exist_ok=True)
        cache_file = os.path.join(cache_dir, parts[-1])
        # return cache_file
        return cache_file if include_cache_path else cache_file[len(self.cache_dir) + 1:]

    def get_as_file(self, name: str, cob: int | None = None, include_cache_path=True) -> ntpath:
        cache_file = self.get_cached_name(name)
        if not os.path.exists(cache_file):
            content = self.read_file(name, cob)
            with open(cache_file, "wb") as f:
                f.write(content)
        return cache_file if include_cache_path else cache_file[len(self.cache_dir) + 1:]
