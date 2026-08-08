"""Unit tests for the source control nodes (sub-phase 4.1, Discovery module)."""

from pathlib import Path
from typing import Any

from modules.discovery.nodes.control_fuentes import (
    existen_fuentes_configuradas,
    quedan_fuentes_por_procesar,
    seleccionar_fuente_pendiente,
)
from modules.discovery.run_context import RunContext

CONFIG_CAPTURA = {
    "max_paginas": 5,
    "max_ofertas_por_corrida": 25,
    "pausa_entre_lotes_segundos": 10,
}

FUENTE_LINKEDIN: dict[str, Any] = {
    "source_id": "linkedin",
    "nombre": "LinkedIn",
    "ficha_acceso": {
        "url": "https://www.linkedin.com/jobs/search",
        "tipo_acceso": "con_autenticacion",
        "credenciales_referencia": ["LINKEDIN_EMAIL", "LINKEDIN_PASSWORD"],
        "criterio_exito": "global-nav",
        "timeout_segundos": 30,
    },
    "sets_de_filtros": [
        {"set_indice": 0, "filtros": [{"tipo": "keywords", "valor": ["Data Engineer"]}]}
    ],
    "politicas_de_captura": {
        "max_paginas": 2,
        "max_ofertas_por_corrida": 10,
        "pausa_entre_lotes_segundos": 1,
    },
}

FUENTE_COMPUTRABAJO: dict[str, Any] = {
    "source_id": "computrabajo",
    "nombre": "Computrabajo",
    "ficha_acceso": {
        "url": "https://www.computrabajo.com.pe/empleos",
        "tipo_acceso": "publico",
        "criterio_exito": "ofertas",
        "timeout_segundos": 30,
    },
    "sets_de_filtros": [{"set_indice": 0, "filtros": []}],
    "politicas_de_captura": {
        "max_paginas": 2,
        "max_ofertas_por_corrida": 10,
        "pausa_entre_lotes_segundos": 1,
    },
}


def _contexto(
    fuentes: list[dict[str, Any]] | None = None,
    run_id: str = "COR-9001",
) -> RunContext:
    lista = fuentes if fuentes is not None else [dict(FUENTE_LINKEDIN)]
    return RunContext(
        config_fuentes=lista,
        config_captura=dict(CONFIG_CAPTURA),
        run_id=run_id,
        permitir_vacio=True,
    )


# --- Nodo 1: existencia ---


def test_existen_fuentes_rama_si() -> None:
    res = existen_fuentes_configuradas(_contexto())
    assert res.estado == "ok"
    assert res.decision == "si"


def test_existen_fuentes_rama_no_motivo_sin_fuentes() -> None:
    contexto = _contexto(fuentes=[])
    res = existen_fuentes_configuradas(contexto)
    assert res.estado == "ok"
    assert res.decision == "no"
    assert contexto.motivo_terminacion == "sin_fuentes"
    assert contexto.timestamp_terminacion != ""


def test_existen_fuentes_contexto_corrupto_aborta(temp_db_file: Path) -> None:
    res = existen_fuentes_configuradas(None)
    assert res.estado == "error"
    assert res.codigo == "ERR-01"


# --- Nodo 2: iteración ---


def test_quedan_fuentes_iterador_ninguna_rama_si() -> None:
    contexto = _contexto(fuentes=[FUENTE_LINKEDIN, FUENTE_COMPUTRABAJO])
    contexto.iterador_fuentes = -1
    res = quedan_fuentes_por_procesar(contexto)
    assert res.estado == "ok"
    assert res.decision == "si"


def test_quedan_fuentes_todas_procesadas_rama_no() -> None:
    contexto = _contexto(fuentes=[FUENTE_LINKEDIN, FUENTE_COMPUTRABAJO])
    contexto.iterador_fuentes = 1
    res = quedan_fuentes_por_procesar(contexto)
    assert res.estado == "ok"
    assert res.decision == "no"
    assert contexto.motivo_terminacion == "corrida_completada"
    assert contexto.timestamp_terminacion != ""


def test_quedan_fuentes_iterador_corrupto_aborta(temp_db_file: Path) -> None:
    contexto = _contexto()
    setattr(contexto, "iterador_fuentes", None)
    res = quedan_fuentes_por_procesar(contexto)
    assert res.estado == "error"
    assert res.codigo == "ERR-01"


# --- Nodo 3: selección ---


def test_seleccionar_primera_pendiente_y_marcar_procesada() -> None:
    contexto = _contexto(fuentes=[FUENTE_LINKEDIN, FUENTE_COMPUTRABAJO])
    res = seleccionar_fuente_pendiente(contexto)
    assert res.estado == "ok"
    assert contexto.iterador_fuentes == 0
    assert contexto.posicion_fuente_corriente == 0
    assert contexto.fuente_corriente is not None
    assert contexto.fuente_corriente.source_id == "linkedin"


def test_fuente_corriente_expone_parametros_completos() -> None:
    contexto = _contexto()
    seleccionar_fuente_pendiente(contexto)
    assert contexto.fuente_corriente is not None
    ficha = contexto.fuente_corriente
    assert ficha.source_id == "linkedin"
    assert ficha.url == "https://www.linkedin.com/jobs/search"
    assert ficha.tipo_acceso == "con_autenticacion"
    assert ficha.credenciales_referencia == [
        "LINKEDIN_EMAIL",
        "LINKEDIN_PASSWORD",
    ]
    assert ficha.criterio_exito == "global-nav"
    assert ficha.timeout_segundos == 30
    assert len(contexto.sets_validos(ficha)) == 1


def test_seleccionar_sin_pendiente_pese_contrato_aborta(
    temp_db_file: Path,
) -> None:
    contexto = _contexto()
    contexto.iterador_fuentes = 0
    res = seleccionar_fuente_pendiente(contexto)
    assert res.estado == "error"
    assert res.codigo == "ERR-02"


def test_seleccionar_iterador_fuera_de_rango_aborta() -> None:
    contexto = _contexto()
    contexto.iterador_fuentes = 99
    res = seleccionar_fuente_pendiente(contexto)
    assert res.estado == "error"
    assert res.codigo == "ERR-01"


def test_seleccionar_iterador_corrupto_aborta(temp_db_file: Path) -> None:
    contexto = _contexto()
    setattr(contexto, "iterador_fuentes", None)
    res = seleccionar_fuente_pendiente(contexto)
    assert res.estado == "error"
    assert res.codigo == "ERR-01"


def test_seleccionar_fallo_mutacion_aborta(temp_db_file: Path) -> None:
    class _ContextoRoto(RunContext):
        def __setattr__(self, name: str, value: Any) -> None:
            if name == "iterador_fuentes" and value != -1:
                raise RuntimeError("mutacion forzada")
            super().__setattr__(name, value)

    contexto_roto = _ContextoRoto(
        config_fuentes=[dict(FUENTE_LINKEDIN)],
        config_captura=dict(CONFIG_CAPTURA),
        run_id="COR-ROTO",
        permitir_vacio=True,
    )
    res = seleccionar_fuente_pendiente(contexto_roto)
    assert res.estado == "error"
    assert res.codigo == "ERR-03"


def test_seleccionar_no_reselecta_fuente_procesada() -> None:
    contexto = _contexto(fuentes=[FUENTE_LINKEDIN, FUENTE_COMPUTRABAJO])
    seleccionar_fuente_pendiente(contexto)
    seleccionar_fuente_pendiente(contexto)
    assert contexto.fuente_corriente is not None
    assert contexto.fuente_corriente.source_id == "computrabajo"
    assert contexto.iterador_fuentes == 1
