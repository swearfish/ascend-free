import math
from copy import copy
from typing import Optional, Sequence


class Vector(Sequence):
    def __init__(self, derived_type, value: list = None, dim: Optional[int] = None):
        self._derived_type = derived_type
        if dim is not None:
            assert value is None, 'Either provide dim or value, not both'
            self._value = [0 for _ in range(dim)]
        elif value is not None:
            self._value = value
        else:
            assert value is None, 'Either provide dim or value, not both'

    def __getitem__(self, i):
        return self._value[i]

    def __len__(self):
        return len(self._value)

    @property
    def length(self):
        result = 0
        for x in self._value:
            result += x*x
        return math.sqrt(result)

    def dup(self):
        return copy(self)

    def __eq__(self, other):
        if not isinstance(other, Vector):
            return False
        return self._value == other._value

    def __add__(self, other):
        assert isinstance(other, Vector) and len(other) == len(self)
        return self._derived_type(*[self._value[i] + other._value[i] for i in range(len(self))])

    def __sub__(self, other):
        assert isinstance(other, Vector) and len(other) == len(self)
        return self._derived_type(*[self._value[i] - other._value[i] for i in range(len(self))])

    def __mul__(self, other):
        assert isinstance(other, (int, float))
        return self._derived_type(*[x * other for x in self._value])

    def __truediv__(self, other):
        assert isinstance(other, (int, float))
        return self._derived_type(*[x / other for x in self._value])

    def as_tuple(self):
        return tuple(self._value)

    def __str__(self):
        coordinates = ', '.join([str(x) for x in self._value])
        return f'({coordinates})'

    def __repr__(self):
        return self.__str__()

