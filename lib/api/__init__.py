from os import getenv

from exceptions import MissRequiredVariable

GUILD_ID = getenv("GUILD_ID")
CHANNEL_ID = getenv("CHANNEL_ID")
USER_TOKEN = getenv("USER_TOKEN")
CALLBACK_URL = getenv("CALLBACK_URL")

assert all([GUILD_ID, CHANNEL_ID, USER_TOKEN, CALLBACK_URL]), \
    MissRequiredVariable("Missing required environment variable")
