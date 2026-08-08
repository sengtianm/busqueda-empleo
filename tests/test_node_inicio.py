"""Unit tests for the INICIO node (sub-phase 4.1, Discovery module)."""

import datetime
from pathlib import Path
from typing import Any

import yaml

from modules.discovery.nodes.inicio import ejecutar_inicio
from modules.discovery.run_context import RunContext
from shared.errors import PersistenceError
from shared.persistence import (
    acquire_lock,
    check_lock,
    read_table,
    release_lock,
)

CONFIG_BASE = {
    "captura": {
        "max_paginas": 5,
        "max_ofertas_por_corrida": 25,
        "pausa_entre_lotes_segundos": 10,
    },
    "concurrencia": {"umbral_obsolescencia_minutos": 120},
}

FUENTE_VALIDA: dict[str, Any] = {
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
        {"set_indice": 0, "filtros": [{"tipo": "keywords", "valor": ["Data Engineer"]}]},
        {"set_indice": 1, "filtros": []},
    ],
    "politicas_de_captura": {
        "max_paginas": 2,
        "max_ofertas_por_corrida": 10,
        "pausa_entre_lotes_segundos": 1,
    },
}

CONFIG_UNA_FUENTE: dict[str, Any] = {
    **CONFIG_BASE,
    "fuentes": [FUENTE_VALIDA],
}


def _marca(momento: datetime.datetime) -> str:
    return momento.strftime("%Y-%m-%d %H:%M:%S")


def test_inicio_ok_corrida_registrada_y_bloqueo(temp_db_file: Path) -> None:
    res = ejecutar_inicio(dict(CONFIG_UNA_FUENTE))
    assert res.estado == "ok"
    assert res.run_id.startswith("COR-")
    assert isinstance(res.contexto, RunContext)
    assert res.contexto.run_id == res.run_id
    assert res.contexto.bloqueo_adquirido is True
    corridas = read_table("corridas")
    assert any(
        c["run_id"] == res.run_id and c["estado"] == "en_ejecucion"
        for c in corridas
    )
    bloqueo = check_lock()
    assert bloqueo is not None
    assert bloqueo["run_id"] == res.run_id


def test_inicio_config_sin_fuentes_no_es_error(temp_db_file: Path) -> None:
    res = ejecutar_inicio({**CONFIG_BASE, "fuentes": []})
    assert res.estado == "ok"
    assert res.contexto is not None
    assert res.contexto.fuentes_filtradas == []


def test_inicio_descarta_fuente_incompleta_con_evento(temp_db_file: Path) -> None:
    incompleta: dict[str, Any] = {
        "source_id": "rotosource",
        "nombre": "Roto",
        "ficha_acceso": {"tipo_acceso": "publico"},
    }
    config = {
        **CONFIG_BASE,
        "fuentes": [dict(FUENTE_VALIDA), incompleta],
    }
    res = ejecutar_inicio(config)
    assert res.estado == "ok"
    assert res.contexto is not None
    assert [f.source_id for f in res.contexto.fuentes_filtradas] == ["linkedin"]
    eventos = read_table("eventos")
    assert any(
        e["codigo"] == "ERR-12" and e["source_id"] == "rotosource"
        for e in eventos
    )


def test_inicio_aborta_source_id_duplicados(temp_db_file: Path) -> None:
    duplicada = {**FUENTE_VALIDA, "nombre": "LinkedIn Clon"}
    res = ejecutar_inicio({**CONFIG_BASE, "fuentes": [FUENTE_VALIDA, duplicada]})
    assert res.estado == "error"
    assert res.codigo == "ERR-11"
    assert read_table("corridas") == []


def test_inicio_concurrencia_activa_terminacion_controlada(
    temp_db_file: Path,
) -> None:
    acquire_lock("COR-OTRO", _marca(datetime.datetime.now()))
    try:
        res = ejecutar_inicio(dict(CONFIG_UNA_FUENTE))
    finally:
        release_lock("COR-OTRO")
    assert res.estado == "concurrencia"
    assert res.motivo == "concurrencia"
    assert res.codigo == "ERR-06"
    assert read_table("corridas") == []
    eventos = read_table("eventos")
    assert any(e["codigo"] == "ERR-06" for e in eventos)


def test_inicio_bloqueo_obsoleto_se_sobrescribe(temp_db_file: Path) -> None:
    viejo = datetime.datetime.now() - datetime.timedelta(minutes=300)
    acquire_lock("COR-VIEJA", _marca(viejo))
    try:
        res = ejecutar_inicio(dict(CONFIG_UNA_FUENTE))
        assert res.estado == "ok"
        bloqueo = check_lock()
        assert bloqueo is not None
        assert bloqueo["run_id"] == res.run_id
        eventos = read_table("eventos")
        assert any(e["codigo"] == "ERR-07" for e in eventos)
    finally:
        release_lock(res.run_id)


def test_inicio_bd_indisponible_aborta(temp_db_file: Path, monkeypatch: Any) -> None:
    def _boom() -> None:
        raise PersistenceError("05", "database down")

    monkeypatch.setattr("modules.discovery.nodes.inicio.init_db", _boom)
    res = ejecutar_inicio(dict(CONFIG_UNA_FUENTE))
    assert res.estado == "error"
    assert res.codigo == "ERR-05"


