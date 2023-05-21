from enum import Enum
from typing import Union


class ErrorCode(Enum):
    # 发生错误
    MISS_REQUIRED_VARIABLE_ERROR = 11
    WRONG_ARGUMENT_ERROR = 12
    MAX_RETRY_ERROR = 13
    NO_TOKEN_ERROR = 14
    REQUEST_PARAMS_ERROR = 15


class SuccessCode(Enum):
    SUCCESS = 0


ReturnCode = Union[ErrorCode, SuccessCode]


class BaseException(Exception):
    code: ErrorCode
    message: str

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class MissRequiredVariable(BaseException):
    code: ErrorCode.MISS_REQUIRED_VARIABLE_ERROR


class MaxRetryError(BaseException):
    code = ErrorCode.MAX_RETRY_ERROR


class RequestParamsError(BaseException):
    code = ErrorCode.REQUEST_PARAMS_ERROR
