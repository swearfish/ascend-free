"""

Based on https://github.com/daumiller/ascendancy

"""
import io
import os
import struct
from typing import AnyStr


class CobFile:
    def __init__(self, path, file_name):
        self.path = path
        self.name = file_name
        self.size = 0
        self.offset = 0

    @property
    def full_name(self):
        return f'{self.path}/{self.name}' if self.path != '' else self.name

    def __repr__(self):
        return f'{self.full_name} [{self.size}@{self.offset}]'


class CobArchive:
    def __init__(self, file_name):
        self._handle = open(file_name, 'rb')
        self._handle.seek(0, io.SEEK_SET)
        self.files: dict[str, CobFile] = {}
        num_files = struct.unpack('<i', self._handle.read(4))[0]
        if num_files < 1:
            return
        files = []
        for index in range(num_files):
            path = self._handle.read(50).partition(b'\0')[0].decode('utf-8')
            dirname, file_name = os.path.split(path.replace('\\', '/'))
            file = CobFile(dirname, file_name)
            files.append(file)
            self.files[file.full_name] = file
        files[0].offset = struct.unpack('<I', self._handle.read(4))[0]
        for index in range(1, num_files):
            files[index].offset = struct.unpack('<I', self._handle.read(4))[0]
            files[index - 1].size = files[index].offset - files[index - 1].offset
        self._handle.seek(0, io.SEEK_END)
        files[num_files - 1].size = self._handle.tell() - files[num_files - 1].offset

    def close(self):
        self._handle.close()

    def exists(self, name: str) -> bool:
        return name in self.files

    def read_file(self, name: str) -> AnyStr:
        assert self.exists(name), f'{name} not found'
        file = self.files[name]
        return self._read(file)

    def _read(self, file: CobFile) -> AnyStr:
        self._handle.seek(file.offset)
        return self._handle.read(file.size)


def dump_file(content: AnyStr, file_name: str | os.PathLike[str]):
    with open(file_name, "wb") as f:
        f.write(content)
