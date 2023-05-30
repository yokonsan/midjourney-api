from os import getenv

import aiohttp
from loguru import logger

from lib.api import CALLBACK_URL
from util.fetch import fetch


async def callback(data):
    logger.debug(f"callback data: {data}")
    if not CALLBACK_URL:
        return

    headers = {"Content-Type": "application/json"}
    async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers=headers
    ) as session:
        await fetch(session, CALLBACK_URL, json=data)


QUEUE_RELEASE_API = getenv("QUEUE_RELEASE_API") \
                    or "http://127.0.0.1:8062/v1/api/trigger/queue/release"


async def queue_release(trigger_id: str):
    logger.debug(f"queue_release: {trigger_id}")

    headers = {"Content-Type": "application/json"}
    data = {"trigger_id": trigger_id}
    async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers=headers
    ) as session:
        await fetch(session, QUEUE_RELEASE_API, json=data)
