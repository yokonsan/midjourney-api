from typing import Optional

from pydantic import BaseModel


class TriggerImagineIn(BaseModel):
    prompt: str
    picurl: Optional[str]


class TriggerUVIn(BaseModel):
    index: int
    msg_id: str
    msg_hash: str

    trigger_id: str  # 供业务定位触发ID，/trigger/imagine 接口返回的 trigger_id


class TriggerResetIn(BaseModel):
    msg_id: str
    msg_hash: str

    trigger_id: str  # 供业务定位触发ID，/trigger/imagine 接口返回的 trigger_id


class TriggerDescribeIn(BaseModel):
    upload_filename: str
    trigger_id: str


class QueueReleaseIn(BaseModel):
    trigger_id: str


class TriggerResponse(BaseModel):
    message: str = "success"
    trigger_id: str
    trigger_type: str = ""


class UploadResponse(BaseModel):
    message: str = "success"
    upload_filename: str = ""
    upload_url: str = ""
    trigger_id: str


class SendMessageIn(BaseModel):
    upload_filename: str


class SendMessageResponse(BaseModel):
    message: str = "success"
    picurl: str
