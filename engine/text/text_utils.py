from typing import Optional


def _scale(value, size: Optional[float]) -> int:
    return int(value * size) if size is not None else value


def _scale_tuple(values: tuple, size: Optional[float]) -> list[int]:
    result = []
    for value in values:
        result.append(_scale(value, size))
    return result
