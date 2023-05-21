from os import getenv

import __init__  # noqa
from lib.bot import bot

BOT_TOKEN = getenv("BOT_TOKEN")

if __name__ == '__main__':
    bot.run(BOT_TOKEN)
