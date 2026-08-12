from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest

from modules.discovery.adapters.linkedin import FlowError
from modules.discovery.nodes.captura import (
    capturar_ofertas,
    quedan_ofertas_por_capturar,
    quedan_sets_por_aplicar,
    registrar_ofertas,
)
from modules.discovery.run_context import RunContext
from shared.models import CaptureBatch, EstadoCaptura, Offer, SetFiltros


def _run_context(sets: int = 1) -> RunContext:
    config_fuentes = [
        {
            "fuente_id": "LI-01",
            "nombre": "LinkedIn",
            "ficha_acceso": {
                "enlace": "https://www.linkedin.com/jobs",
                "tipo_acceso": "publico",
                "criterio_exito": "global-nav",
                "timeout_segundos": 10,
            },
            "sets_de_filtros": [
                {"indice_set": i, "filtros": []} for i in range(sets)
            ],
        }
    ]
    contexto = RunContext(config_fuentes=config_fuentes)
    contexto.fuente_corriente = contexto.fuentes_filtradas[0]
    return contexto


def _oferta(enlace: str = "https://www.linkedin.com/jobs/view/123") -> Offer:
    return Offer(
        enlace=enlace,
        titulo="Desarrollador Python",
        descripcion_original="Descripcion de la vacante.",
        fuente_id="LI-01",
        indice_set=0,
        id_externo="123",
    )


@pytest.fixture
def contexto() -> RunContext:
    return _run_context()


@pytest.fixture
def adapter() -> Generator[MagicMock, None, None]:
    with patch("modules.discovery.nodes.captura.obtener_adaptador") as mock:
        yield mock.return_value


def test_captura_exitosa_guarda_resultados(
    contexto: RunContext, adapter: MagicMock
) -> None:
    contexto.handle_sesion = MagicMock()
    contexto.set_corriente = SetFiltros(fuente_id="LI-01", indice=0, filtros=[])
    lote = CaptureBatch(
        ofertas=[_oferta()],
        id_corrida=contexto.id_corrida,
        fuente_id="LI-01",
        id_sesion="SES-1",
        indice_set=0,
        paginas_consumidas=2,
    )
    estado = EstadoCaptura(
        estado="exito",
        paginas_consumidas=2,
        capturadas_acumuladas_fuente=1,
        limite_alcanzado=False,
    )
    adapter.capture_batch.return_value = (lote, estado)

    res = capturar_ofertas(contexto)

    assert res.estado == "ok"
    assert contexto.capture_batch is lote
    assert contexto.estado_captura is estado
    assert contexto.paginas_consumidas == 2
    assert contexto.capturadas_acumuladas_fuente == 1
    assert contexto.limite_alcanzado is False


def test_captura_handle_ausente(contexto: RunContext) -> None:
    contexto.handle_sesion = None
    res = capturar_ofertas(contexto)
    assert res.estado == "error"
    assert res.codigo == "ERR-01"


def test_captura_fuente_ausente(contexto: RunContext) -> None:
    contexto.fuente_corriente = None
    contexto.handle_sesion = MagicMock()

    res = capturar_ofertas(contexto)
    assert res.estado == "error"
    assert res.codigo == "ERR-01"


def test_captura_set_ausente(contexto: RunContext) -> None:
    contexto.handle_sesion = MagicMock()
    contexto.set_corriente = None

    res = capturar_ofertas(contexto)
    assert res.estado == "error"
    assert res.codigo == "ERR-01"


def test_captura_reintento_timeout_exito(
    contexto: RunContext, adapter: MagicMock
) -> None:
    contexto.handle_sesion = MagicMock()
    contexto.set_corriente = SetFiltros(fuente_id="LI-01", indice=0, filtros=[])
    lote = CaptureBatch(ofertas=[_oferta()], indice_set=0)
    estado = EstadoCaptura(estado="exito", capturadas_acumuladas_fuente=1)
    adapter.capture_batch.side_effect = [
        FlowError("tiempo_agotado_captura", "Page timeout"),
        (lote, estado),
    ]

    with patch("modules.discovery.nodes.captura.should_retry", return_value=True):
        with patch("modules.discovery.nodes.captura.time.sleep"):
            res = capturar_ofertas(contexto)

    assert res.estado == "ok"
    assert contexto.estado_captura is estado
    assert adapter.capture_batch.call_count == 2


def test_captura_timeout_todos_intentos(contexto: RunContext, adapter: MagicMock) -> None:
    contexto.handle_sesion = MagicMock()
    contexto.set_corriente = SetFiltros(fuente_id="LI-01", indice=0, filtros=[])
    adapter.capture_batch.side_effect = FlowError("tiempo_agotado_captura", "Timeout")

    with patch(
        "modules.discovery.nodes.captura.should_retry", return_value=True
    ):
        with patch("modules.discovery.nodes.captura.time.sleep"):
            with patch("modules.discovery.nodes.captura.write_evento"):
                res = capturar_ofertas(contexto)

    assert res.estado == "ok"
    assert contexto.estado_captura is not None
    assert contexto.estado_captura.estado == "fallo"
    assert contexto.estado_captura.codigo_motivo == "tiempo_agotado_captura"
    assert contexto.capture_batch is None
    assert adapter.capture_batch.call_count == 3


