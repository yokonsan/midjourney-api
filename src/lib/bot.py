import re
from typing import Union

from settings import TRIGGER_ID_PATTERN


def match_trigger_id(content: str) -> Union[str, None]:
    match = re.findall(TRIGGER_ID_PATTERN, content)
    return match[0] if match else None
