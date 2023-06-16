import json
from enum import Enum
from typing import Dict, Any, Union

import aiohttp

from lib.api import CHANNEL_ID, USER_TOKEN, GUILD_ID
from util.fetch import fetch, fetch_json, FetchMethod

TRIGGER_URL = "https://discord.com/api/v9/interactions"
UPLOAD_ATTACHMENT_URL = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/attachments"
SEND_MESSAGE_URL = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/messages"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": USER_TOKEN
}


class TriggerType(str, Enum):
    generate = "generate"
    upscale = "upscale"
    variation = "variation"
    max_upscale = "max_upscale"
    reset = "reset"
    describe = "describe"


async def trigger(payload: Dict[str, Any]):
    async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers=HEADERS
    ) as session:
        return await fetch(session, TRIGGER_URL, data=json.dumps(payload))


async def upload_attachment(
        filename: str, file_size: int, image: bytes
) -> Union[Dict[str, Union[str, int]], None]:
    payload = {
        "files": [{
            "filename": filename,
            "file_size": file_size,
            "id": "0"
        }]
    }
    async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers=HEADERS
    ) as session:
        response = await fetch_json(session, UPLOAD_ATTACHMENT_URL, data=json.dumps(payload))
        if not response or not response.get("attachments"):
            return None

        attachment = response["attachments"][0]

    response = await put_attachment(attachment.get("upload_url"), image)
    return attachment if response is not None else None


async def put_attachment(url: str, image: bytes):
    headers = {"Content-Type": "image/png"}
    async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers=headers
    ) as session:
        return await fetch(session, url, data=image, method=FetchMethod.put)


async def send_attachment_message(upload_filename: str) -> Union[str, None]:
    payload = {
        "content": "",
        "nonce": "",
        "channel_id": "1105829904790065223",
        "type": 0,
        "sticker_ids": [],
        "attachments": [{
            "id": "0",
            "filename": upload_filename.split("/")[-1],
            "uploaded_filename": upload_filename
        }]
    }
    async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers=HEADERS
    ) as session:
        response = await fetch_json(session, SEND_MESSAGE_URL, data=json.dumps(payload))
        if not response or not response.get("attachments"):
            return None

        attachment = response["attachments"][0]
        return attachment.get("url")


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
        "version": "1118961510123847772",
        "id": "938956540159881230",
        "name": "imagine",
        "type": 1,
        "options": [{
            "type": 3,
            "name": "prompt",
            "value": prompt
        }],
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
        "custom_id": f"MJ::JOB::upsample_max::1::{msg_hash}::SOLO"
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
        "version": "1118961510123847774",
        "id": "1092492867185950852",
        "name": "describe",
        "type": 1,
        "options": [
            {
                "type": 11,
                "name": "image",
                "value": 0
            }
        ],
        "attachments": [{
            "id": "0",
            "filename": upload_filename.split("/")[-1],
            "uploaded_filename": upload_filename,
        }]
    })
    return await trigger(payload)
