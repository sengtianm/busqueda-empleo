import logging
from collections.abc import Callable
from typing import Any, TypeVar

from tenacity import (
    before_sleep_log,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)
from tenacity import (
    retry as tenacity_retry,
)

from shared.config import load

_logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable[..., Any])

# Codes that may be retried (DOC-06, Section 11 / RN-03-RN-06 of the technical
# sheet). Includes network-level unavailability and timeouts; excludes codes
# that compromise the source (Grupo A, e.g. bloqueo_plataforma) and those that
# would not change on retry (e.g. autenticacion_rechazada).
_CODIGOS_REINTENTABLES = (
    "fuente_inalcanzable",
    "timeout_ingreso",
    "timeout_consulta",
    "timeout_captura",
)


def _policies() -> dict[str, Any]:
    cfg = load().get("retries", {})
    return {
        "max_attempts": cfg.get("max_attempts", 3),
        "base_wait": cfg.get("base_wait_seconds", 2),
        "max_wait": cfg.get("max_wait_seconds", 30),
        "multiplier": cfg.get("multiplier", 2),
    }


def retry_decorator(
    max_attempts: int | None = None,
    base_wait: float | None = None,
    max_wait: float | None = None,
    multiplier: float | None = None,
) -> Callable[[F], F]:
    policy = _policies()
    return tenacity_retry(
        stop=stop_after_attempt(max_attempts or policy["max_attempts"]),
        wait=wait_exponential(
            multiplier=multiplier or policy["multiplier"],
            min=base_wait or policy["base_wait"],
            max=max_wait or policy["max_wait"],
        ),
        before_sleep=before_sleep_log(_logger, logging.WARNING),
        reraise=True,
    )


def should_retry(codigo_motivo: str) -> bool:
    return codigo_motivo in _CODIGOS_REINTENTABLES


def retry_conditional(
    max_reintentos: int = 2,
    backoff_inicial: float = 1.0,
) -> Callable[[F], F]:
    def _si_reintentar(exception: BaseException) -> bool:
        codigo = getattr(exception, "codigo_motivo", None)
        if isinstance(codigo, str):
            return should_retry(codigo)
        codigo_business = getattr(exception, "code", None)
        if isinstance(codigo_business, str):
            return should_retry(codigo_business)
        return False

    policy = _policies()
    return tenacity_retry(
        stop=stop_after_attempt(max_reintentos + 1),
        wait=wait_exponential(
            multiplier=policy["multiplier"],
            min=backoff_inicial,
            max=max(backoff_inicial * 8, backoff_inicial),
        ),
        retry=retry_if_exception(_si_reintentar),
        before_sleep=before_sleep_log(_logger, logging.WARNING),
        reraise=True,
    )
