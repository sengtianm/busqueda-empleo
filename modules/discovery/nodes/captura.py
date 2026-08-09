"""Nodos de captura y registro de ofertas (Sub-fase 4.4).

Cubre los nodos "Capturar ofertas", "Registrar ofertas en Ofertas Totales",
"¿Quedan ofertas por capturar?" y "¿Quedan sets de filtros por aplicar?"
(DOC-04 Section 15). El adaptador resuelve toda la paginación internamente
(RN-10), por lo que el bucle interno de captura se ejecuta una sola vez por
set; la deduplicación se hace por `id_externo_url`.
"""

import time
from dataclasses import dataclass
from typing import Any

from loguru import logger

from modules.discovery.adapters.linkedin import FlowError, LinkedInAdapter
from modules.discovery.run_context import RunContext, _ahora
from shared.config import load
from shared.models import CaptureBatch, EstadoCaptura, Offer
from shared.persistence import upsert_oferta, write_evento, write_row
from shared.retry import should_retry


@dataclass
class ResultadoCaptura:
    estado: str  # "ok" | "error"
    decision: str = ""  # "si" | "no" (solo nodos de decisión)
    contexto: RunContext | None = None
    codigo: str = ""
    descripcion: str = ""


def _config_reintentos() -> tuple[int, float, float, float]:
    cfg_retries = load().get("retries", {})
    return (
        int(cfg_retries.get("max_attempts", 3)),
        float(cfg_retries.get("base_wait_seconds", 2)),
        float(cfg_retries.get("multiplier", 2)),
        float(cfg_retries.get("max_wait_seconds", 30)),
    )


def _registrar_evento(
    contexto: RunContext,
    tipo: str,
    codigo: str,
    evidencia: str,
) -> None:
    """Escribe un evento en la tabla `eventos` sin abortar el flujo."""
    try:
        write_evento(
            {
                "run_id": contexto.run_id,
                "source_id": (
                    contexto.fuente_corriente.source_id
                    if contexto.fuente_corriente
                    else ""
                ),
                "session_id": contexto.session_id,
                "set_indice": (
                    contexto.set_corriente.indice
                    if contexto.set_corriente
                    else None
                ),
                "timestamp": _ahora(),
                "tipo": tipo,
                "codigo": codigo,
                "evidencia": evidencia,
            }
        )
    except Exception as exc:
        logger.error(
            f"[{contexto.run_id}] Failed to write event to DB: {exc} | "
            f"codigo={codigo}"
        )


def capturar_ofertas(contexto: RunContext) -> ResultadoCaptura:
    """Nodo: Capturar ofertas (v1.0).

    Invoca al adaptador UNA SOLA VEZ con reintento condicional
    (máximo 3 intentos totales, solo códigos reintentables como
    `timeout_captura`). En éxito guarda los resultados en el contexto y
    escribe la auditoría de sesión; en fallo descarta el set completo
    (las ofertas parciales) y continúa con el siguiente set.
    """
    # Paso 1: verificar insumos
    if contexto.handle_sesion is None:
        logger.error(f"ERR-01: handle_sesion ausente en corrida {contexto.run_id}")
        return ResultadoCaptura(
            estado="error", codigo="ERR-01", descripcion="Insumos ausentes"
        )
    fuente = contexto.fuente_corriente
    if fuente is None:
        logger.error(f"ERR-01: fuente_corriente ausente en corrida {contexto.run_id}")
        return ResultadoCaptura(
            estado="error", codigo="ERR-01", descripcion="Fuente ausente"
        )
    set_actual = contexto.set_corriente
    if set_actual is None:
        logger.error(f"ERR-01: set_corriente ausente en corrida {contexto.run_id}")
        return ResultadoCaptura(
            estado="error", codigo="ERR-01", descripcion="Set ausente"
        )

    # Paso 2: obtener políticas
    politicas = contexto.politicas(fuente)

    # Paso 3: ejecutar captura con reintento condicional
    adapter = LinkedInAdapter()
    max_attempts, base_wait, multiplier, max_wait = _config_reintentos()

    attempt = 0
    while attempt < max_attempts:
        attempt += 1
        try:
            lote, estado = adapter.capture_batch(
                page=contexto.handle_sesion,
                ficha=fuente,
                set_filtros=set_actual,
                politicas=politicas,
            )
        except FlowError as fe:
            if should_retry(fe.codigo_motivo) and attempt < max_attempts:
                logger.warning(
                    f"[{contexto.run_id}] Captura reintentable "
                    f"({fe.codigo_motivo}), intento {attempt}/{max_attempts}"
                )
                wait_time = min(
                    base_wait * (multiplier ** (attempt - 1)), max_wait
                )
                time.sleep(wait_time)
                continue
            # Paso 6: fallo definitivo (no reintentable o intentos agotados)
            estado_fallo = EstadoCaptura(estado="fallo", codigo_motivo=fe.codigo_motivo)
            contexto.capture_batch = None
            contexto.estado_captura = estado_fallo
            _registrar_evento(
                contexto,
                tipo="error",
                codigo=fe.codigo_motivo,
                evidencia=fe.mensaje,
            )
            return ResultadoCaptura(estado="ok", contexto=contexto)
        except Exception as exc:
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

        # Paso 4: éxito de captura
        contexto.capture_batch = lote
        contexto.estado_captura = estado
        contexto.paginas_consumidas = estado.paginas_consumidas
        contexto.capturadas_acumuladas_fuente = estado.capturadas_acumuladas_fuente
        contexto.limite_alcanzado = estado.limite_alcanzado

        # Paso 5: auditoría de sesión (no aborta si falla la escritura)
        _escribir_auditoria_sesion(contexto, lote)

        return ResultadoCaptura(estado="ok", contexto=contexto)

    return ResultadoCaptura(
        estado="error", codigo="ERR-09", descripcion="Sin intentos configurados"
    )


