import os
import pathlib


def ensure_exist(dir: pathlib.Path):
    if not dir.exists():
        os.mkdir(dir)
    return dir
