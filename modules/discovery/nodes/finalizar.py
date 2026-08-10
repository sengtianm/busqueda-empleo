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
    liberar_bloqueo,
    read_table,
    write_evento,
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
    run_id = contexto.run_id
    try:
        ofertas = read_table("ofertas", {"run_id": run_id})
        eventos = read_table("eventos", {"run_id": run_id})
    except Exception as exc:
        logger.error(
            f"Metricas no consultables | run={run_id} | {exc} | "
            "se degrada a ceros"
        )
        return {campo: 0 for campo in _CAMPOS_METRICAS}
    errores = sum(1 for e in eventos if e.get("tipo") == "error")
    sucesos = len(eventos) - errores
    fuentes = len({e.get("source_id") for e in eventos if e.get("source_id")})
    return {
        "total_ofertas": len(ofertas),
        "total_errores": errores,
        "total_sucesos": sucesos,
        "fuentes_procesadas": fuentes,
    }


def _persistir_cierre_corrida(
    run_id: str, estado: str, motivo: str, metricas: dict[str, int]
) -> None:
    """Step 3: update the run row with a single retry; never aborts."""
    campos: dict[str, Any] = {
        "estado": estado,
        "timestamp_fin": _ahora(),
        "motivo_terminacion": motivo,
        **metricas,
    }
    for intento in (1, 2):
        try:
            actualizar_corrida(run_id, campos)
            return
        except Exception as exc:
            logger.error(
                f"actualizar_corrida fallo (intento {intento}/2) | "
                f"run={run_id} | {exc}"
            )
    logger.error(f"Corrida no persistida | run={run_id} | estado={estado} | {motivo}")


def _escribir_evento_terminacion(
    run_id: str, estado: str, motivo: str, metricas: dict[str, int]
) -> None:
    """Step 4: write the termination event; never aborts."""
    evidencia = " | ".join(
        f"{campo}={metricas.get(campo, 0)}" for campo in _CAMPOS_METRICAS
    )
    try:
        write_evento(
            {
                "run_id": run_id,
                "tipo": "suceso" if estado == "completada" else "error",
                "codigo": motivo,
                "evidencia": evidencia,
                "timestamp": _ahora(),
            }
        )
    except Exception as exc:
        logger.error(
            f"Evento de terminacion no persistible | run={run_id} | "
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
                f"page.close() fallo | run={contexto.run_id} | {exc}"
            )
    browser = getattr(contexto, "browser", None)
    if browser is not None:
        try:
            browser.close()
        except Exception as exc:
            logger.error(f"browser.close() fallo | run={contexto.run_id} | {exc}")
    playwright_instance = getattr(contexto, "playwright_instance", None)
    if playwright_instance is not None:
        try:
            playwright_instance.stop()
        except Exception as exc:
            logger.error(
                f"playwright.stop() fallo | run={contexto.run_id} | {exc}"
            )


def _liberar_bloqueo(run_id: str) -> None:
    """Step 6: release the concurrency lock; never aborts."""
    try:
        liberar_bloqueo(run_id)
    except Exception as exc:
        logger.error(f"liberar_bloqueo fallo | run={run_id} | {exc}")


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
    run_id = contexto.run_id if contexto is not None else ""

    metricas_previas = consultar_metricas(contexto)

    if run_id:
        _escribir_evento_terminacion(run_id, estado, motivo, metricas_previas)

    metricas = consultar_metricas(contexto)

    if run_id:
        _persistir_cierre_corrida(run_id, estado, motivo, metricas)

    _cerrar_recursos(contexto)
    if run_id:
        _liberar_bloqueo(run_id)

    return ResultadoFinalizar(
        estado="ok", contexto=contexto, codigo=motivo, metricas=metricas
    )
