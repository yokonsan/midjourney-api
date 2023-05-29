from enum import Enum

from aiohttp import hdrs
from pydantic import BaseModel


class TriggerStatus(Enum):
    start = "start"  # 首次触发
    generating = "generating"  # 生成中
    end = "end"  # 生成结束
    error = "error"  # 生成错误
    banned = "banned"  # 提示词被禁
    
    verify = "verify"  # 需人工验证


class FetchMethod:
    get = hdrs.METH_GET
    post = hdrs.METH_POST


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
