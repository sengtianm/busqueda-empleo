"""Nodos de captura y registro de ofertas (Sub-fase 4.4).

Cubre los nodos "Capturar ofertas", "Registrar ofertas en Ofertas Totales",
"¿Quedan ofertas por capturar?" y "¿Quedan sets de filtros por aplicar?"
(DOC-04 Section 15). El adaptador resuelve toda la paginación internamente
(RN-10), por lo que el bucle interno de captura se ejecuta una sola vez por
set; la deduplicación se hace por `id_externo`.
"""

from dataclasses import dataclass
from time import monotonic
from typing import Any, cast

from loguru import logger

from modules.discovery.adapters.linkedin import FlowError
from modules.discovery.adapters.registry import obtener_adaptador
from modules.discovery.run_context import RunContext
from shared.models import AuditoriaSesion, CaptureBatch, EstadoCaptura, Offer
from shared.persistence import (
    escribir_evento_seguro,
    escribir_fila,
    upsert_lote_ofertas,
)
from shared.retry import ejecutar_con_reintento
from shared.utilidades import FORMATO_TIMESTAMP, acotar_evidencia, ahora


@dataclass
class ResultadoCaptura:
    estado: str  # "ok" | "error"
    decision: str = ""  # "si" | "no" (solo nodos de decisión)
    contexto: RunContext | None = None
    codigo: str = ""
    descripcion: str = ""


def _registrar_evento(
    contexto: RunContext,
    tipo: str,
    codigo: str,
    evidencia: str,
) -> None:
    """Escribe un evento en la tabla `eventos` sin abortar el flujo."""
    escribir_evento_seguro(
        {
            "id_corrida": contexto.id_corrida,
            "fuente_id": (
                contexto.fuente_corriente.fuente_id
                if contexto.fuente_corriente
                else ""
            ),
            "id_sesion": contexto.id_sesion,
            "indice_set": (
                contexto.set_corriente.indice
                if contexto.set_corriente
                else None
            ),
            "marca_temporal": ahora(),
            "tipo": tipo,
            "codigo": codigo,
            "evidencia": evidencia,
        },
        contexto_log=contexto.id_corrida,
    )


def capturar_ofertas(contexto: RunContext) -> ResultadoCaptura:
    """Nodo: Capturar ofertas (v1.0).

    Invoca al adaptador UNA SOLA VEZ con reintento condicional
    (máximo 3 intentos totales, solo códigos reintentables como
    `tiempo_agotado_captura`). En éxito guarda los resultados en el contexto y
    escribe la auditoría de sesión; en fallo descarta el set completo
    (las ofertas parciales) y continúa con el siguiente set.
    """
    # Paso 1: verificar insumos
    if contexto.handle_sesion is None:
        logger.error(f"ERR-01: handle_sesion ausente en corrida {contexto.id_corrida}")
        return ResultadoCaptura(
            estado="error", codigo="ERR-01", descripcion="Insumos ausentes"
        )
    fuente = contexto.fuente_corriente
    if fuente is None:
        logger.error(f"ERR-01: fuente_corriente ausente en corrida {contexto.id_corrida}")
        return ResultadoCaptura(
            estado="error", codigo="ERR-01", descripcion="Fuente ausente"
        )
    set_actual = contexto.set_corriente
    if set_actual is None:
        logger.error(f"ERR-01: set_corriente ausente en corrida {contexto.id_corrida}")
        return ResultadoCaptura(
            estado="error", codigo="ERR-01", descripcion="Set ausente"
        )

    # Paso 2: obtener políticas
    politicas = contexto.politicas(fuente)

    # Paso 3: ejecutar captura con reintento condicional
    adapter = obtener_adaptador(fuente.fuente_id)
    inicio_captura = monotonic()

    def _fallo_captura(fe: BaseException, intentos: int) -> ResultadoCaptura:
        error = cast(FlowError, fe)
        # Paso 6: fallo definitivo (no reintentable o intentos agotados)
        estado_fallo = EstadoCaptura(estado="fallo", codigo_motivo=error.codigo_motivo)
        contexto.capture_batch = None
        contexto.estado_captura = estado_fallo
        _registrar_evento(
            contexto,
            tipo="error",
            codigo=error.codigo_motivo,
            evidencia=acotar_evidencia(error.mensaje),
        )
        return ResultadoCaptura(estado="ok", contexto=contexto)

    def _fallo_interno(exc: Exception, intentos: int) -> ResultadoCaptura:
        if intentos == 0:
            return ResultadoCaptura(
                estado="error",
                codigo="ERR-09",
                descripcion="Sin intentos configurados",
            )
        logger.error(f"ERR-07: Error interno en captura: {exc}")
        estado_falla = EstadoCaptura(
            estado="fallo", codigo_motivo="error_interno_captura"
        )
        contexto.capture_batch = None
        contexto.estado_captura = estado_falla
        _registrar_evento(
            contexto,
            tipo="error",
            codigo="error_interno_captura",
            evidencia=str(exc),
        )
        return ResultadoCaptura(estado="ok", contexto=contexto)

    res, _ = ejecutar_con_reintento(
        lambda: adapter.capture_batch(
            page=contexto.handle_sesion,
            ficha=fuente,
            set_filtros=set_actual,
            politicas=politicas,
        ),
        al_fallo_final=_fallo_captura,
        al_error_interno=_fallo_interno,
        contexto_log=contexto.id_corrida,
    )
    if isinstance(res, ResultadoCaptura):
        return res
    lote, estado = res

    # Paso 4: éxito de captura
    contexto.capture_batch = lote
    contexto.estado_captura = estado
    _registrar_evento(
        contexto,
        tipo="suceso",
        codigo="captura_completada",
        evidencia=(
            f"páginas={estado.paginas_consumidas} | "
            f"ofertas={len(lote.ofertas)} | "
            f"duracion_s={int(monotonic() - inicio_captura)}"
        ),
    )

    # Paso 5: auditoría de sesión (no aborta si falla la escritura)
    _escribir_auditoria_sesion(contexto, lote)

    return ResultadoCaptura(estado="ok", contexto=contexto)


