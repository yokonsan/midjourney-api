from enum import Enum


class TriggerStatus(Enum):
    start = "start"  # 首次触发 MessageType.chat_input_command
    generating = "generating"  # 生成中
    end = "end"  # 生成结束 MessageType.default
    error = "error"  # 生成错误
    banned = "banned"  # 提示词被禁

    text = "text"  # 文本内容：describe

    verify = "verify"  # 需人工验证
