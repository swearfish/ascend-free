import png

from ascendancy import Palette
from foundation import BinaryReader


class Font:
    def __init__(self, name: str, reader: BinaryReader, pal: Palette):
        self.name = name
        self.palette = pal
        self.color_key: int | None = None
        self.transparent_color: list[int] | None = None
        self.chars: dict[str, tuple] = {}
        self.character_height: int | None = None
        self.total_width = 0
        self.pixels = []
        self._read(reader)

    def measure_text(self, line: str):
        width = 0
        for c in line:
            if c not in self.chars:
                continue
            area = self.chars[c]
            chr_width = area[2] - area[0]
            width += chr_width
        return width, self.total_width

    def _read(self, reader: BinaryReader):
        magic = reader.read_uint32()
        if magic != 0x00002e31:
            raise Exception("Invalid FNT file (bad signature).")

        character_count = reader.read_uint32()
        self.character_height = reader.read_uint32()
        self.color_key = reader.read_uint32()
        self.transparent_color = self.palette.entries[self.color_key]

        self.pixels = []
        for i in range(self.character_height):
            self.pixels.append([])

        for i in range(character_count):
            off_char = reader.read_uint32()
            off_restore = reader.position
            reader.seek(off_char)
            self.chars[chr(i)] = self._read_chr(reader)
            reader.seek(off_restore)

    def _read_chr(self, reader: BinaryReader):
        width = reader.read_uint32()
        if not width:
            return

        result = (self.total_width, 0, width, self.character_height)
        self.total_width += width
        for y in range(self.character_height):
            row = self.pixels[y]
            for x in range(width):
                index = reader.read_uint8()
                row += self.palette.entries[index]
        return result

    def export_to_png(self, file_name: str):
        with open(file_name, 'wb') as f:
            w = png.Writer(width=self.total_width, height=self.character_height, bitdepth=8, alpha=True,
                           greyscale=False)
            w.write(f, self.pixels)