def test_captura_bloqueo_inmediato(contexto: RunContext, adapter: MagicMock) -> None:
    contexto.handle_sesion = MagicMock()
    contexto.set_corriente = SetFiltros(fuente_id="LI-01", indice=0, filtros=[])
    adapter.capture_batch.side_effect = FlowError("bloqueo_plataforma", "Captcha")

    with patch("modules.discovery.nodes.captura.write_evento"):
        res = capturar_ofertas(contexto)

    assert res.estado == "ok"
    assert contexto.estado_captura is not None
    assert contexto.estado_captura.estado == "fallo"
    assert contexto.estado_captura.codigo_motivo == "bloqueo_plataforma"
    assert adapter.capture_batch.call_count == 1


def test_captura_sesion_expirada_inmediato(
    contexto: RunContext, adapter: MagicMock
) -> None:
    contexto.handle_sesion = MagicMock()
    contexto.set_corriente = SetFiltros(fuente_id="LI-01", indice=0, filtros=[])
    adapter.capture_batch.side_effect = FlowError("sesion_expirada", "Authwall")

    with patch("modules.discovery.nodes.captura.write_evento"):
        res = capturar_ofertas(contexto)

    assert res.estado == "ok"
    assert contexto.estado_captura is not None
    assert contexto.estado_captura.estado == "fallo"
    assert contexto.estado_captura.codigo_motivo == "sesion_expirada"
    assert adapter.capture_batch.call_count == 1


def test_captura_auditoria_sesion_escrita(
    contexto: RunContext, adapter: MagicMock
) -> None:
    contexto.handle_sesion = MagicMock()
    contexto.id_sesion = "SES-1"
    contexto.set_corriente = SetFiltros(fuente_id="LI-01", indice=0, filtros=[])
    lote = CaptureBatch(
        ofertas=[_oferta()], indice_set=0, fuente_id="LI-01"
    )
    estado = EstadoCaptura(estado="exito")
    adapter.capture_batch.return_value = (lote, estado)

    with patch("modules.discovery.nodes.captura.write_row") as mock_write_row:
        res = capturar_ofertas(contexto)

    assert res.estado == "ok"
    mock_write_row.assert_called_once()
    args = mock_write_row.call_args.args
    assert args[0] == "sesiones"
    assert args[1]["id"] == "SES-1"
    assert args[1]["id_sesion"] == "SES-1"
    assert args[1]["conteo"] == 1
    assert args[1]["estado"] == "completa"


def test_captura_auditoria_falla_no_aborta(
    contexto: RunContext, adapter: MagicMock
) -> None:
    contexto.handle_sesion = MagicMock()
    contexto.set_corriente = SetFiltros(fuente_id="LI-01", indice=0, filtros=[])
    lote = CaptureBatch(ofertas=[_oferta()], indice_set=0)
    estado = EstadoCaptura(estado="exito")
    adapter.capture_batch.return_value = (lote, estado)

    with patch(
        "modules.discovery.nodes.captura.write_row", side_effect=RuntimeError("db")
    ) as mock_write_row:
        with patch("modules.discovery.nodes.captura.logger"):
            res = capturar_ofertas(contexto)

    assert res.estado == "ok"
    assert contexto.estado_captura is estado
    assert mock_write_row.call_count == 2


def test_registrar_una_oferta_upsert(
    contexto: RunContext,
) -> None:
    contexto.id_sesion = "SES-1"
    contexto.capture_batch = CaptureBatch(ofertas=[_oferta()], indice_set=0)

    with patch("modules.discovery.nodes.captura.upsert_oferta") as mock_upsert:
        with patch("modules.discovery.nodes.captura.write_evento"):
            res = registrar_ofertas(contexto)

    assert res.estado == "ok"
    mock_upsert.assert_called_once()
    fila = mock_upsert.call_args.args[0]
    assert fila["titulo"] == "Desarrollador Python"
    assert fila["fuente_id"] == "LI-01"
    assert fila["id_externo"] == "123"
    assert fila["id_corrida"] == contexto.id_corrida


def test_registrar_lote_vacio(contexto: RunContext) -> None:
    contexto.capture_batch = CaptureBatch(ofertas=[], indice_set=0)

    with patch("modules.discovery.nodes.captura.upsert_oferta") as mock_upsert:
        res = registrar_ofertas(contexto)

    assert res.estado == "ok"
    mock_upsert.assert_not_called()


def test_registrar_sin_lote(contexto: RunContext) -> None:
    contexto.capture_batch = None

    with patch("modules.discovery.nodes.captura.upsert_oferta") as mock_upsert:
        res = registrar_ofertas(contexto)

    assert res.estado == "ok"
    mock_upsert.assert_not_called()


