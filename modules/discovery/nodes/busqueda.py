"""Nodes for searching opportunities with filters (v1.1).
( RN-10: Set iterator is property of this node; reset on source change)
"""

import time
from dataclasses import dataclass

from loguru import logger

from modules.discovery.adapters.linkedin import FlowError, LinkedInAdapter
from modules.discovery.run_context import RunContext
from shared.config import load
from shared.models import SearchResult
from shared.retry import should_retry
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
        logger.error(f"ERR-01: session handle or source missing in run {contexto.run_id}")
        return ResultadoBusqueda(estado="error", codigo="ERR-01", descripcion="Insumos ausentes")

    # Paso 2: Detectar cambio de fuente y seleccionar siguiente set
    source_id = fuente.source_id
    if contexto._ultimo_source_id_sets != source_id:
        # Previous source results no longer belong to the current run segment
        contexto.search_result = None
        contexto.iterador_sets[source_id] = -1
        contexto._ultimo_source_id_sets = source_id

    try:
        indice = contexto.seleccionar_siguiente_set(source_id)
    except ValueError:
        logger.error(f"ERR-01: Unknown source {source_id} in run {contexto.run_id}")
        return ResultadoBusqueda(estado="error", codigo="ERR-01", descripcion="Fuente desconocida")
    set_actual = contexto.set_filtros(fuente, indice)

    if set_actual is None:
        logger.error(f"ERR-01: No filter set available for {source_id} at index {indice}")
        return ResultadoBusqueda(estado="error", codigo="ERR-01", descripcion="Set ausente")

    contexto.set_corriente = set_actual

    # Paso 3: Aplicar filtros con reintento condicional
    politicas = contexto.politicas(fuente)
    adapter = LinkedInAdapter()
    cfg_retries = load().get("retries", {})
    max_attempts = cfg_retries.get("max_attempts", 3)
    base_wait = cfg_retries.get("base_wait_seconds", 2)
    multiplier = cfg_retries.get("multiplier", 2)
    max_wait = cfg_retries.get("max_wait_seconds", 30)

    attempt = 0
    while attempt < max_attempts:
        attempt += 1
        try:
            res = adapter.apply_filters(
                page=handle, ficha=fuente, set_filtros=set_actual, politicas=politicas
            )
            # Paso 4 & 5: Resultado exitoso (intentos reales del flujo)
            contexto.search_result = res.model_copy(
                update={"numero_de_intentos": attempt}
            )
            if res.set_indice != set_actual.indice:
                logger.warning(
                    "Consistency warning: search_result index "
                    f"{res.set_indice} != set index {set_actual.indice}"
                )

            return ResultadoBusqueda(estado="ok", contexto=contexto)

        except FlowError as fe:
            if should_retry(fe.codigo_motivo) and attempt < max_attempts:
                wait_time = min(base_wait * (multiplier ** (attempt - 1)), max_wait)
                time.sleep(wait_time)
                continue
            else:
                # Paso 6: Fallo definitivo
                contexto.search_result = SearchResult(
                    estado="fallo",
                    codigo_motivo=fe.codigo_motivo,
                    evidencia_acotada=acotar_evidencia(fe.mensaje),
                    numero_de_intentos=attempt,
                    ofertas_primera_pagina=[],
                    estado_paginacion="fin",
                    set_indice=set_actual.indice,
                )
                return ResultadoBusqueda(estado="ok", contexto=contexto)
        except Exception as e:
            logger.error(f"ERR-07: Internal error in apply_filters: {e}")
            contexto.search_result = SearchResult(
                estado="fallo",
                codigo_motivo="error_interno_consulta",
                evidencia_acotada=acotar_evidencia(str(e)),
                numero_de_intentos=attempt,
                ofertas_primera_pagina=[],
                estado_paginacion="fin",
                set_indice=set_actual.indice,
            )
            return ResultadoBusqueda(estado="ok", contexto=contexto)
    contexto.search_result = SearchResult(
        estado="fallo",
        codigo_motivo="error_interno_consulta",
        evidencia_acotada="no attempts configured",
        numero_de_intentos=0,
        ofertas_primera_pagina=[],
        estado_paginacion="fin",
        set_indice=set_actual.indice,
    )
    return ResultadoBusqueda(estado="ok", contexto=contexto)


def se_encontraron_ofertas(contexto: RunContext) -> ResultadoBusqueda:
    """
    Node: Were offers found?
    Pure decision based on the search result.
    """
    res = contexto.search_result
    if res is None:
        logger.error(f"ERR-01: search_result missing in run {contexto.run_id}")
        return ResultadoBusqueda(
            estado="error", codigo="ERR-01", descripcion="search_result ausente"
        )

    # Paso 2: Validar consistencia
    attrs = [
        "estado", "codigo_motivo", "evidencia_acotada", "ofertas_primera_pagina",
        "estado_paginacion", "set_indice", "numero_de_intentos"
    ]
    if not all(hasattr(res, attr) for attr in attrs):
        logger.error(f"ERR-02: Invalid search_result structure in run {contexto.run_id}")
        return ResultadoBusqueda(estado="error", codigo="ERR-02", descripcion="Estructura inválida")

    if res.estado == "exito" and not isinstance(res.ofertas_primera_pagina, list):
        logger.error(f"ERR-02: search_result success without offer list in run {contexto.run_id}")
        return ResultadoBusqueda(estado="error", codigo="ERR-02", descripcion="Éxito sin lista")

    # Paso 3 & 4: Evaluar y Bifurcar
    condicion = (res.estado == "exito" and len(res.ofertas_primera_pagina) > 0)
    decision = "si" if condicion else "no"

    return ResultadoBusqueda(estado="ok", decision=decision, contexto=contexto)
