"""Orchestrator of the full Preparation flow (sub-fase 5.5, ficha M2).

Connects the six nodes in flow order: INICIO, candidate decision, and the
{Preparación -> Verificación -> ¿Quedan ofertas en 'descubierta'?} loop up to
`max_pasadas`, always terminating in Finalizar Proceso. Mirror of the
Discovery orchestrator: every node failure routes to a controlled
termination; the run only skips closure when INICIO failed before registering
the run row (no id, nothing closable). Informative milestones use Loguru.

Motive routing (sheet states/motives table):
- INICIO `concurrencia` (ERR-06) -> Finalizar with motive `concurrencia`.
- INICIO error WITH an id (row already registered, sub-fase 5.5 P2-A)
  -> Finalizar with motive `aborto`.
- INICIO error WITHOUT an id (nothing registered) -> report and return.
- Candidate decision "no" -> Finalizar consumes the context's pre-fixed
  `sin_pendientes`.
- Structured node aborts (BD/config codes) -> `error_critico`; unexpected
  exceptions -> `aborto`.
- Normal loop exit -> Finalizar derives `corrida_completada`/`error_total`
  from metrics.
"""

from typing import Any, Callable, Protocol

from loguru import logger

from modules.preparation.nodes.decision_bucle import ejecutar_decision_bucle
from modules.preparation.nodes.finalizar import (
    ResultadoFinalizar,
    finalizar_proceso,
)
from modules.preparation.nodes.inicio import (
    ResultadoInicio,
    ejecutar_inicio,
    quedan_ofertas_por_preparar,
)
from modules.preparation.nodes.preparacion import ejecutar_preparacion
from modules.preparation.nodes.verificacion import ejecutar_verificacion
from modules.preparation.run_context import RunContext
from shared.persistence import inicializar_si_ausente

_MOTIVO_ABORTO = "aborto"
_MOTIVO_CONCURRENCIA = "concurrencia"

# Node abort codes that mean a critical BD/config failure (ficha: `error_critico`).
_CODIGOS_CRITICOS = frozenset({"ERR-01", "ERR-03", "ERR-09"})


class _ResultadoNodo(Protocol):
    """Structural contract of every node result consumed by the flow."""

    estado: str
    codigo: str
    descripcion: str


def _decision_de(res: _ResultadoNodo) -> str:
    """Reads the `decision` field only decision nodes carry."""
    return str(getattr(res, "decision", ""))


def _terminar(contexto: RunContext, motivo: str | None) -> ResultadoFinalizar:
    """Controlled termination: close the run and log the outcome."""
    resultado = finalizar_proceso(contexto, motivo)
    logger.info(
        f"Corrida {contexto.id_corrida} terminada | motivo={resultado.codigo}"
    )
    return resultado


def _fallo_nodo(contexto: RunContext, nodo: str, resultado: _ResultadoNodo) -> None:
    """Routes a structured node abort to the controlled critical termination."""
    logger.error(
        f"{nodo} abortado | run={contexto.id_corrida} | "
        f"codigo={resultado.codigo} | {resultado.descripcion}"
    )
    _terminar(contexto, "error_critico")


def _ejecutar_nodo(
    contexto: RunContext,
    nombre: str,
    llamada: Callable[[], _ResultadoNodo],
) -> _ResultadoNodo | None:
    """Runs a node; structured aborts -> `error_critico`, exceptions -> `aborto`.

    Returns the node result when it is not an abort, or None after the
    controlled termination.
    """
    try:
        res = llamada()
    except Exception as exc:  # unexpected node crash: aborto
        logger.error(f"{nombre} excepcion | run={contexto.id_corrida} | {exc}")
        _terminar(contexto, _MOTIVO_ABORTO)
        return None
    if res.estado in ("error", "abortada"):
        if res.codigo not in _CODIGOS_CRITICOS:
            # Non-critical structured failure (none today): aborto.
            logger.error(
                f"{nombre} abortado | run={contexto.id_corrida} | "
                f"codigo={res.codigo} | {res.descripcion}"
            )
            _terminar(contexto, _MOTIVO_ABORTO)
            return None
        _fallo_nodo(contexto, nombre, res)
        return None
    return res


def ejecutar_flujo(config: dict[str, Any] | None = None) -> None:
    """Run the complete Preparation flow; terminates in Finalizar Proceso."""
    if inicializar_si_ausente():
        logger.info("Esquema de base de datos creado automaticamente")
    resultado_inicio: ResultadoInicio = ejecutar_inicio(config)
    if resultado_inicio.estado == "error":
        if resultado_inicio.id_corrida:
            # Row already registered (P2-A): close it as a controlled abort.
            logger.error(
                f"INICIO fallo | run={resultado_inicio.id_corrida} | "
                f"codigo={resultado_inicio.codigo} | {resultado_inicio.descripcion}"
            )
            finalizar_proceso(
                None, _MOTIVO_ABORTO, resultado_inicio.id_corrida
            )
        else:
            print(
                f"[ERROR] INICIO no entrego corrida | "
                f"codigo={resultado_inicio.codigo} | "
                f"{resultado_inicio.descripcion}"
            )
        return
    if resultado_inicio.estado == "concurrencia":
        logger.warning(
            f"Corrida {resultado_inicio.id_corrida} no iniciada: "
            "otra corrida activa (ERR-06)"
        )
        finalizar_proceso(None, _MOTIVO_CONCURRENCIA, resultado_inicio.id_corrida)
        return

    contexto = resultado_inicio.contexto
    assert contexto is not None
    logger.info(
        f"Corrida {contexto.id_corrida} iniciada | "
        f"{len(contexto.candidatas)} candidatas en cola"
    )

    res_candidatas = _ejecutar_nodo(
        contexto,
        "quedan_ofertas_por_preparar",
        lambda: quedan_ofertas_por_preparar(contexto),
    )
    if res_candidatas is None:
        return
    if _decision_de(res_candidatas) == "no":
        # The node pre-fixed `sin_pendientes` on the context (VAL-04).
        _terminar(contexto, None)
        return

    while True:
        res_preparacion = _ejecutar_nodo(
            contexto, "preparacion", lambda: ejecutar_preparacion(contexto)
        )
        if res_preparacion is None:
            return

        res_verificacion = _ejecutar_nodo(
            contexto, "verificacion", lambda: ejecutar_verificacion(contexto)
        )
        if res_verificacion is None:
            return

        res_bucle = _ejecutar_nodo(
            contexto, "decision_bucle", lambda: ejecutar_decision_bucle(contexto)
        )
        if res_bucle is None:
            return
        # The loop node signals through its state (`continuar`/`finalizar`),
        # not a `decision` field.
        if res_bucle.estado != "continuar":
            break
        logger.info(
            f"Pasada completada | run={contexto.id_corrida} | "
            "quedan ofertas en 'descubierta': otra pasada"
        )

    # Normal exit: Finalizar derives `corrida_completada`/`error_total`.
    _terminar(contexto, None)
