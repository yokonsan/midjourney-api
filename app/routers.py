from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from exceptions import MaxRetryError, RequestParamsError
from lib.api import discord
from .schema import TriggerBotIn

router = APIRouter()


@router.post("/trigger/bot")
async def trigger_bot(body: TriggerBotIn):
    try:
        if body.type == discord.TriggerType.generate:
            resp = await discord.generate(body.prompt)
        elif body.type == discord.TriggerType.upscale:
            resp = await discord.upscale(body.index, body.msg_id, body.msg_hash)
        elif body.type == discord.TriggerType.variation:
            resp = await discord.variation(body.index, body.msg_id, body.msg_hash)
        elif body.type == discord.TriggerType.max_upscale:
            resp = await discord.max_upscale(body.msg_id, body.msg_hash)
        elif body.type == discord.TriggerType.reset:
            resp = await discord.reset(body.msg_id, body.msg_hash)
        elif body.type == discord.TriggerType.describe:
            resp = await discord.describe(body.prompt)
        else:
            resp = None

        if resp is not None:
            code, content = status.HTTP_200_OK, "success"
        else:
            code, content = status.HTTP_400_BAD_REQUEST, "fail"
    except MaxRetryError:
        code, content = status.HTTP_400_BAD_REQUEST, "Request discord api error"
    except RequestParamsError:
        code, content = status.HTTP_400_BAD_REQUEST, "Miss required params error"

    return JSONResponse(status_code=code, content=content)


@router.post("/trigger/upload")
async def trigger_upload():
    pass
