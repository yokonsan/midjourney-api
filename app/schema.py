from pydantic import BaseModel

from lib.api.discord import TriggerType


class TriggerBotIn(BaseModel):
    type: TriggerType
    prompt: str = ""
    msg_id: str = ""
    msg_hash: str = ""
    index: int = 0
