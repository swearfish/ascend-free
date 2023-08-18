from typing import TypeVar

from pygame.surface import Surface

from engine.shape_renderer import ShapeRenderer
from foundation.vector_2d import Vec2

shape_like = ShapeRenderer | Surface | list[ShapeRenderer | Surface]


class SpriteTemplate:
    def __init__(self, image: shape_like, center=Vec2(0, 0), size: Vec2=None):
        if isinstance(image, ShapeRenderer) and size is None:
            self._shapes = [image]
        elif isinstance(image, list):
            self._shapes = []
            for i in image:
                if size is not None or not isinstance(i, ShapeRenderer):
                    self._shapes.append(ShapeRenderer(i, size))
                else:
                    self._shapes.append(i)
                self._shapes.append(i)
        else:
            self._shapes = [ShapeRenderer(image, size)]
        self._center = center

    @property
    def num_images(self) -> int:
        return len(self._shapes)

    def draw(self, dest: Surface, pos: Vec2, index: int = 0):
        self._shapes[index].draw(dest, pos - self._center)


class Sprite:
    def __init__(self, image: SpriteTemplate | shape_like, pos=Vec2(0, 0), center=Vec2(0, 0), size: Vec2=None):
        if isinstance(image, SpriteTemplate):
            assert size is None, f"Can't resize sprite template"
            self._template = image
            self._center = center
        else:
            self._template = SpriteTemplate(image, center, size)
            self._center = Vec2(0,0)
        self._pos = Vec2(0,0)
        self._state = 0
        self._anim_start: int | None = None
        self._anim_end: int | None = None
        self._anim_loop: bool = False
        self._anim_speed: float = 0.0
        self._anim_state: float = 0.0
        self._destroy_on_end = False
        self.move(pos)

    def stop_animation(self):
        self._anim_start = self._anim_end = None
        self._anim_loop = False
        self._anim_speed = 0.0

    def animate(self, start: int, end: int, loop = False, speed = 1.0, destroy_on_end = False):
        assert start <= end, f'Invalid frame range: {start}-{end}'
        assert 0 < speed, f'Invalid speed: {speed}'
        self._state = start
        self._anim_state = start
        if start == end:
            self.stop_animation()
        else:
            self._anim_start = start
            self._anim_end = end
            self._anim_loop = loop
            self._destroy_on_end = destroy_on_end

    @property
    def state(self) -> int:
        return self._state

    @state.setter
    def state(self, state):
        self._state = state
        self.stop_animation()

    @property
    def animating(self) -> bool:
        return self._anim_start is not None

    @property
    def dead(self) -> bool:
        return self._destroy_on_end and not self.animating

    def update(self, dt: float) -> bool:
        if self._anim_start is None:
            return False
        self._anim_state += dt * self._anim_speed
        if self._anim_end < self._anim_state:
            if not self._anim_loop:
                self.stop_animation()
                return False
            self._anim_state = self._anim_start
        self._state = int(self._anim_state)
        return True

    @property
    def position(self) -> Vec2:
        return self._pos + self._center

    def move(self, pos: Vec2):
        self._pos = pos - self._center

    def move_by(self, delta: Vec2):
        self._pos += delta

    def draw(self, screen: Surface):
        self._template.draw(screen, self._pos, self._state)


class SpriteBatch:
    def __init__(self):
        self.sprites: list[Sprite] = []

    def add(self, sprite: Sprite | SpriteTemplate | shape_like) -> Sprite:
        if isinstance(sprite, Sprite):
            self.sprites.append(sprite)
            return sprite
        else:
            result = Sprite(sprite)
            self.sprites.append(result)
            return result

    def update(self, dt: float):
        has_garbage = False
        for sprite in self.sprites:
            sprite.update(dt)
            has_garbage |= sprite.dead
        if has_garbage:
            self.sprites = list(filter(lambda x: not x.dead, self.sprites))
