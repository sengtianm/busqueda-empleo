"""Unit tests for the Preparation RunContext (sub-phase 5.2)."""

from typing import Any

from modules.preparation.run_context import RunContext


def test_contexto_defaults() -> None:
    ctx = RunContext()
    assert ctx.id_corrida.startswith("COR-")
    assert ctx.fecha_inicio
    assert ctx.config_preparacion == {}
    assert ctx.candidatas == []
    assert ctx.hubo_candidatas is False
    assert ctx.contador_preparadas == 0
    assert ctx.contador_duplicadas == 0
    assert ctx.contador_errores == 0
    assert ctx.bloqueo_adquirido is False
    assert ctx.motivo_cierre is None
    assert ctx.motivo_marca_temporal is None


def test_contexto_con_candidatas_marca_hubo() -> None:
    ctx = RunContext(candidatas=[{"id": "OFE-0001"}])
    assert ctx.hubo_candidatas is True
    assert ctx.candidatas[0]["id"] == "OFE-0001"


def test_contexto_id_explicito_se_respeta() -> None:
    ctx = RunContext(id_corrida="COR-PRUEBA")
    assert ctx.id_corrida == "COR-PRUEBA"


def test_contexto_config_se_guarda_tal_cual() -> None:
    conf: dict[str, Any] = {"umbral_titulo": 90}
    ctx = RunContext(config_preparacion=conf)
    assert ctx.config_preparacion is conf
