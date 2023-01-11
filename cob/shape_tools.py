import os

from cob.palette import Palette
from cob.shape import Shape
from cob.shape_image import ShapeImage
from engine.binary_reader import open_binary_reader, BinaryReader


def extract_shapes(filename: os.PathLike[str] | str, pal0: Palette):
    parent, file_ = os.path.split(os.path.abspath(filename))

    parent = os.path.join(parent, file_ + '.ext')
    if not os.path.isdir(parent):
        os.makedirs(parent)
    with open_binary_reader(filename) as reader:
        read_shp_file(reader, parent, pal0)


def read_shp_file(reader: BinaryReader, parent: os.PathLike[str] | str, pal0: Palette):
    reader.set_endianness('LITTLE_ENDIAN')
    shape_file = Shape(reader, pal0)
    image_count = len(shape_file.images)
    i = 1
    for image in shape_file.images:
        if image is not None:
            shp_to_png(parent, image, i, image_count)
        i += 1


def shp_to_png(path, shape_image: ShapeImage, entry, total):
    __, parent = os.path.split(path)
    idx_len = len("{}".format(total))
    png_str = "{}".format(entry).rjust(idx_len, '0')
    png_str = "".join([png_str, '.png'])
    filename = os.path.join(path, png_str)
    test_name = os.path.join(parent, png_str)
    print(f'Writing {test_name} ... ')
    shape_image.export_to_png(filename)
