import hashlib
import re
import time
from typing import Union

from settings_server import TRIGGER_ID_PATTERN


def match_trigger_id(content: str) -> Union[str, None]:
    match = re.findall(TRIGGER_ID_PATTERN, content)
    return match[0] if match else None


def unique_id():
    """生成唯一的 10 位数字，作为任务 ID"""
    return int(hashlib.sha256(str(time.time()).encode("utf-8")).hexdigest(), 16) % 10 ** 10
