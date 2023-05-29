from typing import Dict

TEMP_MAP: Dict[str, bool] = {}  # 临时存储消息流转信息


def get_temp(trigger_id: str):
    return TEMP_MAP.get(trigger_id)


def set_temp(trigger_id: str):
    TEMP_MAP[trigger_id] = True


def pop_temp(trigger_id: str):
    try:
        TEMP_MAP.pop(trigger_id)
    except KeyError:
        pass
