import asyncio
import re
from typing import Dict, Union, Any

from discord import Message

from app.handler import PROMPT_PREFIX, PROMPT_SUFFIX
from lib.api.callback import queue_release, callback
from task.bot._typing import CallbackData, Attachment, Embed

TRIGGER_ID_PATTERN = f"{PROMPT_PREFIX}(\w+?){PROMPT_SUFFIX}"  # 消息 ID 正则

TEMP_MAP: Dict[str, bool] = {}  # 临时存储消息流转信息


def get_temp(trigger_id: str):
    return TEMP_MAP.get(trigger_id)


def set_temp(trigger_id: str):
    TEMP_MAP[trigger_id] = True


def pop_temp(trigger_id: str):
    asyncio.get_event_loop().create_task(queue_release(trigger_id))
    try:
        TEMP_MAP.pop(trigger_id)
    except KeyError:
        pass


def match_trigger_id(content: str) -> Union[str, None]:
    match = re.findall(TRIGGER_ID_PATTERN, content)
    return match[0] if match else None


async def callback_trigger(trigger_id: str, trigger_status: str, message: Message):
    await callback(CallbackData(
        type=trigger_status,
        id=message.id,
        content=message.content,
        attachments=[
            Attachment(**attachment.to_dict())
            for attachment in message.attachments
        ],
        embeds=[],
        trigger_id=trigger_id,
    ))


async def callback_describe(trigger_status: str, message: Message, embed: Dict[str, Any]):
    url = embed.get("image", {}).get("url")
    trigger_id = url.split("/")[-1].split(".")[0]

    await callback(CallbackData(
        type=trigger_status,
        id=message.id,
        content=message.content,
        attachments=[],
        embeds=[
            Embed(**embed)
        ],
        trigger_id=trigger_id,
    ))
    return trigger_id
