from fastapi import APIRouter, UploadFile

from lib.api import discord
from lib.api.discord import TriggerType
from util._queue import taskqueue
from .handler import prompt_handler, unique_id
from .schema import (
    TriggerImagineIn,
    TriggerUVIn,
    TriggerResetIn,
    QueueReleaseIn,
    TriggerResponse,
    UploadResponse,
    TriggerDescribeIn,
    SendMessageResponse,
    SendMessageIn,
)

router = APIRouter()


@router.post("/imagine", response_model=TriggerResponse)
async def imagine(body: TriggerImagineIn):
    trigger_id, prompt = prompt_handler(body.prompt, body.picurl)
    trigger_type = TriggerType.generate.value

    taskqueue.put(trigger_id, discord.generate, prompt)
    return {"trigger_id": trigger_id, "trigger_type": trigger_type}


@router.post("/upscale", response_model=TriggerResponse)
async def upscale(body: TriggerUVIn):
    trigger_id = body.trigger_id
    trigger_type = TriggerType.upscale.value

    taskqueue.put(trigger_id, discord.upscale, **body.dict())
    return {"trigger_id": trigger_id, "trigger_type": trigger_type}


@router.post("/variation", response_model=TriggerResponse)
async def variation(body: TriggerUVIn):
    trigger_id = body.trigger_id
    trigger_type = TriggerType.variation.value

    taskqueue.put(trigger_id, discord.variation, **body.dict())
    return {"trigger_id": trigger_id, "trigger_type": trigger_type}


@router.post("/reset", response_model=TriggerResponse)
async def reset(body: TriggerResetIn):
    trigger_id = body.trigger_id
    trigger_type = TriggerType.reset.value

    taskqueue.put(trigger_id, discord.reset, **body.dict())
    return {"trigger_id": trigger_id, "trigger_type": trigger_type}


@router.post("/describe", response_model=TriggerResponse)
async def describe(body: TriggerDescribeIn):
    trigger_id = body.trigger_id
    trigger_type = TriggerType.describe.value

    taskqueue.put(trigger_id, discord.describe, **body.dict())
    return {"trigger_id": trigger_id, "trigger_type": trigger_type}


@router.post("/upload", response_model=UploadResponse)
async def upload_attachment(file: UploadFile):
    if not file.content_type.startswith("image/"):
        return {"message": "must image"}

    trigger_id = str(unique_id())
    filename = f"{trigger_id}.jpg"
    file_size = file.size
    attachment = await discord.upload_attachment(filename, file_size, await file.read())
    if not (attachment and attachment.get("upload_url")):
        return {"message": "Failed to upload image"}

    return {
        "upload_filename": attachment.get("upload_filename"),
        "upload_url": attachment.get("upload_url"),
        "trigger_id": trigger_id,
    }


@router.post("/message", response_model=SendMessageResponse)
async def send_message(body: SendMessageIn):
    picurl = await discord.send_attachment_message(body.upload_filename)
    if not picurl:
        return {"message": "Failed to send message"}

    return {"picurl": picurl}


@router.post("/queue/release", response_model=TriggerResponse)
async def queue_release(body: QueueReleaseIn):
    """bot 清除队列任务"""
    taskqueue.pop(body.trigger_id)

    return body
