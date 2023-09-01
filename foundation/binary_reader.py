import struct
from abc import abstractmethod
from typing import AnyStr, Literal, Optional

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
    def __init__(self, endianness: ENDIANNESS = 'NATIVE'):
        self._fmt_i8 = None
        self._fmt_i16 = None
        self._fmt_i32 = None
        self._fmt_u8 = None
        self._fmt_u16 = None
        self._fmt_u32 = None
        self._endianness = None
        self.set_endianness(endianness)

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

    @abstractmethod
    def seek(self, offset: int) -> int:
        pass

    @property
    @abstractmethod
    def position(self) -> int:
        pass

    @property
    @abstractmethod
    def remaining(self) -> int:
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def read_bytes(self, byte_count: int) -> AnyStr:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    def read_all(self) -> AnyStr:
        return self.read_bytes(self.remaining)

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

    def _read_fmt(self, byte_count: int, fmt: str) -> Optional[int]:
        buffer = self.read_bytes(byte_count)
        if len(buffer) < byte_count:
            return None
        result = struct.unpack(fmt, buffer)
        return result[0]

    @staticmethod
    def _get_fmt_str(endianness: ENDIANNESS, signed: bool, size: int) -> str:
        endianness_chr = ENDIANNESS_CHR[endianness]
        format_chr = SIZE_CHR[size] if signed else U_SIZE_CHR[size]
        return endianness_chr + format_chr
