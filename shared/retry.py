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

from shared.config import cargar

_logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


def _politicas() -> dict[str, Any]:
    cfg = cargar().get("reintentos", {})
    return {
        "intentos_max": cfg.get("intentos_max", 3),
        "espera_base": cfg.get("espera_base_segundos", 2),
        "espera_max": cfg.get("espera_max_segundos", 30),
        "multiplicador": cfg.get("multiplicador", 2),
    }


def decorador_reintento(
    intentos_max: int | None = None,
    espera_base: float | None = None,
    espera_max: float | None = None,
    multiplicador: float | None = None,
) -> Callable[[F], F]:
    pol = _politicas()
    return tenacity_retry(
        stop=stop_after_attempt(intentos_max or pol["intentos_max"]),
        wait=wait_exponential(
            multiplier=multiplicador or pol["multiplicador"],
            min=espera_base or pol["espera_base"],
            max=espera_max or pol["espera_max"],
        ),
        before_sleep=before_sleep_log(_logger, logging.WARNING),
        reraise=True,
    )
