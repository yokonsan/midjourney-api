from enum import Enum


class TriggerType(str, Enum):
    generate = "generate"
    upscale = "upscale"
    variation = "variation"
    max_upscale = "max_upscale"
    reset = "reset"
    describe = "describe"
