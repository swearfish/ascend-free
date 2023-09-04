"""

Originally based on https://github.com/daumiller/ascendancy

"""

from ..palette import Palette
from .shape_exception import ShapeException
from .shape_image import image_from_reader, ShapeImage
from foundation import BinaryReader

SHAPE_MAGIC = 0x30312E31


class ShapeFile:
    def __init__(self, reader: BinaryReader, default_palette: Palette, palette_shift=0):
        self.images: list[ShapeImage] = []
        self.default_palette: Palette = default_palette

        self._read_images(reader,palette_shift)

    def _read_images(self, reader: BinaryReader, palette_shift=0):
        reader.set_endianness('LITTLE_ENDIAN')
        magic = reader.read_uint32()
        if magic != SHAPE_MAGIC:
            raise ShapeException("Invalid SHP file (bad signature).")
        image_count = reader.read_uint32()
        for i in range(1, image_count+1):
            off_dat = reader.read_uint32()
            off_pal = reader.read_uint32()
            off_restore = reader.position

            palette = self.default_palette
            if off_pal != 0:
                reader.seek(off_pal)
                palette = Palette(reader)
            if palette is None:
                print(f'No palette for {i} / {image_count}, skipping')
                continue

            reader.seek(off_dat)
            shape = None
            try:
                shape = image_from_reader(palette, reader, palette_shift)
            except ShapeException as e:
                print(f'Failed to load {i} / {image_count} from {reader.name}: {e.msg}')
            except Exception as e:
                print(f'Failed to load {i} / {image_count} from {reader.name}: {e}')
            self.images.append(shape)
            reader.seek(off_restore)
