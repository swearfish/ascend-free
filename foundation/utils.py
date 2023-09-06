import os
from typing import AnyStr


def dump_file(content: AnyStr, file_name: str | os.PathLike[str]):
    with open(file_name, "wb") as f:
        f.write(content)


def read_lines(file_name: str |os.PathLike[str]) -> list[str]:
    with open(file_name, "rt") as f:
        return [x.rstrip('\n') for x in f.readlines()]
