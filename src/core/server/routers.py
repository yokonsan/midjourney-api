from functools import wraps

from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse

from settings_server import PROMPT_PREFIX, PROMPT_SUFFIX
from src.core.discord import bridge
from src.ds.system import TriggerImagineIn, TriggerUVIn, TriggerResetIn
from src.lib.ban import check_banned
from src.lib.utils import unique_id

root_router = APIRouter()


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


@root_router.post("/trigger/imagine", )
@http_response
async def imagine(body: TriggerImagineIn):
    check_banned(body.prompt)
    
    trigger_id = str(unique_id())
    prompt = f"{PROMPT_PREFIX}{trigger_id}{PROMPT_SUFFIX}{body.prompt}"  # 拼接 Prompt 形如: <#1234567890#>a cute cat
    
    return trigger_id, await bridge.imagine(prompt)


@root_router.post("/trigger/upscale", )
@http_response
async def upscale(body: TriggerUVIn):
    return body.trigger_id, await bridge.upscale(**body.dict())


@root_router.post("/trigger/variation", )
@http_response
async def variation(body: TriggerUVIn):
    return body.trigger_id, await bridge.variation(**body.dict())


@root_router.post("/trigger/reset", )
@http_response
async def reset(body: TriggerResetIn):
    return body.trigger_id, await bridge.reset(**body.dict())


@root_router.post("/trigger/describe")
@http_response
async def describe():
    pass


@root_router.post("/trigger/upload")
@http_response
async def upload():
    pass
