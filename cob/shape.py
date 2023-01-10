"""

Based on https://github.com/daumiller/ascendancy

"""
import os
from typing import List

import png

from engine.binary_reader import BinaryReader, open_binary_reader

PALETTE = List[List[int]]


def extract_shapes(filename: os.PathLike[str] | str, pal0: PALETTE):
    parent, file_ = os.path.split(os.path.abspath(filename))

    parent = os.path.join(parent, file_+'.ext')
    if not os.path.isdir(parent):
        os.makedirs(parent)
    with open_binary_reader(filename) as reader:
        read_shp_file(reader, parent, pal0)


def read_shp_file(reader: BinaryReader, parent: os.PathLike[str] | str, pal0: PALETTE):
    reader.set_endianness('LITTLE_ENDIAN')
    magic = reader.read_uint32()
    if magic != 0x30312E31:
        raise Exception("Invalid SHP file (bad signature).")
    image_count = reader.read_uint32()
    for i in range(image_count):
        off_dat = reader.read_uint32()
        off_pal = reader.read_uint32()
        off_restore = reader.position

        palette = pal0
        if off_pal != 0:
            reader.seek(off_pal)
            palette = read_palette(reader)
        elif pal0 is None:
            print("Default palette required for {}/{}; skipping...".format(i + 1, image_count))
            continue

        reader.seek(off_dat)
        shp_to_png(parent, palette, reader, i + 1, image_count)
        reader.seek(off_restore)


def read_palette(reader: BinaryReader, size=256) -> PALETTE:
    entries: PALETTE = []
    for index in range(size):
        rgb = reader.read_bytes(3)
        entries.append([rgb[0] << 2, rgb[1] << 2, rgb[2] << 2, 0xFF])
    return entries


def shp_to_png(path, palette: PALETTE, reader: BinaryReader, entry, total):
    __, parent = os.path.split(path)
    idx_len = len("{}".format(total))
    png_str = "{}".format(entry).rjust(idx_len, '0')
    png_str = "".join([png_str, '.png'])
    filename = os.path.join(path, png_str)
    test_name = os.path.join(parent, png_str)
    print(f'Writing {test_name} ... ')

    height = 1 + reader.read_uint16()
    width = 1 + reader.read_uint16()

    x_center = reader.read_uint16()
    y_center = reader.read_uint16()
    x_start = reader.read_int32()
    y_start = reader.read_int32()
    x_end = reader.read_int32()
    y_end = reader.read_int32()

    if (x_start > (width-1)) or (y_start > (width-1)):
        print("Unable to create {} (w:{}, h:{}, x:{}, y:{}).".format(test_name, width, height, x_start, y_start))
        return

    top = y_center + y_start
    bottom = y_center + y_end
    left = x_center + x_start

    background = [0, 0, 0, 0xFF]
    pad_row = background * width
    pad_left = background * left

    y = 0
    row = []
    pixels = []

    # this doesn't seem right... but works
    plane_width = width << 2
    read_width = (x_center + x_end + (x_center + x_start)) << 2
    if plane_width > read_width: read_width = plane_width

    while y < height:
        if (y < top) or (y >= bottom):
            pixels.append(pad_row)
            y += 1
            continue

        if len(row) == 0:
            row += pad_left

        b = reader.read_uint8()
        if b is None:
            print("Unable to create {} (hit EOF at {},{} of {},{}).".format(test_name, len(row) >> 2, y, width, height))
            return

        if b == 0:
            # this doesn't seem right either...
            if len(row) == len(pad_left):
                continue
            row += background * ((read_width - len(row)) >> 2)
        elif b == 1:
            num_bg_pixels = reader.read_uint8()
            row += background * num_bg_pixels
        elif (b & 1) == 0:
            index = reader.read_uint8() or 0
            clr = palette[index]
            repeat_clr = b >> 1
            row += clr * repeat_clr
        else:
            num_pixels = b >> 1
            for i in range(num_pixels):
                index = reader.read_uint8() or 0
                clr = palette[index]
                row += clr

        if len(row) == read_width:
            row = row[:plane_width]
            pixels.append(row)
            row = []
            y += 1

    with open(filename, 'wb') as png_file:
        w = png.Writer(width=width, height=height, bitdepth=8, alpha=True, greyscale=False)
        w.write(png_file, pixels)
