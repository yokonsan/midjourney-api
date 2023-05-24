import asyncio

import aiofiles


async def loads_banned_words():
    prompt = set()
    filename = "banned_words.txt"
    async with aiofiles.open(filename, "r") as r:
        for line in await r.readlines():
            prompt.add(line.strip())

    return prompt

BANNED_PROMPT = asyncio.run(loads_banned_words())