def test_registrar_dedup_id_externo(contexto: RunContext) -> None:
    contexto.capture_batch = CaptureBatch(ofertas=[_oferta()], indice_set=0)

    with patch("modules.discovery.nodes.captura.upsert_oferta") as mock_upsert:
        registrar_ofertas(contexto)

    fila = mock_upsert.call_args.args[0]
    assert fila["id_externo"] == "123"


def test_registrar_ofertas_exito_registra_suceso(
    contexto: RunContext,
) -> None:
    contexto.id_sesion = "SES-9"
    contexto.fuente_corriente = _run_context().fuentes_filtradas[0]
    oferta_a = _oferta("https://www.linkedin.com/jobs/view/11")
    oferta_b = _oferta("https://www.linkedin.com/jobs/view/22")
    contexto.capture_batch = CaptureBatch(
        ofertas=[oferta_a, oferta_b], indice_set=0
    )
    contexto.set_corriente = SetFiltros(fuente_id="LI-01", indice=0, filtros=[])

    with patch("modules.discovery.nodes.captura.upsert_oferta") as mock_upsert:
        with patch("modules.discovery.nodes.captura.write_evento") as mock_evento:
            res = registrar_ofertas(contexto)

    assert res.estado == "ok"
    assert mock_upsert.call_count == 2
    mock_evento.assert_called_once()
    evento = mock_evento.call_args.args[0]
    assert evento["tipo"] == "suceso"
    assert evento["codigo"] == "ofertas_registradas"
    assert evento["evidencia"] == "ofertas registradas: 2 | total: 2"
    assert evento["id_corrida"] == contexto.id_corrida
    assert evento["id_sesion"] == "SES-9"
    assert evento["fuente_id"] == "LI-01"


def test_registrar_fallo_parcial(contexto: RunContext) -> None:
    oferta_a = _oferta("https://www.linkedin.com/jobs/view/1")
    oferta_b = _oferta("https://www.linkedin.com/jobs/view/2")
    contexto.capture_batch = CaptureBatch(ofertas=[oferta_a, oferta_b], indice_set=0)

    with patch(
        "modules.discovery.nodes.captura.upsert_oferta",
        side_effect=[None, RuntimeError("db"), RuntimeError("db")],
    ) as mock_upsert:
        with patch("modules.discovery.nodes.captura.write_evento") as mock_evento:
            with patch("modules.discovery.nodes.captura.logger"):
                res = registrar_ofertas(contexto)

    assert res.estado == "ok"
    assert mock_upsert.call_count == 3
    assert mock_evento.call_count == 2
    assert mock_evento.call_args_list[0].args[0]["codigo"] == "ofertas_registradas"
    assert mock_evento.call_args_list[1].args[0]["codigo"] == "registro_parcial"


def test_registrar_fallo_total(contexto: RunContext) -> None:
    oferta_a = _oferta("https://www.linkedin.com/jobs/view/1")
    oferta_b = _oferta("https://www.linkedin.com/jobs/view/2")
    contexto.capture_batch = CaptureBatch(ofertas=[oferta_a, oferta_b], indice_set=0)

    with patch(
        "modules.discovery.nodes.captura.upsert_oferta",
        side_effect=RuntimeError("db"),
    ) as mock_upsert:
        with patch("modules.discovery.nodes.captura.write_evento") as mock_evento:
            with patch("modules.discovery.nodes.captura.logger"):
                res = registrar_ofertas(contexto)

    assert res.estado == "ok"
    assert mock_upsert.call_count == 4
    mock_evento.assert_called_once()
    assert mock_evento.call_args.args[0]["codigo"] == "lote_degradado"


def test_quedan_ofertas_exito(contexto: RunContext) -> None:
    contexto.estado_captura = EstadoCaptura(estado="exito")
    res = quedan_ofertas_por_capturar(contexto)
    assert res.estado == "ok"
    assert res.decision == "no"


def test_quedan_ofertas_fallo(contexto: RunContext) -> None:
    contexto.estado_captura = EstadoCaptura(estado="fallo", codigo_motivo="x")
    res = quedan_ofertas_por_capturar(contexto)
    assert res.estado == "ok"
    assert res.decision == "no"


def test_quedan_ofertas_estado_ausente(contexto: RunContext) -> None:
    contexto.estado_captura = None
    res = quedan_ofertas_por_capturar(contexto)
    assert res.estado == "error"
    assert res.codigo == "ERR-01"


def test_quedan_sets_si() -> None:
    contexto = _run_context(sets=3)
    contexto.iterador_sets["LI-01"] = 0
    res = quedan_sets_por_aplicar(contexto)
    assert res.estado == "ok"
    assert res.decision == "si"


def test_quedan_sets_no() -> None:
    contexto = _run_context(sets=3)
    contexto.iterador_sets["LI-01"] = 2
    res = quedan_sets_por_aplicar(contexto)
    assert res.estado == "ok"
    assert res.decision == "no"


def test_quedan_sets_fuente_ausente(contexto: RunContext) -> None:
    contexto.fuente_corriente = None
    res = quedan_sets_por_aplicar(contexto)
    assert res.estado == "error"
    assert res.codigo == "ERR-01"
