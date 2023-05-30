import asyncio
from collections import deque
from os import getenv
from typing import ParamSpec, Callable, Any, Tuple, Dict, List, Deque

from loguru import logger

from exceptions import QueueFullError

P = ParamSpec("P")


class Task:
    def __init__(
        self, func: Callable[P, Any], *args: P.args, **kwargs: P.kwargs
    ) -> None:
        self.func = func
        self.args = args
        self.kwargs = kwargs

    async def __call__(self) -> None:
        await self.func(*self.args, **self.kwargs)

    def __repr__(self) -> str:
        return f"{self.func.__name__}({self.args}, {self.kwargs})"


class TaskQueue:
    def __init__(self, concur_size: int, wait_size: int) -> None:
        self._concur_size = concur_size
        self._wait_size = wait_size
        self._wait_queue: Deque[Dict[Tuple[str, str], Task]] = deque()
        self._concur_queue: List[Tuple[str, str]] = []

    def put(
            self,
            _trigger_id: str,
            trigger_type: str,
            func: Callable[P, Any],
            *args: P.args,
            **kwargs: P.kwargs
    ) -> None:
        if len(self._wait_queue) >= self._wait_size:
            raise QueueFullError(f"Task queue is full: {self._wait_size}")

        self._wait_queue.append({
            (_trigger_id, trigger_type): Task(func, *args, **kwargs)
        })
        while self._wait_queue and len(self._concur_queue) < self._concur_size:
            self._exec()

    def pop(self, _trigger_id: str, trigger_type: str, ) -> None:
        self._concur_queue.remove((_trigger_id, trigger_type))
        if self._wait_queue:
            self._exec()

    def _exec(self):
        key, task = self._wait_queue.popleft().popitem()

        logger.debug(f"Task[{key}] start execution: {task}")
        loop = asyncio.get_running_loop()
        tsk = loop.create_task(task())
        tsk.add_done_callback(
            lambda t: print(t.result())
        )  # todo

        self._concur_queue.append(key)

    def concur_size(self):
        return self._concur_size

    def wait_size(self):
        return self._wait_size

    def clear_wait(self):
        self._wait_queue.clear()

    def clear_concur(self):
        self._concur_queue.clear()


taskqueue = TaskQueue(
    int(getenv("CONCUR_SIZE") or 2),
    int(getenv("WAIT_SIZE") or 3),
)
