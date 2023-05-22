from enum import Enum
from typing import TypedDict, List

from discord import Intents, Message
from discord.ext import commands
from loguru import logger

from lib.api.callback import callback

intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="", intents=intents)


class TriggerStatus(Enum):
    start = "start"
    generating = "generating"
    end = "end"
    error = "error"


class Attachment(TypedDict):
    id: int
    url: str
    proxy_url: str
    filename: str
    content_type: str
    width: int
    height: int
    size: int
    ephemeral: bool


class CallbackData(TypedDict):
    type: str
    id: int
    content: str
    attachments: List[Attachment]


@bot.event
async def on_ready():
    logger.success(f"Logged in as {bot.user} (ID: {bot.user.id})")


@bot.event
async def on_message(message: Message):
    logger.debug(f"on_message: {message.content}")
    if message.author.id != 936929561302675456:
        return

    content = message.content
    if content.find("Waiting to start") != -1:
        type_ = TriggerStatus.start.value
    elif content.find("(Stopped)") != -1:
        type_ = TriggerStatus.error.value
    else:
        type_ = TriggerStatus.end.value

    await callback(CallbackData(
        type=type_,
        id=message.id,
        content=content,
        attachments=[
            Attachment(**attachment.to_dict())
            for attachment in message.attachments
        ],
    ))


@bot.event
async def on_message_edit(_: Message, after: Message):
    logger.debug(f"on_message_edit: {after.content}")
    if after.author.id != 936929561302675456:
        return

    if after.webhook_id != "":
        await callback(CallbackData(
            type=TriggerStatus.generating.value,
            id=after.id,
            content=after.content,
            attachments=[
                Attachment(**attachment.to_dict())
                for attachment in after.attachments
            ],
        ))
