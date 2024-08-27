from os import getenv

from exceptions import MissRequiredVariableError

GUILD_ID = getenv("GUILD_ID")
CHANNEL_ID = getenv("CHANNEL_ID")
USER_TOKEN = getenv("USER_TOKEN")
CALLBACK_URL = getenv("CALLBACK_URL")
PROXY_URL = getenv("PROXY_URL")

DRAW_VERSION = getenv("DRAW_VERSION")

if not all([GUILD_ID, CHANNEL_ID, USER_TOKEN, DRAW_VERSION]):
    raise MissRequiredVariableError(
        "Missing required environment variable: [GUILD_ID, CHANNEL_ID, USER_TOKEN, DRAW_VERSION]")
