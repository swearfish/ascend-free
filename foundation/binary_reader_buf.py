from typing import AnyStr

from .binary_reader import BinaryReader, ENDIANNESS


class BinaryReaderBuf(BinaryReader):
    def __init__(self, buffer: AnyStr, endianness: ENDIANNESS = 'NATIVE', name: str = None):
        super().__init__(endianness)
        self._buffer = buffer
        self._position = 0
        self._size = len(buffer)
        self._name = name

    def seek(self, offset: int) -> int:
        self._position = min(self._size, offset)
        return self._position

    @property
    def position(self) -> int:
        return self._position

    @property
    def remaining(self) -> int:
        return self._size - self._position

    @property
    def name(self) -> str:
        return self._name

    def close(self):
        pass

    def read_bytes(self, byte_count: int) -> AnyStr:
        to_read = min(byte_count, self.remaining)
        offset = self._position
        self._position += to_read
        result = self._buffer[offset: self._position]
        return result


def binary_reader_from_buffer(buffer: AnyStr, endianness: ENDIANNESS = 'NATIVE', name: str = None) -> BinaryReader:
    return BinaryReaderBuf(buffer, endianness, name=name)
