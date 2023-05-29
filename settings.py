import os
import pathlib
from os import getenv

from dotenv import load_dotenv

from src.lib.exceptions import MissRequiredVariable
from src.lib.path import ensure_exist

load_dotenv()

GUILD_ID = getenv("GUILD_ID")
CHANNEL_ID = getenv("CHANNEL_ID")
USER_TOKEN = getenv("USER_TOKEN")
CALLBACK_URL = getenv("CALLBACK_URL")

if not all([GUILD_ID, CHANNEL_ID, USER_TOKEN]):
    raise MissRequiredVariable("Missing required environment variable: [GUILD_ID, CHANNEL_ID, USER_TOKEN]")

SETTINGS_PATH = pathlib.Path(__file__)
PROJECT_DIR = SETTINGS_PATH.parent
DATA_DIR = ensure_exist(PROJECT_DIR / "data")
BANNED_PROMPTS_FILE_PATH = PROJECT_DIR / "banned_words.txt"

DUMP_CALLBACK_DATA = True

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise MissRequiredVariable("Missing required environment variable: [BOT_TOKEN]")
TRIGGER_URL = "https://discord.com/api/v9/interactions"
UPLOAD_URL = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/attachments"
PROMPT_PREFIX = "<#"
PROMPT_SUFFIX = "#>"
TRIGGER_ID_PATTERN = f"{PROMPT_PREFIX}(\w+?){PROMPT_SUFFIX}"  # 消息 ID 正则
