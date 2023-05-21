import asyncio
from typing import Callable, Coroutine, Any, TypeVar, Union

import aiohttp
from aiohttp import ClientSession

from exceptions import MaxRetryError

T = TypeVar("T")


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
                except aiohttp.ClientError as e:
                    await asyncio.sleep(0.5)
                    print(f"请求失败（{e.__class__.__name__}），正在重试，剩余 {retry - 1} 次")
                except asyncio.TimeoutError:
                    print(f"请求超时，正在重试，剩余 {retry - 1} 次")
                finally:
                    retry -= 1
            raise MaxRetryError("超出最大重试次数")

        return connect_n_times


@MaxRetry()
async def fetch(session: ClientSession, url: str, **kwargs) -> Union[Any, None]:
    print(f"Fetch json: {url}")
    async with session.post(url, **kwargs) as resp:
        if not resp.ok:
            return None
        return True