def test_inicio_config_ausente_aborta(temp_db_file: Path, monkeypatch: Any) -> None:
    def _sin_archivo() -> dict[str, Any]:
        raise FileNotFoundError("config.yaml missing")

    monkeypatch.setattr("modules.discovery.nodes.inicio.load", _sin_archivo)
    res = ejecutar_inicio()
    assert res.estado == "error"
    assert res.codigo == "ERR-02"


def test_inicio_config_ilegible_aborta(temp_db_file: Path, monkeypatch: Any) -> None:
    def _ilegible() -> dict[str, Any]:
        raise OSError("config.yaml unreadable")

    monkeypatch.setattr("modules.discovery.nodes.inicio.load", _ilegible)
    res = ejecutar_inicio()
    assert res.estado == "error"
    assert res.codigo == "ERR-03"


def test_inicio_run_id_falla_dos_veces_aborta(
    temp_db_file: Path, monkeypatch: Any
) -> None:
    def _falla() -> str:
        raise PersistenceError("01", "id generation down")

    monkeypatch.setattr("modules.discovery.nodes.inicio.generate_id", _falla)
    res = ejecutar_inicio(dict(CONFIG_UNA_FUENTE))
    assert res.estado == "error"
    assert res.codigo == "ERR-01"


def test_inicio_timestamp_bloqueo_invalido_aborta(
    temp_db_file: Path, monkeypatch: Any
) -> None:
    def _bloqueo_invalido() -> dict[str, Any] | None:
        return {"run_id": "COR-ROTA", "timestamp": "no-es-fecha"}

    monkeypatch.setattr("modules.discovery.nodes.inicio.check_lock", _bloqueo_invalido)
    res = ejecutar_inicio(dict(CONFIG_UNA_FUENTE))
    assert res.estado == "error"
    assert res.codigo == "ERR-08"
    assert read_table("corridas") == []


def test_inicio_descarta_estrategia_anti_bloqueo_invalida(
    temp_db_file: Path,
) -> None:
    con_estrategia_mala = {**FUENTE_VALIDA, "source_id": "fuente_maliciosa"}
    con_estrategia_mala["politicas_de_captura"] = {
        "max_paginas": 2,
        "max_ofertas_por_corrida": 10,
        "pausa_entre_lotes_segundos": 1,
        "estrategia_anti_bloqueo": "inventada",
    }
    res = ejecutar_inicio(
        {**CONFIG_BASE, "fuentes": [FUENTE_VALIDA, con_estrategia_mala]}
    )
    assert res.estado == "ok"
    assert res.contexto is not None
    assert [f.source_id for f in res.contexto.fuentes_filtradas] == ["linkedin"]
    eventos = read_table("eventos")
    assert any(e["codigo"] == "ERR-12" for e in eventos)


def test_inicio_descarta_fuente_sin_source_id(temp_db_file: Path) -> None:
    sin_id = {**FUENTE_VALIDA, "source_id": None}
    res = ejecutar_inicio({**CONFIG_BASE, "fuentes": [FUENTE_VALIDA, sin_id]})
    assert res.estado == "ok"
    assert res.contexto is not None
    assert [f.source_id for f in res.contexto.fuentes_filtradas] == ["linkedin"]
    eventos = read_table("eventos")
    assert any(
        e["codigo"] == "ERR-12" and "source_id" in e["evidencia"] for e in eventos
    )


def test_inicio_config_corrupta_aborta(temp_db_file: Path, monkeypatch: Any) -> None:
    def _corrupta() -> dict[str, Any]:
        raise yaml.YAMLError("bad yaml")

    monkeypatch.setattr("modules.discovery.nodes.inicio.load", _corrupta)
    res = ejecutar_inicio()
    assert res.estado == "error"
    assert res.codigo == "ERR-04"


def test_inicio_estado_interno_falla_aborta(
    temp_db_file: Path, monkeypatch: Any
) -> None:
    def _estalla(_: dict[str, Any]) -> None:
        raise RuntimeError("boom")

    monkeypatch.setattr("modules.discovery.nodes.inicio.write_corrida", _estalla)
    res = ejecutar_inicio(dict(CONFIG_UNA_FUENTE))
    assert res.estado == "error"
    assert res.codigo == "ERR-10"


def test_inicio_contienda_normal_err06_de_concurrencia(
    temp_db_file: Path, monkeypatch: Any
) -> None:
    def _pierde(_run_id: str, _ts: str) -> bool:
        return False

    monkeypatch.setattr(
        "modules.discovery.nodes.inicio.acquire_lock",
        lambda _run_id, _ts, forzar=False: False,
    )
    res = ejecutar_inicio(dict(CONFIG_UNA_FUENTE))
    assert res.estado == "concurrencia"
    assert res.codigo == "ERR-06"
    eventos = read_table("eventos")
    assert any(e["codigo"] == "ERR-06" for e in eventos)


def test_inicio_contienda_sobrescritura_err06(
    temp_db_file: Path, monkeypatch: Any
) -> None:
    viejo = datetime.datetime.now() - datetime.timedelta(minutes=300)
    acquire_lock("COR-VIEJA", _marca(viejo))
    try:
        monkeypatch.setattr(
            "modules.discovery.nodes.inicio.acquire_lock",
            lambda _run_id, _ts, forzar=False: False,
        )
        res = ejecutar_inicio(dict(CONFIG_UNA_FUENTE))
        assert res.estado == "concurrencia"
        assert res.codigo == "ERR-06"
    finally:
        release_lock("COR-VIEJA")