def _escribir_auditoria_sesion(contexto: RunContext, lote: CaptureBatch) -> None:
    """Escribe la auditoría en la tabla `sesiones`; reintenta una vez."""
    session_id = contexto.session_id or ""
    total_declarado = (
        contexto.search_result.total_declarado
        if contexto.search_result is not None
        else None
    )
    set_indice = lote.set_indice
    datos = {
        "session_id": session_id,
        "run_id": contexto.run_id,
        "source_id": (
            contexto.fuente_corriente.source_id
            if contexto.fuente_corriente
            else ""
        ),
        "set_indice": set_indice if set_indice is not None else None,
        "timestamp": _ahora(),
        "total_declarado": total_declarado,
        "conteo": len(lote.ofertas),
        "estado": "completa",
    }
    intentos = 2
    for intento in range(1, intentos + 1):
        try:
            write_row("sesiones", datos)
            return
        except Exception as exc:
            logger.error(
                f"[{contexto.run_id}] Auditoría de sesión fallida "
                f"(intento {intento}/{intentos}): {exc}"
            )
    logger.error(f"[{contexto.run_id}] Auditoría de sesión no persistida.")


def registrar_ofertas(contexto: RunContext) -> ResultadoCaptura:
    """Nodo: Registrar ofertas en Ofertas Totales (v1.0).

    Deduplica por `id_externo_url` vía `upsert_oferta` (reintento único por
    oferta). Si todas fallan, registra un evento crítico de lote degradado;
    el flujo siempre continúa.
    """
    lote = contexto.capture_batch
    if lote is None or not lote.ofertas:
        return ResultadoCaptura(estado="ok", contexto=contexto)

    registradas = 0
    fallidas = 0
    for oferta in lote.ofertas:
        fila = _oferta_a_dict(oferta, contexto)
        if _registrar_oferta_con_reintento(fila):
            registradas += 1
        else:
            fallidas += 1

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

    `empresa_id`/`ubicacion_id` se guardan como NULL (los catálogos aún no
    existen en el MVP); el string del adaptador se conserva en las columnas
    `empresa_nombre`/`ubicacion_nombre` y `fuente_id` conserva su source_id.
    """
    return {
        "titulo": oferta.titulo,
        "descripcion_original": oferta.descripcion_original,
        "empresa_id": None,
        "ubicacion_id": None,
        "empresa_nombre": oferta.empresa_id,
        "ubicacion_nombre": oferta.ubicacion_id,
        "url": oferta.url,
        "fuente_id": oferta.fuente_id,
        "set_indice": oferta.set_indice,
        "id_externo_url": oferta.id_externo_url,
        "run_id": contexto.run_id,
        "session_id": contexto.session_id,
        "discovery_date": _ahora(),
    }


def _registrar_oferta_con_reintento(fila: dict[str, Any]) -> bool:
    """Inserta o actualiza una oferta; reintenta una vez si falla."""
    for intento in range(1, 3):
        try:
            upsert_oferta(fila)
            return True
        except Exception as exc:
            logger.error(
                f"Fallo registrando oferta (intento {intento}/2): {exc}"
            )
    return False


def quedan_ofertas_por_capturar(contexto: RunContext) -> ResultadoCaptura:
    """Nodo de decisión: ¿Quedan ofertas por capturar? (v1.0).

    Con la arquitectura actual el adaptador ya resolvió toda la paginación,
    por lo que siempre responde `no` (tras captura exitosa o fallida).
    """
    if contexto.estado_captura is None:
        logger.error(f"ERR-01: estado_captura ausente en corrida {contexto.run_id}")
        return ResultadoCaptura(
            estado="error",
            codigo="ERR-01",
            descripcion="estado_captura ausente",
        )
    return ResultadoCaptura(estado="ok", decision="no", contexto=contexto)


def quedan_sets_por_aplicar(contexto: RunContext) -> ResultadoCaptura:
    """Decisión: ¿Quedan sets de filtros por aplicar? (v1.0).

    Calcula los sets pendientes SIN avanzar el iterador.
    """
    fuente = contexto.fuente_corriente
    if fuente is None:
        logger.error(f"ERR-01: fuente_corriente ausente en corrida {contexto.run_id}")
        return ResultadoCaptura(
            estado="error", codigo="ERR-01", descripcion="Fuente ausente"
        )
    total_sets = len(contexto.sets_validos(fuente))
    iterador_actual = contexto.iterador_sets.get(fuente.source_id, -1)
    sets_pendientes = total_sets - (iterador_actual + 1)
    decision = "si" if sets_pendientes > 0 else "no"
    return ResultadoCaptura(estado="ok", decision=decision, contexto=contexto)
