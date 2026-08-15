"""Nodes for searching opportunities with filters (v1.1).
( RN-10: Set iterator is property of this node; reset on source change)
"""

from dataclasses import dataclass
from typing import cast

from loguru import logger

from modules.discovery.adapters.linkedin import FlowError
from modules.discovery.adapters.registry import obtener_adaptador
from modules.discovery.run_context import RunContext
from shared.models import SearchResult
from shared.retry import ejecutar_con_reintento
from shared.utilidades import acotar_evidencia


@dataclass
class ResultadoBusqueda:
    estado: str  # "ok" | "error"
    decision: str = ""  # "si" | "no" (for decision nodes)
    contexto: RunContext | None = None
    codigo: str = ""
    descripcion: str = ""


def aplicar_filtros(contexto: RunContext) -> ResultadoBusqueda:
    """
    Node: Apply basic filters.
    Iterates through filter sets and executes query via adapter.
    """
    # Paso 1: Leer insumos
    handle = contexto.handle_sesion
    fuente = contexto.fuente_corriente

    if handle is None or fuente is None:
        logger.error(f"ERR-01: session handle or source missing in run {contexto.id_corrida}")
        return ResultadoBusqueda(estado="error", codigo="ERR-01", descripcion="Insumos ausentes")

    # Paso 2: Detectar cambio de fuente y seleccionar siguiente set
    fuente_id = fuente.fuente_id
    if contexto._ultimo_fuente_id_sets != fuente_id:
        # Previous source results no longer belong to the current run segment
        contexto.search_result = None
        contexto.iterador_sets[fuente_id] = -1
        contexto._ultimo_fuente_id_sets = fuente_id

    try:
        indice = contexto.seleccionar_siguiente_set(fuente_id)
    except ValueError:
        logger.error(f"ERR-01: Unknown source {fuente_id} in run {contexto.id_corrida}")
        return ResultadoBusqueda(estado="error", codigo="ERR-01", descripcion="Fuente desconocida")
    set_actual = contexto.set_filtros(fuente, indice)

    if set_actual is None:
        logger.error(f"ERR-01: No filter set available for {fuente_id} at index {indice}")
        return ResultadoBusqueda(estado="error", codigo="ERR-01", descripcion="Set ausente")

    contexto.set_corriente = set_actual

    # Paso 3: Aplicar filtros con reintento condicional
    politicas = contexto.politicas(fuente)
    adapter = obtener_adaptador(fuente.fuente_id)

    def _fallo_final(fe: BaseException, intentos: int) -> SearchResult:
        error = cast(FlowError, fe)
        return SearchResult(
            estado="fallo",
            codigo_motivo=error.codigo_motivo,
            evidencia_acotada=acotar_evidencia(error.mensaje),
            numero_de_intentos=intentos,
            ofertas_primera_pagina=[],
            estado_paginacion="fin",
            indice_set=set_actual.indice,
        )

    def _fallo_interno(exc: Exception, intentos: int) -> SearchResult:
        logger.error(f"ERR-07: Internal error in apply_filters: {exc}")
        return SearchResult(
            estado="fallo",
            codigo_motivo="error_interno_consulta",
            evidencia_acotada=acotar_evidencia(str(exc)),
            numero_de_intentos=intentos,
            ofertas_primera_pagina=[],
            estado_paginacion="fin",
            indice_set=set_actual.indice,
        )

    res, intentos = ejecutar_con_reintento(
        lambda: adapter.apply_filters(
            page=handle, ficha=fuente, set_filtros=set_actual, politicas=politicas
        ),
        al_fallo_final=_fallo_final,
        al_error_interno=_fallo_interno,
        contexto_log=contexto.id_corrida,
    )

    # Paso 4 & 5: Resultado exitoso (intentos reales del flujo)
    contexto.search_result = res.model_copy(
        update={"numero_de_intentos": intentos}
    )
    if res.indice_set != set_actual.indice:
        logger.warning(
            "Consistency warning: search_result index "
            f"{res.indice_set} != set index {set_actual.indice}"
        )

    return ResultadoBusqueda(estado="ok", contexto=contexto)


def se_encontraron_ofertas(contexto: RunContext) -> ResultadoBusqueda:
    """
    Node: Were offers found?
    Pure decision based on the search result.
    """
    res = contexto.search_result
    if res is None:
        logger.error(f"ERR-01: search_result missing in run {contexto.id_corrida}")
        return ResultadoBusqueda(
            estado="error", codigo="ERR-01", descripcion="search_result ausente"
        )

    # Paso 2: Validar consistencia
    attrs = [
        "estado", "codigo_motivo", "evidencia_acotada", "ofertas_primera_pagina",
        "estado_paginacion", "indice_set", "numero_de_intentos"
    ]
    if not all(hasattr(res, attr) for attr in attrs):
        logger.error(f"ERR-02: Invalid search_result structure in run {contexto.id_corrida}")
        return ResultadoBusqueda(estado="error", codigo="ERR-02", descripcion="Estructura inválida")

    if res.estado == "exito" and not isinstance(res.ofertas_primera_pagina, list):
        logger.error(
            f"ERR-02: search_result success without offer list in run {contexto.id_corrida}"
        )
        return ResultadoBusqueda(estado="error", codigo="ERR-02", descripcion="Éxito sin lista")

    # Paso 3 & 4: Evaluar y Bifurcar
    condicion = (res.estado == "exito" and len(res.ofertas_primera_pagina) > 0)
    decision = "si" if condicion else "no"

    return ResultadoBusqueda(estado="ok", decision=decision, contexto=contexto)
