import json
import time

import aiohttp
from loguru import logger

import settings
from src.lib.api import CALLBACK_URL
from src.util.fetch import fetch


async def callback(data):
    if settings.DUMP_CALLBACK_DATA:
        with open(settings.DATA_DIR / f"callback-{time.time()}.json", "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    logger.debug(f"callback data: {data}")
    if not CALLBACK_URL:
        return
    
    headers = {"Content-Type": "application/json"}
    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=30),
        headers=headers
    ) as session:
        await fetch(session, CALLBACK_URL, json=data)
