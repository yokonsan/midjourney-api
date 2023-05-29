import asyncio
from typing import Callable, Coroutine, Any, Union

from aiohttp import ClientError, ClientSession

from src.ds.generic import T
from src.ds.system import FetchMethod
from src.lib.exceptions import MaxRetryError
from src.lib.log import logger


class MaxRetry:
    """重试装饰器"""
    
    def __init__(self, max_retry: int = 0):
        self.max_retry = max_retry
    
    def __call__(self, connect_once: Callable[..., Coroutine[Any, Any, T]]) -> Callable[..., Coroutine[Any, Any, T]]:
        async def connect_n_times(*args: Any, **kwargs: Any) -> T:
            retry = self.max_retry + 1
            while retry:
                try:
                    return await connect_once(*args, **kwargs)
                except ClientError as e:
                    await asyncio.sleep(0.5)
                    logger.warning(f"请求失败（{e.__class__.__name__}），正在重试，剩余 {retry - 1} 次")
                except asyncio.TimeoutError:
                    logger.warning(f"请求超时，正在重试，剩余 {retry - 1} 次")
                finally:
                    retry -= 1
            raise MaxRetryError("超出最大重试次数")
        
        return connect_n_times


@MaxRetry()
async def fetch(
    session: ClientSession,
    url: str,
    method: str = FetchMethod.post, **kwargs
) -> Union[bool, None]:
    """
    todo: fetch不仅用于discord，还用于callback，所以MaxRetry有可能导致 n * n 次重复
    
    """
    logger.debug(f"Fetch: {url}")
    async with session.request(method, url, **kwargs) as resp:
        if not resp.ok:
            return None
        return True