def _escribir_auditoria_sesion(contexto: RunContext, lote: CaptureBatch) -> None:
    """Escribe la auditoría en la tabla `sesiones`; reintenta una vez."""
    id_sesion = contexto.id_sesion or ""
    total_declarado = (
        contexto.search_result.total_declarado
        if contexto.search_result is not None
        else None
    )
    indice_set = lote.indice_set
    datos = {
        "id": id_sesion,
        "id_sesion": id_sesion,
        "id_corrida": contexto.id_corrida,
        "fuente_id": (
            contexto.fuente_corriente.fuente_id
            if contexto.fuente_corriente
            else ""
        ),
        "indice_set": indice_set if indice_set is not None else None,
        "marca_temporal": ahora(),
        "total_declarado": total_declarado,
        "conteo": len(lote.ofertas),
        "estado": "completa",
    }
    intentos = 2
    for intento in range(1, intentos + 1):
        try:
            AuditoriaSesion.model_validate(datos)
            escribir_fila("sesiones", datos)
            return
        except Exception as exc:
            logger.error(
                f"[{contexto.id_corrida}] Auditoría de sesión fallida "
                f"(intento {intento}/{intentos}): {exc}"
            )
    logger.error(f"[{contexto.id_corrida}] Auditoría de sesión no persistida.")


def registrar_ofertas(contexto: RunContext) -> ResultadoCaptura:
    """Nodo: Registrar ofertas en Ofertas Totales (v1.0).

    Deduplica por `id_externo` vía `upsert_lote_ofertas` (una conexión y un
    reintento único para el lote completo). Si todas fallan, registra un
    evento crítico de lote degradado; el flujo siempre continúa.
    """
    lote = contexto.capture_batch
    if lote is None or not lote.ofertas:
        return ResultadoCaptura(estado="ok", contexto=contexto)

    filas = [_oferta_a_dict(oferta, contexto) for oferta in lote.ofertas]
    registradas, fallidas = _registrar_lote_con_reintento(filas)

    if registradas > 0:
        _registrar_evento(
            contexto,
            tipo="suceso",
            codigo="ofertas_registradas",
            evidencia=(
                f"ofertas registradas: {registradas} | "
                f"total: {len(lote.ofertas)}"
            ),
        )

    if fallidas > 0 and registradas == 0:
        _registrar_evento(
            contexto,
            tipo="error",
            codigo="lote_degradado",
            evidencia=(
                f"Lote degradado: {fallidas} ofertas fallidas de "
                f"{len(lote.ofertas)} en el set."
            ),
        )
    elif fallidas > 0:
        _registrar_evento(
            contexto,
            tipo="error",
            codigo="registro_parcial",
            evidencia=(
                f"Registro parcial: {registradas} registradas, "
                f"{fallidas} fallidas de {len(lote.ofertas)}."
            ),
        )

    return ResultadoCaptura(estado="ok", contexto=contexto)


def _oferta_a_dict(oferta: Offer, contexto: RunContext) -> dict[str, Any]:
    """Construye el dict de la fila `ofertas` desde una oferta capturada.

    `empresa_id`/`ubicacion_id` se guardan como NULL (catálogos no poblados
    en el MVP, D29) y `fuente_id` conserva su fuente_id.
    """
    return {
        "titulo": oferta.titulo,
        "descripcion_original": oferta.descripcion_original,
        "empresa_id": None,
        "ubicacion_id": None,
        "enlace": oferta.enlace,
        "fuente_id": oferta.fuente_id,
        "indice_set": oferta.indice_set,
        "id_externo": oferta.id_externo,
        "fecha_publicacion": (
            oferta.fecha_publicacion.strftime(FORMATO_TIMESTAMP)
            if oferta.fecha_publicacion
            else None
        ),
        "observaciones": oferta.observaciones or "",
        "id_corrida": contexto.id_corrida,
        "id_sesion": contexto.id_sesion,
        "fecha_descubrimiento": ahora(),
    }


def _registrar_lote_con_reintento(
    filas: list[dict[str, Any]],
) -> tuple[int, int]:
    """Registra el lote completo en una conexión; reintenta una vez si falla.

    Returns (registradas, fallidas).
    """
    for intento in range(1, 3):
        try:
            return upsert_lote_ofertas(filas)
        except Exception as exc:
            logger.error(
                f"Fallo registrando lote de ofertas (intento {intento}/2): {exc}"
            )
    return 0, len(filas)


def quedan_sets_por_aplicar(contexto: RunContext) -> ResultadoCaptura:
    """Decisión: ¿Quedan sets de filtros por aplicar? (v1.0).

    Calcula los sets pendientes SIN avanzar el iterador.
    """
    fuente = contexto.fuente_corriente
    if fuente is None:
        logger.error(f"ERR-01: fuente_corriente ausente en corrida {contexto.id_corrida}")
        return ResultadoCaptura(
            estado="error", codigo="ERR-01", descripcion="Fuente ausente"
        )
    total_sets = len(contexto.sets_validos(fuente))
    iterador_actual = contexto.iterador_sets.get(fuente.fuente_id, -1)
    sets_pendientes = total_sets - (iterador_actual + 1)
    decision = "si" if sets_pendientes > 0 else "no"
    return ResultadoCaptura(estado="ok", decision=decision, contexto=contexto)
