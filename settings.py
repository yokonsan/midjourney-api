import os
import pathlib

from dotenv import load_dotenv

from src.exceptions import MissRequiredVariable
from src.util.path import ensure_exist

load_dotenv()

SETTINGS_PATH = pathlib.Path(__file__)
PROJECT_DIR = SETTINGS_PATH.parent
DATA_DIR = ensure_exist(PROJECT_DIR / "data")

DUMP_CALLBACK_DATA = True

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise MissRequiredVariable("Missing required environment variable: [BOT_TOKEN]")
