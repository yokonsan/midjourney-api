from os import getenv

import __init__  # noqa
from exceptions import MissRequiredVariable
from task.bot import bot

BOT_TOKEN = getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise MissRequiredVariable("Missing required environment variable: [BOT_TOKEN]")


if __name__ == '__main__':
    bot.run(BOT_TOKEN)
