class APPBaseException(Exception):
    message: str

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class MissRequiredVariable(APPBaseException):
    """缺少必需变量"""


class MaxRetryError(APPBaseException):
    """请求最大重试错误"""


class RequestParamsError(APPBaseException):
    """请求参数异常"""


class BannedPromptError(APPBaseException):
    """提示词被禁用"""
