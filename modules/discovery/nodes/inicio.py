"""INICIO node of the Discovery flow (technical sheet v1.3, Section 1).

Instantiates the run (run_id with a single retry), loads and validates the
global configuration (VAL-02), verifies the database with a rolled-back write
probe (VAL-03), resolves the concurrency lock (VAL-04), filters structurally
valid sources discarding incomplete sheets with an ERR-12 event (VAL-06),
initializes the run state and registers the run row, then delivers a complete
RunContext (VAL-05). This node never touches job sources, filters, offers,
the credential store or runtime validations (RN-05, RN-09).

Definitions (section 1.11): abort = immediate termination on unrecoverable
failure; controlled termination = finishing without processing (concurrency);
discard = excluding a source from the iteration without stopping the run.
Errors ERR-01..ERR-04 and ERR-11 are logged only with Loguru (DB not
connected yet); events that can reach the `eventos` table fall back to Loguru
when the database is unavailable.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any

import yaml
from loguru import logger

from modules.discovery.run_context import RunContext
from shared.config import load
from shared.persistence import (
    acquire_lock,
    check_lock,
    generate_id,
    init_db,
    probe_write,
    umbral_obsolescencia_minutos,
    write_corrida,
    write_evento,
)

_FORMATO_TIMESTAMP = "%Y-%m-%d %H:%M:%S"
_TIPOS_ACCESO = ("publico", "con_autenticacion")
_ESTRATEGIAS_ANTI_BLOQUEO = ("pausa_aleatoria", "retraso_fijo", "none")
_RANGOS_POLITICAS: dict[str, int] = {
    "max_paginas": 1,
    "max_ofertas_por_corrida": 1,
    "pausa_entre_lotes_segundos": 0,
}


@dataclass
class ResultadoInicio:
    """Outcome of the INICIO node handed to the orchestrator."""

    estado: str
    run_id: str = ""
    contexto: RunContext | None = None
    codigo: str = ""
    motivo: str = ""
    descripcion: str = ""


def _ahora() -> str:
    return datetime.now().strftime(_FORMATO_TIMESTAMP)


def _generar_run_id() -> str:
    for intento in (1, 2):
        try:
            return generate_id("corridas")
        except Exception:
            if intento == 2:
                raise
    raise RuntimeError("unreachable")  # pragma: no cover


def _es_obsoleto(timestamp: datetime, umbral_minutos: int) -> bool:
    """Mirrors `shared.persistence.acquire_lock` staleness semantics."""
    if umbral_minutos <= 0:
        return False
    antiguedad = (datetime.now() - timestamp).total_seconds() / 60
    return antiguedad >= umbral_minutos


def _registrar_evento(
    run_id: str,
    tipo: str,
    codigo: str,
    evidencia: str,
    source_id: str = "",
) -> None:
    try:
        write_evento(
            {
                "run_id": run_id,
                "source_id": source_id,
                "tipo": tipo,
                "codigo": codigo,
                "evidencia": evidencia,
                "timestamp": _ahora(),
            }
        )
    except Exception as exc:
        logger.error(f"Evento no persistible | run={run_id} | {codigo} | {exc}")


def _validar_fuente(conf: Any) -> str | None:
    """RN-08 sheet validation; returns an explanation or None when valid."""
    if not isinstance(conf, dict):
        return "la fuente no es un objeto"
    source_id = conf.get("source_id")
    if not isinstance(source_id, str) or not source_id.strip():
        return "source_id ausente o invalido"
    nombre = conf.get("nombre")
    if not isinstance(nombre, str) or not nombre.strip():
        return "nombre ausente o invalido"
    ficha = conf.get("ficha_acceso")
    if not isinstance(ficha, dict):
        return "ficha_acceso ausente o invalida"
    url = ficha.get("url")
    if not isinstance(url, str) or not url.strip():
        return "url ausente"
    tipo = ficha.get("tipo_acceso")
    if tipo not in _TIPOS_ACCESO:
        return "tipo_acceso invalido"
    credenciales = ficha.get("credenciales_referencia")
    if tipo == "con_autenticacion" and (
        not isinstance(credenciales, list) or not credenciales
    ):
        return "credenciales_referencia ausente"
    criterio = ficha.get("criterio_exito")
    if not isinstance(criterio, str) or not criterio:
        return "criterio_exito ausente"
    timeout = ficha.get("timeout_segundos")
    if not isinstance(timeout, int) or timeout < 1:
        return "timeout_segundos invalido"
    sets = conf.get("sets_de_filtros")
    if not isinstance(sets, list) or not sets:
        return "sets_de_filtros vacio o ausente"
    for s in sets:
        if not isinstance(s, dict):
            return "set de filtros invalido"
        if not isinstance(s.get("set_indice"), int):
            return "set sin set_indice valido"
        if not isinstance(s.get("filtros"), list):
            return "filtros del set invalidos"
    politicas = conf.get("politicas_de_captura")
    if politicas is not None:
        if not isinstance(politicas, dict):
            return "politicas_de_captura invalida"
        for clave, minimo in _RANGOS_POLITICAS.items():
            if clave not in politicas:
                continue
            valor = politicas[clave]
            if not isinstance(valor, int) or valor < minimo:
                return f"politica {clave} fuera de rango (minimo {minimo})"
        estrategia = politicas.get("estrategia_anti_bloqueo")
        if estrategia is not None and estrategia not in _ESTRATEGIAS_ANTI_BLOQUEO:
            return "estrategia_anti_bloqueo fuera del conjunto definido"
    return None


def ejecutar_inicio(config: dict[str, Any] | None = None) -> ResultadoInicio:
    """Run the INICIO node steps in order (section 2 of the sheet)."""
    try:
        run_id = _generar_run_id()
    except Exception as exc:
        logger.error(f"ERR-01 | run_id generado dos veces con fallo | {exc}")
        return ResultadoInicio(
            estado="error",
            codigo="ERR-01",
            descripcion="run_id generation failed after a single retry",
        )

    try:
        if config is None:
            config = load()
        if not isinstance(config, dict):
            raise ValueError("configuration root is not a mapping")
        if "fuentes" not in config or not isinstance(config["fuentes"], list):
            raise ValueError("'fuentes' key missing or not a list")
    except FileNotFoundError:
        logger.error(f"ERR-02 | run={run_id} | configuration file missing")
        return ResultadoInicio(
            estado="error",
            run_id=run_id,
            codigo="ERR-02",
            descripcion="configuration file missing",
        )
    except OSError:
        logger.error(f"ERR-03 | run={run_id} | configuration file unreadable")
        return ResultadoInicio(
            estado="error",
            run_id=run_id,
            codigo="ERR-03",
            descripcion="configuration file unreadable",
        )
    except (ValueError, yaml.YAMLError):
        logger.error(f"ERR-04 | run={run_id} | configuration corrupt or inconsistent")
        return ResultadoInicio(
            estado="error",
            run_id=run_id,
            codigo="ERR-04",
            descripcion="configuration corrupt or inconsistent structure",
        )

    fuentes = config["fuentes"]
    ids = [str(c.get("source_id", "")) for c in fuentes if isinstance(c, dict)]
    duplicados = sorted({i for i in ids if ids.count(i) > 1}) if ids else []
    if duplicados:
        logger.error(f"ERR-11 | run={run_id} | duplicate source_ids: {duplicados}")
        return ResultadoInicio(
            estado="error",
            run_id=run_id,
            codigo="ERR-11",
            descripcion=f"duplicate source_id(s) {duplicados}",
        )

    try:
        init_db()
        probe_write()
    except Exception as error:
        _registrar_evento(run_id, "error", "ERR-05", f"base de datos no disponible: {error}")
        logger.error(f"ERR-05 | run={run_id} | database unavailable | {error}")
        return ResultadoInicio(
            estado="error",
            run_id=run_id,
            codigo="ERR-05",
            descripcion="database unavailable or not writable",
        )

    try:
        bloqueo_actual = check_lock()
    except Exception as error:
        _registrar_evento(run_id, "error", "ERR-08", f"estado de bloqueo no decidible: {error}")
        logger.error(f"ERR-08 | run={run_id} | lock state undecidable | {error}")
        return ResultadoInicio(
            estado="error",
            run_id=run_id,
            codigo="ERR-08",
            descripcion="lock state undecidable",
        )

    timestamp = _ahora()
    if bloqueo_actual is not None:
        try:
            fecha_bloqueo = datetime.strptime(
                str(bloqueo_actual.get("timestamp", "")), _FORMATO_TIMESTAMP
            )
        except (TypeError, ValueError):
            _registrar_evento(run_id, "error", "ERR-08", "timestamp del bloqueo no valido")
            return ResultadoInicio(
                estado="error",
                run_id=run_id,
                codigo="ERR-08",
                descripcion="lock timestamp undecidable",
            )
        if not _es_obsoleto(fecha_bloqueo, umbral_obsolescencia_minutos(config)):
            _registrar_evento(
                run_id,
                "suceso",
                "ERR-06",
                f"corrida {bloqueo_actual.get('run_id', '')} activa; terminacion por concurrencia",
            )
            return ResultadoInicio(
                estado="concurrencia",
                run_id=run_id,
                codigo="ERR-06",
                motivo="concurrencia",
                descripcion="another run is active (lock not stale)",
            )
        try:
            adquirido = acquire_lock(run_id, timestamp, forzar=True)
        except Exception as error:
            _registrar_evento(run_id, "error", "ERR-08", f"fallo al sobrescribir: {error}")
            return ResultadoInicio(
                estado="error",
                run_id=run_id,
                codigo="ERR-08",
                descripcion="lock overwrite failed (undecidable state)",
            )
        if not adquirido:
            _registrar_evento(
                run_id,
                "suceso",
                "ERR-06",
                "contienda de adquisicion al sobrescribir: otro proceso gano el bloqueo",
            )
            return ResultadoInicio(
                estado="concurrencia",
                run_id=run_id,
                codigo="ERR-06",
                motivo="concurrencia",
                descripcion="lock contention at stale overwrite",
            )
        _registrar_evento(
            run_id,
            "suceso",
            "ERR-07",
            f"bloqueo obsoleto de {bloqueo_actual.get('run_id', '')} sobrescrito",
        )
    else:
        try:
            adquirido = acquire_lock(run_id, timestamp)
        except Exception as error:
            _registrar_evento(run_id, "error", "ERR-08", f"fallo al adquirir: {error}")
            return ResultadoInicio(
                estado="error",
                run_id=run_id,
                codigo="ERR-08",
                descripcion="lock acquisition failed (undecidable state)",
            )
        if not adquirido:
            _registrar_evento(
                run_id,
                "suceso",
                "ERR-06",
                "contienda de adquisicion: otro proceso gano el bloqueo",
            )
            return ResultadoInicio(
                estado="concurrencia",
                run_id=run_id,
                codigo="ERR-06",
                motivo="concurrencia",
                descripcion="lock contention race at acquisition",
            )

    validas: list[dict[str, Any]] = []
    for raw in fuentes:
        problema = _validar_fuente(raw)
        if problema is not None:
            source_id = str(raw.get("source_id", "")) if isinstance(raw, dict) else ""
            _registrar_evento(
                run_id,
                "error",
                "ERR-12",
                f"ficha incompleta: {problema}",
                source_id=source_id,
            )
            logger.warning(f"ERR-12 | run={run_id} | source={source_id} discarded | {problema}")
            continue
        validas.append(raw)

    try:
        contexto = RunContext(
            config_fuentes=validas,
            config_captura=config.get("captura") or {},
            run_id=run_id,
            permitir_vacio=True,
        )
        contexto.bloqueo_adquirido = True
        write_corrida(
            {
                "run_id": run_id,
                "timestamp_inicio": contexto.timestamp_inicio,
                "estado": "en_ejecucion",
            }
        )
    except Exception as error:
        _registrar_evento(
            run_id,
            "error",
            "ERR-10",
            f"Fallo interno de inicializacion de estado: {error}",
        )
        logger.error(f"ERR-10 | run={run_id} | internal initialization failure | {error}")
        return ResultadoInicio(
            estado="error",
            run_id=run_id,
            codigo="ERR-10",
            descripcion="internal run state initialization failure",
        )

    if not (contexto.run_id == run_id and contexto.bloqueo_adquirido):
        _registrar_evento(run_id, "error", "ERR-10", "contexto incompleto al entregar control")
        return ResultadoInicio(
            estado="error",
            run_id=run_id,
            codigo="ERR-10",
            descripcion="incomplete context before handover (VAL-05)",
        )

    return ResultadoInicio(estado="ok", run_id=run_id, contexto=contexto)
