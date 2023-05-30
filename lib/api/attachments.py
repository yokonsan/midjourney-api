import aiohttp

from util.fetch import fetch, FetchMethod


async def put_attachment(url: str, image: bytes):
    headers = {"Content-Type": "image/png"}
    async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers=headers
    ) as session:
        return await fetch(session, url, data=image, method=FetchMethod.put)
