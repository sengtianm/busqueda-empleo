"""Unit tests for the ¿Quedan ofertas en 'descubierta'? node (sub-phase 5.4).

The node is the module's only decision with I/O: a SQLite count through the
`temp_db_file` fixture, plus patched `contar_filas` for the DB-failure path.
"""

from typing import Any

import pytest

import modules.preparation.nodes.decision_bucle as decision_bucle
from modules.preparation.nodes.decision_bucle import ejecutar_decision_bucle
from modules.preparation.run_context import RunContext
from shared.persistence import escribir_fila, leer_tabla

CONFIG_RAPIDO: dict[str, Any] = {
    "umbral_titulo": 90,
    "umbral_descripcion": 85,
    "max_pasadas": 2,
    "retries": {
        "max_attempts": 2,
        "base_wait_seconds": 0,
        "max_wait_seconds": 0,
        "multiplier": 1,
    },
}


def _contexto(pasadas: int = 0, config: dict[str, Any] | None = None) -> RunContext:
    contexto = RunContext(
        config_preparacion=config if config is not None else dict(CONFIG_RAPIDO),
        candidatas=[],
        id_corrida="COR-BUC",
    )
    contexto.pasadas = pasadas
    return contexto


def _insertar_descubierta(oferta_id: str) -> None:
    escribir_fila(
        "ofertas_descubiertas",
        {
            "id": oferta_id,
            "enlace": f"https://www.linkedin.com/jobs/view/{oferta_id}",
            "fecha_descubrimiento": "2026-08-20 10:00:00",
            "estado": "descubierta",
            "titulo": "Titulo tarjeta",
        },
    )


def _eventos() -> list[dict[str, Any]]:
    return leer_tabla("eventos")


@pytest.mark.usefixtures("temp_db_file")
def test_rama_si_continua_e_incrementa_pasadas() -> None:
    _insertar_descubierta("OFE-001")
    resultado = ejecutar_decision_bucle(_contexto(pasadas=0))
    assert resultado.estado == "continuar"
    assert resultado.pendientes == 1
    assert resultado.pasadas == 1
    assert resultado.contexto is not None
    assert resultado.contexto.pasadas == 1


@pytest.mark.usefixtures("temp_db_file")
def test_rama_no_sin_pendientes_revision_pasadas_1() -> None:
    """No-loop close after one full pass: pasadas=1, pendientes=0."""
    resultado = ejecutar_decision_bucle(_contexto(pasadas=0))
    assert resultado.estado == "finalizar"
    assert resultado.pasadas == 1
    eventos = [e for e in _eventos() if e["codigo"] == "revision_pendientes"]
    assert len(eventos) == 1
    evento = eventos[0]
    assert evento["tipo"] == "suceso"
    assert "pasadas=1" in str(evento["evidencia"])
    assert "pendientes=0" in str(evento["evidencia"])


@pytest.mark.usefixtures("temp_db_file")
def test_rama_no_por_max_pasadas_agotado() -> None:
    _insertar_descubierta("OFE-001")
    _insertar_descubierta("OFE-002")
    resultado = ejecutar_decision_bucle(_contexto(pasadas=1))
    assert resultado.estado == "finalizar"
    assert resultado.pendientes == 2
    eventos = [e for e in _eventos() if e["codigo"] == "revision_pendientes"]
    assert len(eventos) == 1
    assert "pendientes=2" in str(eventos[0]["evidencia"])


@pytest.mark.usefixtures("temp_db_file")
def test_frontera_pasadas_igual_max_es_no() -> None:
    """VAL-03: Sí requires pasadas_actuales < max_pasadas; equality closes."""
    _insertar_descubierta("OFE-001")
    resultado = ejecutar_decision_bucle(_contexto(pasadas=2))
    assert resultado.estado == "finalizar"


@pytest.mark.usefixtures("temp_db_file")
def test_revision_pendientes_escrito_antes_de_entregar_control() -> None:
    """VAL-04: the event exists as soon as the node returns finalizar."""
    resultado = ejecutar_decision_bucle(_contexto(pasadas=1))
    assert resultado.estado == "finalizar"
    assert any(e["codigo"] == "revision_pendientes" for e in _eventos())


@pytest.mark.usefixtures("temp_db_file")
def test_err01_conteo_bd_agota_y_aborta(monkeypatch: pytest.MonkeyPatch) -> None:
    def estalla(*args: Any, **kwargs: Any) -> int:
        raise RuntimeError("bd caida")

    monkeypatch.setattr(decision_bucle, "contar_filas", estalla)
    resultado = ejecutar_decision_bucle(_contexto())
    assert resultado.estado == "abortada"
    assert resultado.codigo == "ERR-01"


@pytest.mark.usefixtures("temp_db_file")
def test_val01_max_pasadas_invalido_aborta() -> None:
    config = dict(CONFIG_RAPIDO)
    config["max_pasadas"] = 0
    resultado = ejecutar_decision_bucle(_contexto(config=config))
    assert resultado.estado == "abortada"
    assert resultado.codigo == "ERR-01"


@pytest.mark.usefixtures("temp_db_file")
def test_contexto_ausente_aborta() -> None:
    resultado = ejecutar_decision_bucle(None)
    assert resultado.estado == "abortada"
    assert resultado.codigo == "ERR-01"
