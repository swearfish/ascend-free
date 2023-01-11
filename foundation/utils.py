import os
from typing import AnyStr


def dump_file(content: AnyStr, file_name: str | os.PathLike[str]):
    with open(file_name, "wb") as f:
        f.write(content)
