import os
from pathlib import Path

import png

from ascendancy.palette import Palette
from ascendancy.shp.shape_exception import ShapeException
from foundation import BinaryReader


class ShapeImageReader:
    def __init__(self, palette: Palette, reader: BinaryReader):
        self.palette = palette
        self._read_header(reader)
        self._calc_bounds()

        self.background = [0, 0, 0, 0xFF]
        self.pad_row = self.background * self.width
        self.pad_left = self.background * self.left

        self.pixels = self._read_pixels(reader)

    # noinspection PyAttributeOutsideInit
    def _read_header(self, reader: BinaryReader):
        self.height = 1 + reader.read_uint16()
        self.width = 1 + reader.read_uint16()
        self.x_center = reader.read_uint16()
        self.y_center = reader.read_uint16()
        self.x_start = reader.read_int32()
        self.y_start = reader.read_int32()
        self.x_end = reader.read_int32()
        self.y_end = reader.read_int32()
        if (self.x_start > (self.width - 1)) or (self.y_start > (self.width - 1)):
            raise ShapeException(f"Invalid bounds (w:{self.width}, h:{self.height}, x:{self.x_start}, y:{self.x_end}).")

    # noinspection PyAttributeOutsideInit
    def _calc_bounds(self):
        self.top = self.y_center + self.y_start
        self.bottom = self.y_center + self.y_end
        self.left = self.x_center + self.x_start

    def _read_pixels(self, reader: BinaryReader):
        y = 0
        row = []
        pixels = []

        # this doesn't seem right... but works
        plane_width = self.width << 2
        read_width = (self.x_center + self.x_end + (self.x_center + self.x_start)) << 2
        if plane_width > read_width:
            read_width = plane_width

        while y < self.height:
            if (y < self.top) or (y >= self.bottom):
                pixels.append(self.pad_row)
                y += 1
                continue

            if len(row) == 0:
                row += self.pad_left

            b = reader.read_uint8()
            if b is None:
                raise ShapeException(f"hit EOF at {len(row)} >> 2,{y} of {self.width},{self.height}).")

            if b == 0:
                # this doesn't seem right either...
                if len(row) == len(self.pad_left):
                    continue
                row += self.background * ((read_width - len(row)) >> 2)
            elif b == 1:
                num_bg_pixels = reader.read_uint8()
                row += self.background * num_bg_pixels
            elif (b & 1) == 0:
                index = reader.read_uint8() or 0
                clr = self.palette.get_color_for_index(index)
                repeat_clr = b >> 1
                row += clr * repeat_clr
            else:
                num_pixels = b >> 1
                for i in range(num_pixels):
                    index = reader.read_uint8() or 0
                    clr = self.palette.get_color_for_index(index)
                    row += clr

            if len(row) == read_width:
                row = row[:plane_width]
                pixels.append(row)
                row = []
                y += 1
        return pixels


class ShapeImage:
    def __init__(self, reader: ShapeImageReader):
        self.palette = reader.palette
        self.pixels = reader.pixels
        self.width = reader.width
        self.height = reader.height

    def export_to_png(self, file_name: str | os.PathLike[str] | Path):
        with open(file_name, 'wb') as png_file:
            w = png.Writer(width=self.width, height=self.height, bitdepth=8, alpha=True, greyscale=False)
            w.write(png_file, self.pixels)


def image_from_reader(palette: Palette, reader: BinaryReader) -> ShapeImage:
    reader = ShapeImageReader(palette, reader)
    image = ShapeImage(reader)
    return image
