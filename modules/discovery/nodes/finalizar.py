"""Finalizar Proceso node of the Discovery flow (technical sheet, terminal node).

Convergence point of all run terminations. It closes the run deterministically
with best-effort semantics (ficha técnica decisions B): persists the closure
metrics in `corridas` (single retry), writes the termination event, closes the
open Playwright resources, releases the concurrency lock only if this run holds
it, and ends without successors. Failures never abort the closure: each step
logs with Loguru and continues. `should_retry`/`retry_conditional` are not used
here — retries are limited to one manual retry per persistence step.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from loguru import logger

from modules.discovery.run_context import RunContext
from shared.persistence import (
    actualizar_corrida,
    escribir_evento,
    leer_tabla,
    liberar_bloqueo,
)

_FORMATO_TIMESTAMP = "%Y-%m-%d %H:%M:%S"

_ESTADOS_POR_MOTIVO: dict[str, str] = {
    "corrida_completada": "completada",
    "sin_fuentes": "sin_fuentes",
    "error_critico": "abortada",
    "aborto": "abortada",
}

_CAMPOS_METRICAS = (
    "total_ofertas",
    "total_errores",
    "total_sucesos",
    "fuentes_procesadas",
)


@dataclass
class ResultadoFinalizar:
    """Outcome of the Finalizar Proceso node handed to the orchestrator."""

    estado: str
    contexto: RunContext | None = None
    codigo: str = ""
    metricas: dict[str, int] | None = None


def _ahora() -> str:
    return datetime.now().strftime(_FORMATO_TIMESTAMP)


def consultar_metricas(contexto: RunContext | None) -> dict[str, int]:
    """Counts closure metrics from the database; zeros on any failure.

    Metrics: offers registered in this run, error/success events, and the
    number of distinct sources present in the run's events. A failing query
    degrades to zeros (best-effort, ES-4.5 closure must never abort).
    """
    if contexto is None:
        return {campo: 0 for campo in _CAMPOS_METRICAS}
    id_corrida = contexto.id_corrida
    try:
        ofertas = leer_tabla("ofertas", {"id_corrida": id_corrida})
        eventos = leer_tabla("eventos", {"id_corrida": id_corrida})
    except Exception as exc:
        logger.error(
            f"Metricas no consultables | run={id_corrida} | {exc} | "
            "se degrada a ceros"
        )
        return {campo: 0 for campo in _CAMPOS_METRICAS}
    errores = sum(1 for e in eventos if e.get("tipo") == "error")
    sucesos = len(eventos) - errores
    fuentes = len({e.get("fuente_id") for e in eventos if e.get("fuente_id")})
    return {
        "total_ofertas": len(ofertas),
        "total_errores": errores,
        "total_sucesos": sucesos,
        "fuentes_procesadas": fuentes,
    }


def _persistir_cierre_corrida(
    id_corrida: str, estado: str, motivo: str, metricas: dict[str, int]
) -> None:
    """Step 3: update the run row with a single retry; never aborts."""
    campos: dict[str, Any] = {
        "estado": estado,
        "fecha_fin": _ahora(),
        "motivo_terminacion": motivo,
        **metricas,
    }
    for intento in (1, 2):
        try:
            actualizar_corrida(id_corrida, campos)
            return
        except Exception as exc:
            logger.error(
                f"actualizar_corrida fallo (intento {intento}/2) | "
                f"run={id_corrida} | {exc}"
            )
    logger.error(f"Corrida no persistida | run={id_corrida} | estado={estado} | {motivo}")


def _escribir_evento_terminacion(
    id_corrida: str, estado: str, motivo: str, metricas: dict[str, int]
) -> None:
    """Step 4: write the termination event; never aborts."""
    evidencia = " | ".join(
        f"{campo}={metricas.get(campo, 0)}" for campo in _CAMPOS_METRICAS
    )
    try:
        escribir_evento(
            {
                "id_corrida": id_corrida,
                "tipo": "suceso" if estado == "completada" else "error",
                "codigo": motivo,
                "evidencia": evidencia,
                "marca_temporal": _ahora(),
            }
        )
    except Exception as exc:
        logger.error(
            f"Evento de terminacion no persistible | run={id_corrida} | "
            f"motivo={motivo} | {exc}"
        )


def _cerrar_recursos(contexto: RunContext | None) -> None:
    """Step 5: close open Playwright resources; errors never abort."""
    if contexto is None:
        return
    if contexto.handle_sesion is not None:
        try:
            contexto.handle_sesion.close()
        except Exception as exc:
            logger.error(
                f"page.close() fallo | run={contexto.id_corrida} | {exc}"
            )
    browser = getattr(contexto, "browser", None)
    if browser is not None:
        try:
            browser.close()
        except Exception as exc:
            logger.error(f"browser.close() fallo | run={contexto.id_corrida} | {exc}")
    playwright_instance = getattr(contexto, "playwright_instance", None)
    if playwright_instance is not None:
        try:
            playwright_instance.stop()
        except Exception as exc:
            logger.error(
                f"playwright.stop() fallo | run={contexto.id_corrida} | {exc}"
            )


def _liberar_bloqueo(id_corrida: str) -> None:
    """Step 6: release the concurrency lock; never aborts."""
    try:
        liberar_bloqueo(id_corrida)
    except Exception as exc:
        logger.error(f"liberar_bloqueo fallo | run={id_corrida} | {exc}")


def finalizar_proceso(
    contexto: RunContext | None, motivo: str
) -> ResultadoFinalizar:
    """Run the Finalizar Proceso node steps in order (section 2 of the sheet).

    Args:
        contexto: best-effort run context (may be None or partially corrupt).
        motivo: official termination reason (`corrida_completada`, `sin_fuentes`,
            `error_critico`, `aborto`).
    """
    estado = _ESTADOS_POR_MOTIVO.get(motivo, "abortada")
    id_corrida = contexto.id_corrida if contexto is not None else ""

    metricas = consultar_metricas(contexto)

    if id_corrida:
        _escribir_evento_terminacion(id_corrida, estado, motivo, metricas)
        _persistir_cierre_corrida(id_corrida, estado, motivo, metricas)

    _cerrar_recursos(contexto)
    if id_corrida:
        _liberar_bloqueo(id_corrida)

    return ResultadoFinalizar(
        estado="ok", contexto=contexto, codigo=motivo, metricas=metricas
    )
