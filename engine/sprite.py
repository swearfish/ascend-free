from pygame.surface import Surface

from engine.shape import Shape, surface_like, shape_like
from foundation.vector_2d import Vec2


class Sprite:
    def __init__(self, image: shape_like, pos=Vec2(0, 0), center=Vec2(0, 0), size: Vec2 = None):
        if isinstance(image, Shape):
            assert size is None, f"Can't resize sprite template"
            self._template = image
            self._center = center
        else:
            self._template = Shape(image, center, size)
            self._center = Vec2(0, 0)
        self._pos = Vec2(0, 0)
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

    def animate(self, start: int, end: int, loop=False, speed=1.0, destroy_on_end=False):
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

    def add(self, sprite: Sprite | Shape | surface_like) -> Sprite:
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
