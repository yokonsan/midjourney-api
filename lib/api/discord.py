import json
from enum import Enum
from typing import Dict, Any

import aiohttp

from lib.api import CHANNEL_ID, USER_TOKEN, GUILD_ID
from util.fetch import fetch

TRIGGER_URL = "https://discord.com/api/v9/interactions"
UPLOAD_URL = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/attachments"


class TriggerType(str, Enum):
    generate = "generate"
    upscale = "upscale"
    variation = "variation"
    max_upscale = "max_upscale"
    reset = "reset"
    describe = "describe"


async def trigger(payload: Dict[str, Any]):
    headers = {
        "Content-Type": "application/json",
        "Authorization": USER_TOKEN
    }
    async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers=headers
    ) as session:
        return await fetch(session, TRIGGER_URL, data=json.dumps(payload))


async def upload():
    pass


def _trigger_payload(type_: int, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
    payload = {
        "type": type_,
        "application_id": "936929561302675456",
        "guild_id": GUILD_ID,
        "channel_id": CHANNEL_ID,
        "session_id": "cb06f61453064c0983f2adae2a88c223",
        "data": data
    }
    payload.update(kwargs)
    return payload


async def generate(prompt: str, **kwargs):
    payload = _trigger_payload(2, {
        "version": "1077969938624553050",
        "id": "938956540159881230",
        "name": "imagine",
        "type": 1,
        "options": [{
            "type": 3,
            "name": "prompt",
            "value": prompt
        }],
        "application_command": {
            "id": "938956540159881230",
            "application_id": "936929561302675456",
            "version":  "1077969938624553050",
            "default_permission": True,
            "default_member_permissions": None,
            "type": 1,
            "nsfw": False,
            "name": "imagine",
            "description": "Create images with Midjourney",
            "dm_permission": True,
            "options": [{
                "type": 3,
                "name": "prompt",
                "description": "The prompt to imagine",
                "required": True
            }]
        },
        "attachments": []
    })
    return await trigger(payload)


async def upscale(index: int, msg_id: str, msg_hash: str, **kwargs):
    kwargs = {
        "message_flags": 0,
        "message_id": msg_id,
    }
    payload = _trigger_payload(3, {
        "component_type": 2,
        "custom_id": f"MJ::JOB::upsample::{index}::{msg_hash}"
    }, **kwargs)
    return await trigger(payload)


async def variation(index: int, msg_id: str, msg_hash: str, **kwargs):
    kwargs = {
        "message_flags": 0,
        "message_id": msg_id,
    }
    payload = _trigger_payload(3, {
        "component_type": 2,
        "custom_id": f"MJ::JOB::variation::{index}::{msg_hash}"
    }, **kwargs)
    return await trigger(payload)


async def max_upscale(msg_id: str, msg_hash: str, **kwargs):
    kwargs = {
        "message_flags": 0,
        "message_id": msg_id,
    }
    payload = _trigger_payload(3, {
        "component_type": 2,
        "custom_id": f"MJ::JOB::variation::1::{msg_hash}::SOLO"
    }, **kwargs)
    return await trigger(payload)


async def reset(msg_id: str, msg_hash: str, **kwargs):
    kwargs = {
        "message_flags": 0,
        "message_id": msg_id,
    }
    payload = _trigger_payload(3, {
        "component_type": 2,
        "custom_id": f"MJ::JOB::reroll::0::{msg_hash}::SOLO"
    }, **kwargs)
    return await trigger(payload)


async def describe(upload_filename: str, **kwargs):
    payload = _trigger_payload(2, {
        "version": "1092492867185950853",
        "id": "1092492867185950852",
        "name": "describe",
        "type": 1,
        "options": [{
            "type": 11,
            "name": "prompt",
            "value": 0
        }],
        "application_command": {
            "id": "1092492867185950852",
            "application_id": "936929561302675456",
            "version": "1092492867185950853",
            "default_permission": True,
            "default_member_permissions": None,
            "type": 1,
            "nsfw": False,
            "name": "describe",
            "description": "Writes a prompt based on your image.",
            "dm_permission": True,
            "options": [{
                "type": 11,
                "name": "prompt",
                "description": "The image to describe",
                "required": True
            }]
        },
        "attachments": [{
            "id": "0",
            "filename": "",
            "uploaded_filename": upload_filename,
        }]
    })
    return await trigger(payload)
