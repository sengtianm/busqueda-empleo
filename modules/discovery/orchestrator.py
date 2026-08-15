"""Orchestrator of the full Discovery flow (Sub-fase 4.5).

Connects all twelve nodes in flow order (ficha técnica): INICIO, source
control decisions, platform entry, filter search, capture/registration and
Finalizar Proceso. Every node failure in a process node or decision-validator
error leads to a controlled termination with motivo `aborto`; the run always
finishes in `finalizar_proceso` except when INICIO itself failed (no context
to close, no lock owned). Informative milestones are logged with Loguru.
"""

from typing import Callable, Protocol

from loguru import logger

from modules.discovery.nodes.busqueda import aplicar_filtros, se_encontraron_ofertas
from modules.discovery.nodes.captura import (
    capturar_ofertas,
    quedan_sets_por_aplicar,
    registrar_ofertas,
)
from modules.discovery.nodes.control_fuentes import (
    existen_fuentes_configuradas,
    quedan_fuentes_por_procesar,
    seleccionar_fuente_pendiente,
)
from modules.discovery.nodes.finalizar import cerrar_recursos, finalizar_proceso
from modules.discovery.nodes.ingreso import ejecutar_ingreso, ingreso_exitoso
from modules.discovery.nodes.inicio import ejecutar_inicio
from modules.discovery.nodes.registro import registrar_evento
from modules.discovery.run_context import RunContext

_MOTIVO_ABORTO = "aborto"
_MOTIVO_SIN_FUENTES = "sin_fuentes"
_MOTIVO_CORRIDA_COMPLETADA = "corrida_completada"


class _ResultadoNodo(Protocol):
    """Structural contract of every node result consumed by the flow."""

    estado: str
    descripcion: str
    decision: str


def _cerrar_sesion_anterior(contexto: RunContext) -> None:
    """Best-effort close of the previous source session before switching."""
    cerrar_recursos(contexto)
    contexto.id_sesion = None


def _terminar(contexto: RunContext, motivo: str) -> None:
    """Controlled termination: persist closure and log final metrics."""
    resultado = finalizar_proceso(contexto, motivo)
    metricas = resultado.metricas
    if metricas:
        resumen = " | ".join(
            f"{campo}={metricas.get(campo, 0)}" for campo in metricas
        )
        logger.info(
            f"Corrida finalizada | run={contexto.id_corrida} | motivo={motivo} | "
            f"{resumen}"
        )


def _fallo_nodo(contexto: RunContext, nodo: str, descripcion_texto: str) -> None:
    logger.error(f"{nodo} fallo | run={contexto.id_corrida} | {descripcion_texto}")
    _terminar(contexto, _MOTIVO_ABORTO)


def _ejecutar_nodo(
    contexto: RunContext,
    nombre: str,
    llamada: Callable[[], _ResultadoNodo],
) -> _ResultadoNodo | None:
    """Runs a node and routes its error outcome to the controlled abort."""
    res = llamada()
    if res.estado == "error":
        _fallo_nodo(contexto, nombre, res.descripcion)
        return None
    return res


def ejecutar_flujo() -> None:
    """Run the complete Discovery flow; terminates in Finalizar Proceso."""
    resultado_inicio = ejecutar_inicio()
    if resultado_inicio.estado != "ok":
        print(
            f"[ERROR] INICIO no entrego contexto | "
            f"estado={resultado_inicio.estado} | "
            f"codigo={resultado_inicio.codigo} | "
            f"{resultado_inicio.descripcion}"
        )
        return
    contexto = resultado_inicio.contexto
    assert contexto is not None

    logger.info(
        f"Corrida {contexto.id_corrida} iniciada | "
        f"{len(contexto.fuentes_filtradas)} fuentes configuradas"
    )

    res_existencia = _ejecutar_nodo(
        contexto,
        "existen_fuentes_configuradas",
        lambda: existen_fuentes_configuradas(contexto),
    )
    if res_existencia is None:
        return
    if res_existencia.decision == "no":
        _terminar(contexto, _MOTIVO_SIN_FUENTES)
        return

    while True:
        res_quedan = _ejecutar_nodo(
            contexto,
            "quedan_fuentes_por_procesar",
            lambda: quedan_fuentes_por_procesar(contexto),
        )
        if res_quedan is None:
            return
        if res_quedan.decision == "no":
            _terminar(contexto, _MOTIVO_CORRIDA_COMPLETADA)
            return

        _cerrar_sesion_anterior(contexto)

        res_seleccion = _ejecutar_nodo(
            contexto,
            "seleccionar_fuente_pendiente",
            lambda: seleccionar_fuente_pendiente(contexto),
        )
        if res_seleccion is None:
            return
        fuente = contexto.fuente_corriente
        assert fuente is not None
        logger.info(f"Procesando fuente {fuente.fuente_id}")

        res_ingreso = _ejecutar_nodo(
            contexto, "ejecutar_ingreso", lambda: ejecutar_ingreso(contexto)
        )
        if res_ingreso is None:
            return
        res_ingreso_exitoso = _ejecutar_nodo(
            contexto, "ingreso_exitoso", lambda: ingreso_exitoso(contexto)
        )
        if res_ingreso_exitoso is None:
            return
        if res_ingreso_exitoso.decision == "no":
            registrar_evento(contexto)
            continue

        logger.info(
            f"Ingreso exitoso | fuente={fuente.fuente_id} | "
            f"session={contexto.id_sesion}"
        )

        while True:
            res_filtros = _ejecutar_nodo(
                contexto, "aplicar_filtros", lambda: aplicar_filtros(contexto)
            )
            if res_filtros is None:
                return
            res_ofertas = _ejecutar_nodo(
                contexto, "se_encontraron_ofertas", lambda: se_encontraron_ofertas(contexto)
            )
            if res_ofertas is None:
                return
            if res_ofertas.decision == "no":
                registrar_evento(contexto)
                res_sets_tras_vacio = _ejecutar_nodo(
                    contexto,
                    "quedan_sets_por_aplicar",
                    lambda: quedan_sets_por_aplicar(contexto),
                )
                if res_sets_tras_vacio is None:
                    return
                if res_sets_tras_vacio.decision == "si":
                    continue
                break

            res_captura = _ejecutar_nodo(
                contexto, "capturar_ofertas", lambda: capturar_ofertas(contexto)
            )
            if res_captura is None:
                return
            res_registro = _ejecutar_nodo(
                contexto, "registrar_ofertas", lambda: registrar_ofertas(contexto)
            )
            if res_registro is None:
                return
            lote = contexto.capture_batch
            capturadas = len(lote.ofertas) if lote is not None else 0
            indicador_set = (
                contexto.set_corriente.indice
                if contexto.set_corriente is not None
                else "desconocido"
            )
            logger.info(
                f"Capturadas {capturadas} ofertas | fuente={fuente.fuente_id} | "
                f"set={indicador_set}"
            )
            res_sets = _ejecutar_nodo(
                contexto,
                "quedan_sets_por_aplicar",
                lambda: quedan_sets_por_aplicar(contexto),
            )
            if res_sets is None:
                return
            if res_sets.decision == "si":
                continue
            break
