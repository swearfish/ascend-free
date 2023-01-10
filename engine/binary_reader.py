import struct
from os import PathLike
from typing import BinaryIO, AnyStr, Literal, Optional

ENDIANNESS = Literal['LITTLE_ENDIAN', 'BIG_ENDIAN', 'NATIVE']

ENDIANNESS_CHR = {
    'LITTLE_ENDIAN': '<',
    'BIG_ENDIAN': '>',
    'NATIVE': '!',
}

SIZE_CHR = {
    8: 'b',
    16: 'h',
    32: 'i',
}

U_SIZE_CHR = {
    8: 'B',
    16: 'H',
    32: 'I',
}


class BinaryReader:
    def __init__(self, handle: BinaryIO, endianness: ENDIANNESS = 'NATIVE', close_handle: bool = True,
                 start_pos: int = None, size: int = None):
        self._fmt_i8 = None
        self._fmt_i16 = None
        self._fmt_i32 = None
        self._fmt_u8 = None
        self._fmt_u16 = None
        self._fmt_u32 = None
        self._endianness = None
        self._handle = handle
        self.set_endianness(endianness)
        self._close_handle = close_handle
        tmp_pos = self._handle.tell()
        if size is None:
            self._size = self._handle.seek(0, 2)
            self._handle.seek(tmp_pos)
        else:
            self._size = size
        self._start_pos = tmp_pos if start_pos is None else start_pos
        self._position = self._start_pos

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def set_endianness(self, endianness: ENDIANNESS):
        if self._endianness == endianness:
            return
        self._endianness = endianness
        self._fmt_i8 = self._get_fmt_str(self._endianness, signed=True, size=8)
        self._fmt_i16 = self._get_fmt_str(self._endianness, signed=True, size=16)
        self._fmt_i32 = self._get_fmt_str(self._endianness, signed=True, size=32)
        self._fmt_u8 = self._get_fmt_str(self._endianness, signed=False, size=8)
        self._fmt_u16 = self._get_fmt_str(self._endianness, signed=False, size=16)
        self._fmt_u32 = self._get_fmt_str(self._endianness, signed=False, size=32)

    def eof(self):
        return self.remaining <= 0

    def seek(self, offset: int) -> int:
        self._position = min(self._size, offset)
        return self._handle.seek(self._start_pos + self._position) - self._start_pos

    @property
    def position(self) -> int:
        return self._position

    @property
    def remaining(self) -> int:
        return self._size - self._position

    def close(self):
        if self._close_handle:
            self._handle.close()

    def read_int8(self) -> Optional[int]:
        return self._read_fmt(1, self._fmt_i8)

    def read_uint8(self) -> Optional[int]:
        return self._read_fmt(1, self._fmt_u8)

    def read_int16(self) -> Optional[int]:
        return self._read_fmt(2, self._fmt_i16)

    def read_uint16(self) -> Optional[int]:
        return self._read_fmt(2, self._fmt_u16)

    def read_int32(self) -> Optional[int]:
        return self._read_fmt(4, self._fmt_i32)

    def read_uint32(self) -> Optional[int]:
        return self._read_fmt(4, self._fmt_u32)

    def read_bytes(self, byte_count: int) -> AnyStr:
        to_read = min(byte_count, self.remaining)
        result = self._handle.read(to_read)
        self._position += len(result)
        return result

    def _read_fmt(self, byte_count: int, fmt: str) -> Optional[int]:
        buffer = self.read_bytes(byte_count)
        if len(buffer) < byte_count:
            return None
        result = struct.unpack(fmt, buffer)
        return result[0]

    @staticmethod
    def _get_fmt_str(endianness: ENDIANNESS, signed: bool, size: int) -> str:
        endianness_chr = ENDIANNESS_CHR[endianness]
        if signed:
            format_chr = SIZE_CHR[size]
        else:
            format_chr = U_SIZE_CHR[size]
        return endianness_chr + format_chr


def open_binary_reader(file_name: PathLike[str] | str, endianness: ENDIANNESS = 'NATIVE') -> BinaryReader:
    handle = open(file_name, 'rb')
    return BinaryReader(handle, endianness)
