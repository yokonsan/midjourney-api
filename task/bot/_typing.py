from typing import TypedDict, List, Union


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


class EmbedsImage(TypedDict):
    url: str
    proxy_url: str


class Embed(TypedDict):
    type: str
    description: str
    image: EmbedsImage


class Action(TypedDict):
    label: str
    custom_id: str


class CallbackData(TypedDict):
    type: str
    id: int
    content: str
    attachments: List[Attachment]
    embeds: List[Embed]
    actions: List[Action]
    trigger_id: str
