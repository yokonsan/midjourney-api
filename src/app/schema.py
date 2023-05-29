from pydantic import BaseModel


class TriggerImagineIn(BaseModel):
    prompt: str


class TriggerUVIn(BaseModel):
    index: int
    msg_id: str
    msg_hash: str

    trigger_id: str  # 供业务定位触发ID，/trigger/imagine 接口返回的 trigger_id


class TriggerResetIn(BaseModel):
    msg_id: str
    msg_hash: str

    trigger_id: str  # 供业务定位触发ID，/trigger/imagine 接口返回的 trigger_id
