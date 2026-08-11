from unittest.mock import patch

import pytest

from modules.discovery.nodes.registro import registrar_evento
from modules.discovery.run_context import RunContext
from shared.models import EntryResult, FichaFuente, SearchResult, SetFiltros


@pytest.fixture
def mock_context() -> RunContext:
    ctx = RunContext(
        config_fuentes=[
            {
                "fuente_id": "LI-01",
                "nombre": "LinkedIn",
                "ficha_acceso": {
                    "enlace": "https://linkedin.com",
                    "tipo_acceso": "publico",
                    "criterio_exito": "jobs",
                    "timeout_segundos": 30,
                },
            }
        ]
    )
    ctx.fuente_corriente = ctx.fuentes_filtradas[0]
    return ctx


def test_registrar_evento_search_fallo(mock_context: RunContext) -> None:
    mock_context.set_corriente = SetFiltros(fuente_id="LI-01", indice=2, filtros=[])
    mock_context.search_result = SearchResult(
        estado="fallo",
        codigo_motivo="ERR-03",
        evidencia_acotada="Down",
        ofertas_primera_pagina=[],
        estado_paginacion="fin",
        indice_set=2,
        numero_de_intentos=3,
    )
    with patch("modules.discovery.nodes.registro.write_evento") as mock_write:
        res = registrar_evento(mock_context)
        assert res.estado == "ok"
        mock_write.assert_called_once()
        args = mock_write.call_args[0][0]
        assert args["tipo"] == "error"
        assert args["indice_set"] == 2
        assert "intentos: 3" in args["evidencia"]


def test_registrar_evento_search_exito_empty(mock_context: RunContext) -> None:
    mock_context.set_corriente = SetFiltros(fuente_id="LI-01", indice=1, filtros=[])
    mock_context.search_result = SearchResult(
        estado="exito",
        codigo_motivo="",
        evidencia_acotada="No offers",
        ofertas_primera_pagina=[],
        estado_paginacion="fin",
        indice_set=1,
        numero_de_intentos=1,
    )
    with patch("modules.discovery.nodes.registro.write_evento") as mock_write:
        res = registrar_evento(mock_context)
        assert res.estado == "ok"
        args = mock_write.call_args[0][0]
        assert args["tipo"] == "suceso"
        assert args["indice_set"] == 1


def test_registrar_evento_entry_fallo(mock_context: RunContext) -> None:
    mock_context.search_result = None
    mock_context.entry_result = EntryResult(
        estado="fallo",
        codigo_motivo="credenciales_no_disponibles",
        evidencia_acotada="Missing env",
        numero_de_intentos=1,
    )
    with patch("modules.discovery.nodes.registro.write_evento") as mock_write:
        res = registrar_evento(mock_context)
        assert res.estado == "ok"
        args = mock_write.call_args[0][0]
        assert args["tipo"] == "error"
        assert args["indice_set"] is None


def test_registrar_evento_entry_priorizado_si_search_es_de_otra_fuente(
    mock_context: RunContext,
) -> None:
    # Source switch: LI-02 entry failed but the previous source LI-01
    # still has a populated search_result in the context.
    mock_context.set_corriente = SetFiltros(fuente_id="LI-01", indice=2, filtros=[])
    mock_context.search_result = SearchResult(
        estado="exito",
        ofertas_primera_pagina=[],
        estado_paginacion="fin",
        indice_set=2,
        numero_de_intentos=1,
    )
    mock_context.fuente_corriente = FichaFuente(
        fuente_id="LI-02",
        nombre="LinkedIn2",
        enlace="https://linkedin.com",
        tipo_acceso="publico",
        criterio_exito="jobs",
        timeout_segundos=30,
    )
    mock_context.entry_result = EntryResult(
        estado="fallo",
        codigo_motivo="fuente_inalcanzable",
        evidencia_acotada="Down",
        numero_de_intentos=2,
    )
    with patch("modules.discovery.nodes.registro.write_evento") as mock_write:
        res = registrar_evento(mock_context)
        assert res.estado == "ok"
        args = mock_write.call_args[0][0]
        assert args["fuente_id"] == "LI-02"
        assert args["tipo"] == "error"
        assert args["codigo"] == "fuente_inalcanzable"
        assert args["indice_set"] is None


def test_registrar_evento_write_fail_continues(mock_context: RunContext) -> None:
    mock_context.set_corriente = SetFiltros(fuente_id="LI-01", indice=0, filtros=[])
    mock_context.search_result = SearchResult(
        estado="fallo",
        codigo_motivo="ERR",
        evidencia_acotada="E",
        ofertas_primera_pagina=[],
        estado_paginacion="fin",
        indice_set=0,
        numero_de_intentos=1,
    )
    with patch(
        "modules.discovery.nodes.registro.write_evento", side_effect=Exception("DB Error")
    ):
        res = registrar_evento(mock_context)
        assert res.estado == "ok"
