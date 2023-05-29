import json
import time

import aiohttp

import settings_discord
import src.lib.path
from src.ds.discord import CallbackDict
from src.lib.fetch import fetch
from src.lib.log import logger


async def callback(data: CallbackDict):
    if settings_discord.DUMP_CALLBACK_DATA:
        with open(src.lib.path.DATA_DIR / f"callback-{time.time()}.json", "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    logger.debug(f"callback data: {data}")
    if not settings_discord.CALLBACK_URL:
        logger.warning("没有配置 CALLBACK_URL，因此忽略回调数据")
        return
    
    headers = {"Content-Type": "application/json"}
    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=30),
        headers=headers
    ) as session:
        await fetch(session, settings_discord.CALLBACK_URL, json=data)
