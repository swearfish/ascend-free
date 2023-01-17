from foundation import BinaryReader


class Palette:
    def __init__(self, reader: BinaryReader, start = 0, size=256):
        self.entries: list[list[int]] = []
        for index in range(start):
            self.entries.append([0, 0, 0])
        for index in range(size):
            rgb = reader.read_bytes(3)
            if len(rgb) < 3:
                break
            self.entries.append([rgb[0] << 2, rgb[1] << 2, rgb[2] << 2, 0xFF])

    def get_color_for_index(self, index: int):
        assert 0 <= index < len(self.entries), "Color {index} is out of bounds"
        return self.entries[index]


def read_palette(reader: BinaryReader, size: int = 256) -> Palette:
    return Palette(reader, size)
