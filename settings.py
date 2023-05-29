import pathlib

from util.path import ensure_exist

SETTINGS_PATH = pathlib.Path(__file__)
PROJECT_DIR = SETTINGS_PATH.parent
DATA_DIR = ensure_exist(PROJECT_DIR / "data")

DUMP_CALLBACK_DATA = True
