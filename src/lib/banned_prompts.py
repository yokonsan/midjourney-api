import asyncio

import aiofiles

import settings


async def loads_banned_words():
    prompt = set()
    async with aiofiles.open(settings.BANNED_PROMPTS_FILE_PATH, "r") as r:
        for line in await r.readlines():
            prompt.add(line.strip())
    
    return prompt


BANNED_PROMPTS = asyncio.run(loads_banned_words())
