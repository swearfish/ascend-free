"""

Originally based on https://github.com/daumiller/ascendancy

"""

from foundation import BinaryReader


class Palette:
    def __init__(self, reader: BinaryReader, start=0, size=256):
        self.entries: list[list[int]] = []
        for index in range(start):
            self.entries.append([0, 0, 0])
        for index in range(size):
            rgb = reader.read_bytes(3)
            if len(rgb) < 3:
                break
            self.entries.append([rgb[0] << 2, rgb[1] << 2, rgb[2] << 2, 0xFF])

    def get_color_for_index(self, index: int, fn_transform):
        assert 0 <= index < len(self.entries), f"Color {index} is out of bounds"
        real_index = fn_transform(index) if fn_transform is not None else index
        assert 0 <= real_index < len(self.entries), f"Transformed color {real_index} is out of bounds"
        return self.entries[real_index]


def read_palette(reader: BinaryReader, size: int = 256) -> Palette:
    return Palette(reader, size)
