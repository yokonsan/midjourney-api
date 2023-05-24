import re
from enum import Enum
from typing import Dict, Union

from discord import Intents, Message
from discord.ext import commands
from loguru import logger

from _typing import Attachment, CallbackData
from app.handler import PROMPT_PREFIX, PROMPT_SUFFIX
from lib.api.callback import callback

intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="", intents=intents)

TRIGGER_ID_PATTERN = f"{PROMPT_PREFIX}(\w+?){PROMPT_SUFFIX}"  # 消息 ID 正则


class TriggerStatus(Enum):
    start = "start"  # 首次触发
    generating = "generating"  # 生成中
    end = "end"  # 生成结束
    error = "error"  # 生成错误
    banned = "banned"  # 提示词被禁

    verify = "verify"  # 需人工验证


TEMP_MAP: Dict[str, bool] = {}  # 临时存储消息流转信息


def get_temp(trigger_id: str):
    return TEMP_MAP.get(trigger_id)


def set_temp(trigger_id: str):
    TEMP_MAP[trigger_id] = True


def pop_temp(trigger_id: str):
    try:
        TEMP_MAP.pop(trigger_id)
    except KeyError:
        pass


def match_trigger_id(content: str) -> Union[str, None]:
    match = re.findall(TRIGGER_ID_PATTERN, content)
    return match[0] if match else None


@bot.event
async def on_ready():
    logger.success(f"Logged in as {bot.user} (ID: {bot.user.id})")


@bot.event
async def on_message(message: Message):
    if message.author.id != 936929561302675456:
        return

    logger.debug(f"on_message: {message.content}")
    content = message.content
    trigger_id = match_trigger_id(content)
    if not trigger_id:
        return

    if content.find("Waiting to start") != -1:
        type_ = TriggerStatus.start.value
        set_temp(trigger_id)
    elif content.find("(Stopped)") != -1:
        type_ = TriggerStatus.error.value
        pop_temp(trigger_id)
    else:
        type_ = TriggerStatus.end.value
        pop_temp(trigger_id)

    await callback(CallbackData(
        type=type_,
        id=message.id,
        content=content,
        attachments=[
            Attachment(**attachment.to_dict())
            for attachment in message.attachments
        ],
        trigger_id=trigger_id,
    ))


@bot.event
async def on_message_edit(_: Message, after: Message):
    if after.author.id != 936929561302675456:
        return

    trigger_id = match_trigger_id(after.content)
    if not trigger_id:
        return

    logger.debug(f"on_message_edit: {after.content}")
    if after.webhook_id != "":
        await callback(CallbackData(
            type=TriggerStatus.generating.value,
            id=after.id,
            content=after.content,
            attachments=[
                Attachment(**attachment.to_dict())
                for attachment in after.attachments
            ],
            trigger_id=trigger_id,
        ))


@bot.event
async def on_message_delete(message: Message):
    if message.author.id != 936929561302675456:
        return

    trigger_id = match_trigger_id(message.content)
    if not trigger_id:
        return

    logger.debug(f"on_message_delete: {message.content, TEMP_MAP}")
    if get_temp(trigger_id) is None:
        return

    logger.warning(f"sensitive content: {message.content}")
    await callback(CallbackData(
        type=TriggerStatus.banned.value,
        id=message.id,
        content=message.content,
        attachments=[
            Attachment(**attachment.to_dict())
            for attachment in message.attachments
        ],
        trigger_id=trigger_id,
    ))
