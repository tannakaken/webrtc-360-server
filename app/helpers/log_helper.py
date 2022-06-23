"""
Just simple log wrapper like kotlin
"""
import logging
import sys
import datetime
import time
from functools import wraps
from typing import Callable, Tuple

from anyio import Any

from app.config import get_settings
from app.helpers.wrap_helper import either_sync_async

settings = get_settings()

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)
if settings.debug_mode:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)


def now_iso_format() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def d(tag: str, message: str) -> None:
    logger.debug(f"[{now_iso_format()}][{tag}][DEBUG]: {message}")


def i(tag: str, message: str) -> None:
    logger.info(f"[{now_iso_format()}][{tag}][INFO]: {message}")


def w(tag: str, message: str) -> None:
    logger.warning(f"[{now_iso_format()}][{tag}][WARNING]: {message}")


def e(tag: str, message: str) -> None:
    logger.error(f"[{now_iso_format()}][{tag}][ERROR]: {message}")


def c(tag: str, message: str) -> None:
    logger.critical(f"[{now_iso_format()}][{tag}][CRITICAL]: {message}")


TFunc = Callable[..., Any]  # 関数


@either_sync_async
def debug_log(router: TFunc) -> TFunc:
    if settings.debug_mode:

        @wraps(router)
        def _inner(*args: Tuple, **kwargs: dict) -> Any:
            start = time.perf_counter()
            result = router(*args, **kwargs)
            d(router.__name__, f"elapsed: {time.perf_counter() - start} s")
            return result

        return _inner
    else:
        return router
