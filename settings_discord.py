from os import getenv

from dotenv import load_dotenv

from src.lib.exceptions import MissRequiredVariable

load_dotenv()

GUILD_ID = getenv("GUILD_ID")
CHANNEL_ID = getenv("CHANNEL_ID")
USER_TOKEN = getenv("USER_TOKEN")
BOT_TOKEN = getenv("BOT_TOKEN")

CALLBACK_URL = getenv("CALLBACK_URL")  # todo: enable without it

if not all([GUILD_ID, CHANNEL_ID, USER_TOKEN, BOT_TOKEN]):
    raise MissRequiredVariable("Missing required environment variable: [GUILD_ID, CHANNEL_ID, USER_TOKEN, BOT_TOKEN, CALLBACK_URL]")

DUMP_CALLBACK_DATA = True

TRIGGER_URL = "https://discord.com/api/v9/interactions"
UPLOAD_URL = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/attachments"
