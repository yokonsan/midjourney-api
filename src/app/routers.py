from fastapi import APIRouter

from src.lib.api import discord
from .handler import prompt_handler, http_response
from .schema import TriggerImagineIn, TriggerUVIn, TriggerResetIn

router = APIRouter()


@router.post("/trigger/imagine", )
@http_response
async def imagine(body: TriggerImagineIn):
    trigger_id, prompt = prompt_handler(body.prompt)
    return trigger_id, await discord.generate(prompt)


@router.post("/trigger/upscale", )
@http_response
async def upscale(body: TriggerUVIn):
    return body.trigger_id, await discord.upscale(**body.dict())


@router.post("/trigger/variation", )
@http_response
async def variation(body: TriggerUVIn):
    return body.trigger_id, await discord.variation(**body.dict())


@router.post("/trigger/reset", )
@http_response
async def reset(body: TriggerResetIn):
    return body.trigger_id, await discord.reset(**body.dict())


@router.post("/trigger/describe")
@http_response
async def describe():
    pass


@router.post("/trigger/upload")
@http_response
async def upload():
    pass
