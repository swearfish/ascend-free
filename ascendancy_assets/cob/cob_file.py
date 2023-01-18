"""

Originally based on https://github.com/daumiller/ascendancy

"""

from typing import BinaryIO, AnyStr
from foundation import BinaryReader, binary_reader_from_file_handle


class CobFile:
    def __init__(self, cob_path: str, path: str, file_name: str):
        self.cob_path = cob_path
        self.path = path
        self.name = file_name
        self.size = 0
        self.offset = 0

    def open(self) -> BinaryIO:
        cob_file = open(self.cob_path, 'rb')
        cob_file.seek(self.offset)
        return cob_file

    def open_reader(self) -> BinaryReader:
        handle = self.open()
        return binary_reader_from_file_handle(handle, endianness='LITTLE_ENDIAN', close_handle=True, size=self.size)

    def read_all(self) -> AnyStr:
        with self.open() as f:
            return f.read(self.size)

    @property
    def full_name(self):
        return f'{self.path}/{self.name}' if self.path != '' else self.name

    def __repr__(self):
        return f'{self.full_name} [{self.size}@{self.offset}]'
