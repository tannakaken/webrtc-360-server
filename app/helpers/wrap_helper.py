from functools import wraps
import asyncio
from typing import Any, Callable, Tuple

TFunc = Callable[..., Any]  # 関数
TDecorator = Callable[[TFunc], TFunc]  # デコレーター


def either_sync_async(decorator: TDecorator) -> TDecorator:
    """
    デコレーターを同期関数にも非同期関数にも使えるようにする、デコレーターのデコレーター
    """

    @wraps(decorator)
    def _decorator(router: TFunc) -> TFunc:
        if asyncio.iscoroutinefunction(router):

            @decorator
            @wraps(router)
            def _inner(*args: Tuple, **kwargs: dict) -> Any:
                return router(*args, **kwargs)

            @wraps(_inner)
            async def inner(*args: Tuple, **kwargs: dict) -> Any:
                return await _inner(*args, **kwargs)
        else:

            @decorator
            @wraps(router)
            def inner(*args: Tuple, **kwargs: dict) -> Any:
                return router(*args, **kwargs)

        return inner

    return _decorator
