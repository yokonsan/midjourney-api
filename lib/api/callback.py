import aiohttp

from lib.api import CALLBACK_URL
from util.fetch import fetch


async def callback(data):
    print(data)
    headers = {"Content-Type": "application/json"}
    async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers=headers
    ) as session:
        return await fetch(session, CALLBACK_URL, json=data)
