"""

Originally based on https://github.com/daumiller/ascendancy

"""

import io
import os
import struct
import sys
from typing import AnyStr

from .cob_file import CobFile
from foundation import BinaryReader
from settings import ORIGINAL_TITLE


class CobArchive:
    def __init__(self, cob_file_name: str):
        try:
            self._handle = open(cob_file_name, 'rb')
        except Exception:
            print(f'FATAL ERROR: unable to open {cob_file_name}!')
            print(f'Please ensure that ASSETS directory is properly configured,')
            print(f'and copy original {ORIGINAL_TITLE["game_name"]} assets (*.cob) into the ASSETS directory!')
            print('')
            sys.exit()
        self._handle.seek(0, io.SEEK_SET)
        self.files: dict[str, CobFile] = {}
        num_files = struct.unpack('<i', self._handle.read(4))[0]
        if num_files < 1:
            return
        files = []
        for index in range(num_files):
            path = self._handle.read(50).partition(b'\0')[0].decode('utf-8')
            dir_name, file_name = os.path.split(path.replace('\\', '/'))
            file = CobFile(cob_file_name, dir_name, file_name)
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

    def get_file(self, name: str) -> CobFile:
        assert self.exists(name), f'{name} not found'
        file = self.files[name]
        return file

    def open_file(self, name: str) -> BinaryReader:
        return self.get_file(name).open_reader()

    def read_file(self, name: str) -> AnyStr:
        return self._read(self.get_file(name))

    def _read(self, file: CobFile) -> AnyStr:
        self._handle.seek(file.offset)
        return self._handle.read(file.size)
