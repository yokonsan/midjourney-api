import aiohttp
from loguru import logger

from lib.api import CALLBACK_URL
from util.fetch import fetch


async def callback(data):
    logger.debug(f"callback data: {data}")
    headers = {"Content-Type": "application/json"}
    async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers=headers
    ) as session:
        return await fetch(session, CALLBACK_URL, json=data)
