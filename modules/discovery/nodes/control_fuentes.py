"""Source control nodes of the Discovery flow (technical sheet v1.0).

Three nodes implemented here:

1. Decision "¿Existe al menos una fuente configurada?" (v1.0)
2. Decision "¿Quedan fuentes por procesar en esta corrida?" (v1.0)
3. Process "Seleccionar la siguiente fuente pendiente" (v1.0)

All three operate exclusively on the execution context (RN-01): no config
store I/O, no network access, no database writes (RN-05, decisions). The
only admissible side effects are, in the selection node, mutating the
iterator and current source. Abort protocol (ERR-01..ERR-03) registers a
critical event and delivers control to "Finalizar Proceso" with state error.

Note: the technical sheet lists "¿Es la primera ejecución del ciclo?" as
sucesorcandidate of node 1 pending redefinition; per sub-phase 4.1
instruction, the Yes branch goes directly to the iteration decision.
"""

from dataclasses import dataclass
from datetime import datetime

from loguru import logger

from modules.discovery.run_context import RunContext
from shared.persistence import write_evento

_FORMATO_TIMESTAMP = "%Y-%m-%d %H:%M:%S"


@dataclass
class ResultadoControlFuentes:
    """Outcome of any of the three source control nodes."""

    estado: str  # "ok" | "error"
    decision: str = ""  # "si" | "no" (only decision nodes)
    contexto: RunContext | None = None
    codigo: str = ""
    descripcion: str = ""


def _ahora() -> str:
    return datetime.now().strftime(_FORMATO_TIMESTAMP)


def _registrar_evento(contexto: RunContext | None, codigo: str, evidencia: str) -> None:
    """Critical abort event; falls back to Loguru when the store rejects it."""
    id_corrida = contexto.id_corrida if contexto is not None else ""
    if not id_corrida:
        logger.error(f"{codigo} | sin id_corrida | {evidencia}")
        return
    try:
        write_evento(
            {
                "id_corrida": id_corrida,
                "tipo": "error",
                "codigo": codigo,
                "evidencia": evidencia,
                "marca_temporal": _ahora(),
            }
        )
    except Exception as exc:
        logger.error(f"Evento no persistible | run={id_corrida} | {codigo} | {exc}")


def _abortar(
    contexto: RunContext | None, codigo: str, descripcion: str
) -> ResultadoControlFuentes:
    _registrar_evento(contexto, codigo, descripcion)
    logger.error(f"{codigo} | run={getattr(contexto, 'id_corrida', '')} | {descripcion}")
    return ResultadoControlFuentes(
        estado="error",
        contexto=contexto,
        codigo=codigo,
        descripcion=descripcion,
    )


def existen_fuentes_configuradas(
    contexto: RunContext | None,
) -> ResultadoControlFuentes:
    """Decision v1.0: "¿Existe al menos una fuente configurada?"."""
    if contexto is None:
        return _abortar(
            contexto,
            "ERR-01",
            "contexto ausente: no se puede evaluar la existencia de fuentes",
        )

    lista = contexto.fuentes_filtradas
    if not isinstance(lista, list):
        return _abortar(
            contexto,
            "ERR-01",
            "contexto incompleto: la lista de fuentes no es accesible",
        )

    if len(lista) > 0:
        return ResultadoControlFuentes(
            estado="ok", decision="si", contexto=contexto
        )

    return ResultadoControlFuentes(
        estado="ok", decision="no", contexto=contexto
    )


def quedan_fuentes_por_procesar(
    contexto: RunContext | None,
) -> ResultadoControlFuentes:
    """Decision node: "¿Quedan fuentes por procesar en esta corrida?" (v1.0)."""
    if contexto is None or not isinstance(contexto.iterador_fuentes, int):
        return _abortar(
            contexto,
            "ERR-01",
            "iterador ausente o corrupto: no se puede calcular el progreso",
        )

    lista = contexto.fuentes_filtradas
    if not isinstance(lista, list):
        return _abortar(
            contexto,
            "ERR-01",
            "contexto incompleto: la lista de fuentes no es accesible",
        )

    # VAL-01: progreso válido — iterador en rango [-1, len(lista) - 1]
    if not (-1 <= contexto.iterador_fuentes <= len(lista) - 1):
        return _abortar(
            contexto,
            "ERR-01",
            f"iterador fuera de rango: {contexto.iterador_fuentes} (valido: -1..{len(lista) - 1})",
        )

    pendientes = [
        pos
        for pos, _ in enumerate(lista)
        if pos > contexto.iterador_fuentes
    ]

    if pendientes:
        return ResultadoControlFuentes(
            estado="ok", decision="si", contexto=contexto
        )

    return ResultadoControlFuentes(
        estado="ok", decision="no", contexto=contexto
    )


def seleccionar_fuente_pendiente(
    contexto: RunContext | None,
) -> ResultadoControlFuentes:
    """Process node v1.0: "Seleccionar la siguiente fuente pendiente"."""
    if contexto is None or not isinstance(contexto.iterador_fuentes, int):
        return _abortar(
            contexto,
            "ERR-01",
            "iterador ausente o corrupto: el nodo de seleccion no puede operar",
        )

    lista = contexto.fuentes_filtradas
    if not isinstance(lista, list):
        return _abortar(
            contexto,
            "ERR-01",
            "contexto incompleto: la lista de fuentes no es accesible",
        )

    # VAL-01: progreso válido — iterador en rango [-1, len(lista) - 1]
    if not (-1 <= contexto.iterador_fuentes <= len(lista) - 1):
        return _abortar(
            contexto,
            "ERR-01",
            f"iterador fuera de rango: {contexto.iterador_fuentes} (valido: -1..{len(lista) - 1})",
        )

    try:
        posicion = next(
            pos
            for pos, _ in enumerate(lista)
            if pos > contexto.iterador_fuentes
        )
    except StopIteration:
        return _abortar(
            contexto,
            "ERR-02",
            "no existe fuente pendiente pese al contrato de la rama Sí",
        )

    try:
        contexto.iterador_fuentes = posicion
        contexto.fuente_corriente = lista[posicion]
    except Exception as exc:
        return _abortar(
            contexto,
            "ERR-03",
            f"fallo interno al mutar el contexto: {exc}",
        )

    return ResultadoControlFuentes(
        estado="ok",
        decision="",
        contexto=contexto,
        descripcion=(
            f"fuente corriente fijada: {getattr(contexto.fuente_corriente, 'fuente_id', '')} "
            f"en posicion {posicion}"
        ),
    )
