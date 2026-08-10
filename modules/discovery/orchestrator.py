"""Orchestrator of the full Discovery flow (Sub-fase 4.5).

Connects all thirteen nodes in flow order (ficha técnica): INICIO, source
control decisions, platform entry, filter search, capture/registration and
Finalizar Proceso. Every node failure in a process node or decision-validator
error leads to a controlled termination with motivo `aborto`; the run always
finishes in `finalizar_proceso` except when INICIO itself failed (no context
to close, no lock owned). Informative milestones are logged with Loguru.
"""

from typing import Any

from loguru import logger

from modules.discovery.nodes.busqueda import aplicar_filtros, se_encontraron_ofertas
from modules.discovery.nodes.captura import (
    capturar_ofertas,
    quedan_ofertas_por_capturar,
    quedan_sets_por_aplicar,
    registrar_ofertas,
)
from modules.discovery.nodes.control_fuentes import (
    existen_fuentes_configuradas,
    quedan_fuentes_por_procesar,
    seleccionar_fuente_pendiente,
)
from modules.discovery.nodes.finalizar import consultar_metricas, finalizar_proceso
from modules.discovery.nodes.ingreso import ejecutar_ingreso, ingreso_exitoso
from modules.discovery.nodes.inicio import ejecutar_inicio
from modules.discovery.nodes.registro import registrar_evento
from modules.discovery.run_context import RunContext

_MOTIVO_ABORTO = "aborto"
_MOTIVO_SIN_FUENTES = "sin_fuentes"
_MOTIVO_CORRIDA_COMPLETADA = "corrida_completada"


def _cerrar_sesion_anterior(contexto: RunContext) -> None:
    """Best-effort close of the previous source session before switching."""
    pagina = contexto.handle_sesion
    if pagina is None:
        return
    try:
        pagina.close()
    except Exception as exc:
        logger.warning(
            f"Fallo al cerrar sesion anterior | run={contexto.run_id} | {exc}"
        )
    finally:
        contexto.handle_sesion = None
        contexto.session_id = None


def _terminar(contexto: RunContext, motivo: str) -> None:
    """Controlled termination: persist closure and log final metrics."""
    contexto.motivo_terminacion = motivo
    finalizar_proceso(contexto, motivo)
    metricas = consultar_metricas(contexto)
    resumen = " | ".join(
        f"{campo}={metricas.get(campo, 0)}" for campo in metricas
    )
    logger.info(
        f"Corrida finalizada | run={contexto.run_id} | motivo={motivo} | "
        f"{resumen}"
    )


def _fallo_nodo(
    contexto: RunContext, nodo: str, resultado: Any, descripcion_texto: str
) -> None:
    logger.error(f"{nodo} fallo | run={contexto.run_id} | {descripcion_texto}")
    _terminar(contexto, _MOTIVO_ABORTO)


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
        f"Corrida {contexto.run_id} iniciada | "
        f"{len(contexto.fuentes_filtradas)} fuentes configuradas"
    )

    res_existencia = existen_fuentes_configuradas(contexto)
    if res_existencia.estado == "error":
        _fallo_nodo(
            contexto,
            "existen_fuentes_configuradas",
            res_existencia,
            res_existencia.descripcion,
        )
        return
    if res_existencia.decision == "no":
        _terminar(contexto, _MOTIVO_SIN_FUENTES)
        return

    while True:
        res_quedan = quedan_fuentes_por_procesar(contexto)
        if res_quedan.estado == "error":
            _fallo_nodo(
                contexto,
                "quedan_fuentes_por_procesar",
                res_quedan,
                res_quedan.descripcion,
            )
            return
        if res_quedan.decision == "no":
            _terminar(contexto, _MOTIVO_CORRIDA_COMPLETADA)
            return

        _cerrar_sesion_anterior(contexto)

        res_seleccion = seleccionar_fuente_pendiente(contexto)
        if res_seleccion.estado == "error":
            _fallo_nodo(
                contexto,
                "seleccionar_fuente_pendiente",
                res_seleccion,
                res_seleccion.descripcion,
            )
            return
        fuente = contexto.fuente_corriente
        assert fuente is not None
        logger.info(f"Procesando fuente {fuente.source_id}")

        res_ingreso = ejecutar_ingreso(contexto)
        if res_ingreso.estado == "error":
            _fallo_nodo(
                contexto, "ejecutar_ingreso", res_ingreso, res_ingreso.descripcion
            )
            return
        res_ingreso_exitoso = ingreso_exitoso(contexto)
        if res_ingreso_exitoso.estado == "error":
            _fallo_nodo(
                contexto,
                "ingreso_exitoso",
                res_ingreso_exitoso,
                res_ingreso_exitoso.descripcion,
            )
            return
        if res_ingreso_exitoso.decision == "no":
            registrar_evento(contexto)
            continue

        logger.info(
            f"Ingreso exitoso | fuente={fuente.source_id} | "
            f"session={contexto.session_id}"
        )

        while True:
            res_filtros = aplicar_filtros(contexto)
            if res_filtros.estado == "error":
                _fallo_nodo(
                    contexto, "aplicar_filtros", res_filtros, res_filtros.descripcion
                )
                return
            res_ofertas = se_encontraron_ofertas(contexto)
            if res_ofertas.estado == "error":
                _fallo_nodo(
                    contexto,
                    "se_encontraron_ofertas",
                    res_ofertas,
                    res_ofertas.descripcion,
                )
                return
            if res_ofertas.decision == "no":
                registrar_evento(contexto)
                res_sets_tras_vacio = quedan_sets_por_aplicar(contexto)
                if res_sets_tras_vacio.estado == "error":
                    _fallo_nodo(
                        contexto,
                        "quedan_sets_por_aplicar",
                        res_sets_tras_vacio,
                        res_sets_tras_vacio.descripcion,
                    )
                    return
                if res_sets_tras_vacio.decision == "si":
                    continue
                break

            res_captura = capturar_ofertas(contexto)
            if res_captura.estado == "error":
                _fallo_nodo(
                    contexto, "capturar_ofertas", res_captura, res_captura.descripcion
                )
                return
            res_registro = registrar_ofertas(contexto)
            if res_registro.estado == "error":
                _fallo_nodo(
                    contexto,
                    "registrar_ofertas",
                    res_registro,
                    res_registro.descripcion,
                )
                return
            res_quedan_ofertas = quedan_ofertas_por_capturar(contexto)
            if res_quedan_ofertas.estado == "error":
                _fallo_nodo(
                    contexto,
                    "quedan_ofertas_por_capturar",
                    res_quedan_ofertas,
                    res_quedan_ofertas.descripcion,
                )
                return
            lote = contexto.capture_batch
            capturadas = len(lote.ofertas) if lote is not None else 0
            indicador_set = (
                contexto.set_corriente.indice
                if contexto.set_corriente is not None
                else "desconocido"
            )
            logger.info(
                f"Capturadas {capturadas} ofertas | fuente={fuente.source_id} | "
                f"set={indicador_set}"
            )
            res_sets = quedan_sets_por_aplicar(contexto)
            if res_sets.estado == "error":
                _fallo_nodo(
                    contexto,
                    "quedan_sets_por_aplicar",
                    res_sets,
                    res_sets.descripcion,
                )
                return
            if res_sets.decision == "si":
                continue
            break
