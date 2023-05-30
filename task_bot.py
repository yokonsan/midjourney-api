from os import getenv

import __init__  # noqa
from exceptions import MissRequiredVariableError
from task.bot.listener import bot

BOT_TOKEN = getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise MissRequiredVariableError("Missing required environment variable: [BOT_TOKEN]")


if __name__ == '__main__':
    bot.run(BOT_TOKEN)
