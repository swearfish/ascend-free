from os import PathLike
from typing import BinaryIO, AnyStr

from .binary_reader import BinaryReader, ENDIANNESS


class BinaryReaderIO(BinaryReader):
    def __init__(self, handle: BinaryIO, endianness: ENDIANNESS = 'NATIVE', close_handle: bool = True,
                 _offset: int = None, size: int = None):
        self._handle = handle
        self._close_handle = close_handle
        super().__init__(endianness)
        tmp_pos = self._handle.tell()
        if size is None:
            self._size = self._handle.seek(0, 2)
            self._handle.seek(tmp_pos)
        else:
            self._size = size
        self._offset = tmp_pos if _offset is None else _offset
        self._position = 0

    def seek(self, offset: int) -> int:
        self._position = min(self._size, offset)
        return self._handle.seek(self._offset + self._position) - self._offset

    @property
    def position(self) -> int:
        return self._position

    @property
    def remaining(self) -> int:
        return self._size - self._position

    def close(self):
        if self._close_handle:
            self._handle.close()

    def read_bytes(self, byte_count: int) -> AnyStr:
        to_read = min(byte_count, self.remaining)
        result = self._handle.read(to_read)
        self._position += len(result)
        return result


def binary_reader_from_file_path(file_name: PathLike[str] | str, endianness: ENDIANNESS = 'NATIVE') -> BinaryReader:
    handle = open(file_name, 'rb')
    return binary_reader_from_file_handle(handle, endianness)


def binary_reader_from_file_handle(handle: BinaryIO,
                                   endianness: ENDIANNESS = 'NATIVE',
                                   close_handle: bool = False,
                                   start_pos: int | None = None,
                                   size: int | None = None) -> BinaryReader:
    return BinaryReaderIO(handle, endianness, close_handle, start_pos, size)
