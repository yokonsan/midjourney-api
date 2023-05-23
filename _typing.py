from typing import TypedDict, List


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

    trigger_id: str
