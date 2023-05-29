from enum import Enum
from typing import TypedDict, List


class TriggerType(str, Enum):
    generate = "generate"
    upscale = "upscale"
    variation = "variation"
    max_upscale = "max_upscale"
    reset = "reset"
    describe = "describe"


class AttachmentDict(TypedDict):
    id: int
    url: str
    proxy_url: str
    filename: str
    content_type: str
    width: int
    height: int
    size: int
    ephemeral: bool


class CallbackDict(TypedDict):
    type: str
    id: int
    content: str
    attachments: List[AttachmentDict]
    
    trigger_id: str
