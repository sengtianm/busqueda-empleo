import logging
from collections.abc import Callable
from typing import Any, TypeVar

from tenacity import (
    before_sleep_log,
    stop_after_attempt,
    wait_exponential,
)
from tenacity import (
    retry as tenacity_retry,
)

from shared.config import load

_logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


def _policies() -> dict[str, Any]:
    cfg = load().get("retries", {})
    return {
        "max_attempts": cfg.get("max_attempts", 3),
        "base_wait": cfg.get("base_wait_seconds", 2),
        "max_wait": cfg.get("max_wait_seconds", 30),
        "multiplier": cfg.get("multiplier", 2),
    }


def decorador_reintento(
    max_attempts: int | None = None,
    base_wait: float | None = None,
    max_wait: float | None = None,
    multiplier: float | None = None,
) -> Callable[[F], F]:
    pol = _policies()
    return tenacity_retry(
        stop=stop_after_attempt(max_attempts or pol["max_attempts"]),
        wait=wait_exponential(
            multiplier=multiplier or pol["multiplier"],
            min=base_wait or pol["base_wait"],
            max=max_wait or pol["max_wait"],
        ),
        before_sleep=before_sleep_log(_logger, logging.WARNING),
        reraise=True,
    )
