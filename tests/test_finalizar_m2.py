"""Unit tests for the Finalizar Proceso node of Module 2 (sub-phase 5.5).

Covers the official motive/state/event-type matrix, metrics from events
(D36 DISTINCT semantics, D30 pre-closure counting), motive resolution
priority, best-effort persistence (single retries never abort), resource
closing, ownership-safe lock release and the H2 enrichment stub.
"""

from typing import Any, Generator

import pytest

import modules.preparation.nodes.finalizar as finalizar_mod
from modules.preparation.nodes.finalizar import (
    cerrar_recursos,
    finalizar_proceso,
)
from modules.preparation.run_context import RunContext
from shared.persistence import (
    actualizar_corrida,
    adquirir_bloqueo,
    consultar_bloqueo,
    escribir_evento,
    leer_tabla,
    liberar_bloqueo,
    registrar_corrida,
)

CONFIG_BASE: dict[str, Any] = {
    "umbral_titulo": 90,
    "umbral_descripcion": 85,
    "max_pasadas": 2,
    "profundidad_catalogo_empresa": 0,
}


@pytest.fixture
def mensajes_loguru() -> Generator[list[str]]:
    """Captures Loguru messages (caplog only sees stdlib logging)."""
    from loguru import logger

    mensajes: list[str] = []
    handler_id = logger.add(mensajes.append, format="{message}", level="INFO")
    yield mensajes
    logger.remove(handler_id)


def _contexto(
    *,
    candidatas: int = 0,
    motivo_cierre: str | None = None,
    id_corrida: str = "COR-FIN",
) -> RunContext:
    ctx = RunContext(
        config_preparacion=dict(CONFIG_BASE),
        candidatas=[
            {"id": f"OFE-{i:04d}"} for i in range(candidatas)
        ],
        id_corrida=id_corrida,
    )
    ctx.motivo_cierre = motivo_cierre
    return ctx


def _registrar_corrida(id_corrida: str) -> None:
    registrar_corrida(
        {
            "id_corrida": id_corrida,
            "fecha_inicio": "2026-08-21 08:00:00",
            "estado": "en_ejecucion",
        }
    )


_evento_n = [0]


def _evento(
    tipo: str,
    codigo: str,
    *,
    id_corrida: str = "COR-FIN",
    id_oferta: str = "N/A",
) -> None:
    _evento_n[0] += 1
    escribir_evento(
        {
            "evento_id": f"EVT-{_evento_n[0]:04d}",
            "id_corrida": id_corrida,
            "marca_temporal": "2026-08-21 09:00:00",
            "tipo": tipo,
            "codigo": codigo,
            "evidencia": "prueba",
            "id_oferta": id_oferta,
        }
    )


# ------------------------------------------------------------ matriz de motivos


@pytest.mark.usefixtures("temp_db_file")
@pytest.mark.parametrize(
    "motivo,estado,tipo_evento",
    [
        ("sin_pendientes", "sin_pendientes", "suceso"),
        ("corrida_completada", "completada", "suceso"),
        ("error_total", "abortada", "error"),
        ("error_critico", "abortada", "error"),
        ("aborto", "abortada", "error"),
        ("concurrencia", "abortada", "suceso"),
    ],
)
def test_matriz_motivos_estado_y_tipo_evento(
    motivo: str, estado: str, tipo_evento: str
) -> None:
    _registrar_corrida("COR-FIN")
    res = finalizar_proceso(_contexto(), motivo)
    assert res.estado == "ok"
    assert res.codigo == motivo
    corrida = next(c for c in leer_tabla("corridas") if c["id_corrida"] == "COR-FIN")
    assert corrida["estado"] == estado
    assert corrida["motivo_terminacion"] == motivo
    assert corrida["fecha_fin"] != ""
    evento = leer_tabla("eventos")[-1]
    assert evento["codigo"] == motivo
    assert evento["tipo"] == tipo_evento


# ------------------------------------------------------------------- métricas


@pytest.mark.usefixtures("temp_db_file")
def test_metricas_distinct_d36_doble_emision_cuenta_uno() -> None:
    _registrar_corrida("COR-FIN")
    _evento("suceso", "oferta_preparada", id_oferta="OFE-0001")
    _evento("suceso", "oferta_preparada", id_oferta="OFE-0001")  # lote (b), D36
    _evento("suceso", "oferta_preparada", id_oferta="OFE-0002")
    _evento("suceso", "oferta_duplicada", id_oferta="OFE-0003")
    res = finalizar_proceso(_contexto(), "corrida_completada")
    m = res.metricas
    assert m is not None
    assert m["total_preparadas"] == 2  # DISTINCT id_oferta
    assert m["total_duplicadas"] == 1
    assert m["total_ofertas"] == 3


