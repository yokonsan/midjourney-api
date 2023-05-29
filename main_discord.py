from discord import Intents, Message
from discord.ext import commands

import settings_discord
from src.ds.discord import AttachmentDict, CallbackDict
from src.ds.system import TriggerStatus
from src.lib.callback import callback
from src.lib.log import logger
from src.lib.store import get_temp, set_temp, pop_temp
from src.lib.utils import match_trigger_id

intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="", intents=intents)


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
    
    await callback(CallbackDict(
        type=type_,
        id=message.id,
        content=content,
        attachments=[
            AttachmentDict(**attachment.to_dict())
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
        await callback(CallbackDict(
            type=TriggerStatus.generating.value,
            id=after.id,
            content=after.content,
            attachments=[
                AttachmentDict(**attachment.to_dict())
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
    
    logger.debug(f"on_message_delete: {message.content}")
    if get_temp(trigger_id) is None:
        return
    
    logger.warning(f"sensitive content: {message.content}")
    await callback(CallbackDict(
        type=TriggerStatus.banned.value,
        id=message.id,
        content=message.content,
        attachments=[
            AttachmentDict(**attachment.to_dict())
            for attachment in message.attachments
        ],
        trigger_id=trigger_id,
    ))


if __name__ == '__main__':
    bot.run(settings_discord.BOT_TOKEN)
