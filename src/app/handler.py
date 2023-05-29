import hashlib
import time
from functools import wraps

from fastapi import status
from fastapi.responses import JSONResponse

from settings import PROMPT_PREFIX, PROMPT_SUFFIX
from src.lib.banned_prompts import BANNED_PROMPTS
from src.lib.exceptions import BannedPromptError


def check_banned(prompt: str):
    words = set(w.lower() for w in prompt.split())
    if len(words & BANNED_PROMPTS) != 0:
        raise BannedPromptError(f"banned prompt: {prompt}")


def unique_id():
    """生成唯一的 10 位数字，作为任务 ID"""
    return int(hashlib.sha256(str(time.time()).encode("utf-8")).hexdigest(), 16) % 10 ** 10


def prompt_handler(prompt: str):
    """
    拼接 Prompt 形如: <#1234567890#>a cute cat
    """
    check_banned(prompt)
    
    trigger_id = str(unique_id())
    return trigger_id, f"{PROMPT_PREFIX}{trigger_id}{PROMPT_SUFFIX}{prompt}"


def http_response(func):
    @wraps(func)
    async def router(*args, **kwargs):
        trigger_id, resp = await func(*args, **kwargs)
        if resp is not None:
            code, trigger_result = status.HTTP_200_OK, "success"
        else:
            code, trigger_result = status.HTTP_400_BAD_REQUEST, "fail"
        
        return JSONResponse(
            status_code=code,
            content={"trigger_id": trigger_id, "trigger_result": trigger_result}
        )
    
    return router