@pytest.mark.usefixtures("temp_db_file")
def test_total_ofertas_union_cuenta_solape_una_vez() -> None:
    """Traspaso 2026-08-25: una oferta preparada y LUEGO duplicada se cuenta
    una sola vez en `total_ofertas` (unión DISTINCT), que reporta el total
    físico en lugar de la suma literal preparadas+duplicadas."""
    _registrar_corrida("COR-FIN")
    _evento("suceso", "oferta_preparada", id_oferta="OFE-0001")
    _evento("suceso", "oferta_preparada", id_oferta="OFE-0002")
    _evento("suceso", "oferta_duplicada", id_oferta="OFE-0002")
    res = finalizar_proceso(_contexto(), "corrida_completada")
    m = res.metricas
    assert m is not None
    assert m["total_preparadas"] == 2
    assert m["total_duplicadas"] == 1
    assert m["total_ofertas"] == 2


@pytest.mark.usefixtures("temp_db_file")
def test_total_sucesos_excluye_evento_terminacion_d30() -> None:
    _registrar_corrida("COR-FIN")
    _evento("suceso", "revision_pendientes")
    _evento("suceso", "ingreso_exitoso")
    finalizar_proceso(_contexto(), "corrida_completada")
    eventos = leer_tabla("eventos")
    assert len(eventos) == 3  # 2 previos + terminación
    corrida = next(c for c in leer_tabla("corridas") if c["id_corrida"] == "COR-FIN")
    assert corrida["total_sucesos"] == 2  # el evento de cierre no se cuenta
    assert corrida["total_errores"] == 0


@pytest.mark.usefixtures("temp_db_file")
def test_metricas_solo_de_la_corrida_propia() -> None:
    _registrar_corrida("COR-FIN")
    _evento("suceso", "oferta_preparada", id_oferta="OFE-0001")
    _evento("suceso", "oferta_preparada", id_corrida="COR-OTRA", id_oferta="OFE-0009")
    res = finalizar_proceso(_contexto(), "corrida_completada")
    assert res.metricas is not None
    assert res.metricas["total_preparadas"] == 1


@pytest.mark.usefixtures("temp_db_file")
def test_evidencia_terminacion_campo_valor() -> None:
    _registrar_corrida("COR-FIN")
    _evento("suceso", "oferta_preparada", id_oferta="OFE-0001")
    finalizar_proceso(_contexto(), "corrida_completada")
    evento = leer_tabla("eventos")[-1]
    assert "total_preparadas=1" in evento["evidencia"]
    assert "total_ofertas=1" in evento["evidencia"]


# ------------------------------------------------------- resolución de motivo


@pytest.mark.usefixtures("temp_db_file")
def test_derivacion_error_total_con_candidatas_todas_fallidas() -> None:
    _registrar_corrida("COR-FIN")
    _evento("error", "preparacion_fallida")
    _evento("error", "preparacion_fallida")
    res = finalizar_proceso(_contexto(candidatas=3))  # sin motivo explícito
    assert res.codigo == "error_total"
    assert leer_tabla("corridas")[0]["estado"] == "abortada"


@pytest.mark.usefixtures("temp_db_file")
def test_derivacion_corrida_completada_con_exito() -> None:
    _registrar_corrida("COR-FIN")
    _evento("suceso", "oferta_preparada", id_oferta="OFE-0001")
    res = finalizar_proceso(_contexto(candidatas=1))
    assert res.codigo == "corrida_completada"


@pytest.mark.usefixtures("temp_db_file")
def test_motivo_prefijado_en_contexto_tiene_prioridad() -> None:
    _registrar_corrida("COR-FIN")
    res = finalizar_proceso(_contexto(motivo_cierre="sin_pendientes"))
    assert res.codigo == "sin_pendientes"
    assert leer_tabla("corridas")[0]["estado"] == "sin_pendientes"


@pytest.mark.usefixtures("temp_db_file")
def test_motivo_explicito_gana_sobre_prefijo() -> None:
    _registrar_corrida("COR-FIN")
    res = finalizar_proceso(
        _contexto(motivo_cierre="sin_pendientes"), "error_critico"
    )
    assert res.codigo == "error_critico"


