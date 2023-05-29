from enum import Enum


class TriggerStatus(Enum):
    start = "start"  # 首次触发
    generating = "generating"  # 生成中
    end = "end"  # 生成结束
    error = "error"  # 生成错误
    banned = "banned"  # 提示词被禁
    
    verify = "verify"  # 需人工验证
