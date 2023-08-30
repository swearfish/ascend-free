from pygame import Surface

from engine.surface_renderer import SurfaceRenderer
from foundation import Vec2

surface_like = SurfaceRenderer | Surface
shape_images_like = surface_like | list[surface_like]


class Shape:
    def __init__(self, image: shape_images_like, center=Vec2(0, 0), size: Vec2 = None):
        if isinstance(image, SurfaceRenderer) and size is None:
            self._shapes = [image]
        elif isinstance(image, list):
            self._shapes = []
            for i in image:
                if i is None:
                    self._shapes.append(None)
                elif size is not None or not isinstance(i, SurfaceRenderer):
                    renderer = SurfaceRenderer(i, size)
                    renderer.set_color_key()
                    self._shapes.append(renderer)
                else:
                    self._shapes.append(i)
        else:
            self._shapes = [SurfaceRenderer(image, size)]
        self._center = center

    @property
    def num_images(self) -> int:
        return len(self._shapes)

    def draw(self, dest: Surface, pos: Vec2, index: int = 0):
        self._shapes[index].draw(dest, pos - self._center)


shape_like = Shape | shape_images_like