@pytest.mark.usefixtures("temp_db_file")
def test_metricas_fallidas_sin_motivo_previo_degradan_a_aborto(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _registrar_corrida("COR-FIN")

    def _estalla(*args: Any, **kwargs: Any) -> int:
        raise RuntimeError("bd caida")

    monkeypatch.setattr(finalizar_mod, "contar_filas", _estalla)
    monkeypatch.setattr(finalizar_mod, "contar_distintos", _estalla)
    res = finalizar_proceso(_contexto(candidatas=1))
    # Ficha M2: métricas vacías + motivo por defecto `aborto` (no ceros, M1).
    assert res.metricas is None
    assert res.codigo == "aborto"
    assert leer_tabla("eventos")[-1]["evidencia"] == "metricas=no_disponibles"


@pytest.mark.usefixtures("temp_db_file")
def test_metricas_fallidas_con_motivo_explicito_lo_conserva(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _registrar_corrida("COR-FIN")

    def _estalla(*args: Any, **kwargs: Any) -> int:
        raise RuntimeError("bd caida")

    monkeypatch.setattr(finalizar_mod, "contar_filas", _estalla)
    monkeypatch.setattr(finalizar_mod, "contar_distintos", _estalla)
    res = finalizar_proceso(None, "concurrencia", "COR-FIN")
    assert res.codigo == "concurrencia"
    assert res.metricas is None


# ---------------------------------------------------------- persistencia cierre


@pytest.mark.usefixtures("temp_db_file")
def test_actualizar_corrida_reintenta_una_vez_y_persiste(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _registrar_corrida("COR-FIN")
    intentos: list[int] = []
    real = actualizar_corrida

    def _falla_una(*args: Any, **kwargs: Any) -> bool:
        intentos.append(1)
        if len(intentos) == 1:
            raise RuntimeError("lock momentaneo")
        return real(*args, **kwargs)

    monkeypatch.setattr(
        "modules.preparation.nodes.finalizar.actualizar_corrida", _falla_una
    )
    finalizar_proceso(_contexto(), "corrida_completada")
    assert len(intentos) == 2
    assert leer_tabla("corridas")[0]["estado"] == "completada"


@pytest.mark.usefixtures("temp_db_file")
def test_evento_terminacion_fallido_no_aborta(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _registrar_corrida("COR-FIN")

    def _estalla(*args: Any, **kwargs: Any) -> None:
        raise RuntimeError("bd caida")

    monkeypatch.setattr(finalizar_mod, "escribir_evento_seguro", _estalla)
    res = finalizar_proceso(_contexto(), "corrida_completada")
    assert res.estado == "ok"  # best-effort: nunca aborta
    assert leer_tabla("corridas")[0]["estado"] == "completada"


# ------------------------------------------------------------- recursos/bloqueo


class _SesionFalsa:
    def __init__(self) -> None:
        self.cerrada = False

    def close(self) -> None:
        self.cerrada = True


@pytest.mark.usefixtures("temp_db_file")
def test_cerrar_recursos_cierra_sesion_y_es_idempotente() -> None:
    ctx = _contexto()
    sesion = _SesionFalsa()
    ctx.sesion_http = sesion
    ctx.ofertas_en_sesion = 7
    cerrar_recursos(ctx)
    assert sesion.cerrada is True
    assert ctx.sesion_http is None
    assert ctx.ofertas_en_sesion == 0
    cerrar_recursos(ctx)  # segunda llamada: no-op sin excepción


@pytest.mark.usefixtures("temp_db_file")
def test_bloqueo_ajeno_sobrevive_al_cierre() -> None:
    _registrar_corrida("COR-FIN")
    adquirir_bloqueo("COR-OTRA", "2026-08-21 08:30:00")
    try:
        finalizar_proceso(None, "aborto", "COR-FIN")
        bloqueo = consultar_bloqueo()
        assert bloqueo is not None
        assert bloqueo["id_corrida"] == "COR-OTRA"
    finally:
        liberar_bloqueo("COR-OTRA")


@pytest.mark.usefixtures("temp_db_file")
def test_ruta_concurrencia_sin_contexto_cierra_por_id() -> None:
    """INICIO ERR-06 route: no context, but the row exists (P2-A)."""
    _registrar_corrida("COR-FIN")
    res = finalizar_proceso(None, "concurrencia", "COR-FIN")
    assert res.estado == "ok"
    assert res.codigo == "concurrencia"
    corrida = leer_tabla("corridas")[0]
    assert corrida["estado"] == "abortada"
    assert leer_tabla("eventos")[-1]["tipo"] == "suceso"


@pytest.mark.usefixtures("temp_db_file")
def test_contexto_corrupto_no_explota() -> None:
    res = finalizar_proceso(None, "aborto", "")
    assert res.estado == "ok"
    assert res.codigo == "aborto"
