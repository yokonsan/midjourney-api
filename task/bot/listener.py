from discord import Intents, Message
from discord.ext import commands
from loguru import logger

from task.bot import TriggerStatus
from task.bot.handler import (
    match_trigger_id,
    set_temp,
    pop_temp,
    get_temp,
    callback_trigger,
    callback_describe
)

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
    logger.debug(f"on_message embeds: {message.embeds[0].to_dict() if message.embeds else message.embeds}")
    content = message.content
    trigger_id = match_trigger_id(content)
    if not trigger_id:
        return

    if content.find("Waiting to start") != -1:
        trigger_status = TriggerStatus.start.value
        set_temp(trigger_id)
    elif content.find("(Stopped)") != -1:
        trigger_status = TriggerStatus.error.value
        pop_temp(trigger_id)
    else:
        trigger_status = TriggerStatus.end.value
        pop_temp(trigger_id)

    await callback_trigger(trigger_id, trigger_status, message)


@bot.event
async def on_message_edit(_: Message, after: Message):
    if after.author.id != 936929561302675456:
        return

    logger.debug(f"on_message_edit: {after.content}")
    if after.embeds:
        embed = after.embeds[0]
        if not (embed.image.width and embed.image.height):
            return

        embed = embed.to_dict()
        logger.debug(f"on_message_edit embeds: {embed}")
        trigger_status = TriggerStatus.text.value
        trigger_id = await callback_describe(trigger_status, after, embed)
        pop_temp(trigger_id)
        return

    trigger_id = match_trigger_id(after.content)
    if not trigger_id:
        return

    if after.webhook_id != "":
        await callback_trigger(trigger_id, TriggerStatus.generating.value, after)


@bot.event
async def on_message_delete(message: Message):
    if message.author.id != 936929561302675456:
        return

    trigger_id = match_trigger_id(message.content)
    if not trigger_id:
        return

    if get_temp(trigger_id) is None:
        return

    logger.debug(f"on_message_delete: {message.content}")
    logger.warning(f"sensitive content: {message.content}")
    trigger_status = TriggerStatus.banned.value
    pop_temp(trigger_id)
    await callback_trigger(trigger_id, trigger_status, message)
