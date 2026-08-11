from unittest.mock import MagicMock, patch

import pytest

from modules.discovery.adapters.linkedin import FlowError, LinkedInAdapter
from modules.discovery.nodes.busqueda import aplicar_filtros, se_encontraron_ofertas
from modules.discovery.run_context import RunContext
from shared.models import FichaFuente, Offer, SearchResult, SetFiltros


def _oferta() -> Offer:
    return Offer(enlace="https://jobs/view/1", titulo="Oferta", descripcion_original="")


def _resultado_ok(indice: int = 0, con_ofertas: bool = False) -> SearchResult:
    ofertas = [_oferta()] if con_ofertas else []
    return SearchResult(
        estado="exito",
        ofertas_primera_pagina=ofertas,
        estado_paginacion="fin",
        indice_set=indice,
        numero_de_intentos=1,
    )


def _search_result(ctx: RunContext) -> SearchResult:
    res = ctx.search_result
    assert res is not None
    return res


def _set_corriente(ctx: RunContext) -> SetFiltros:
    valor = ctx.set_corriente
    assert valor is not None
    return valor


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
                "sets_de_filtros": [
                    {"indice_set": 0, "filtros": [{"tipo": "keywords", "valor": "Python"}]},
                    {"indice_set": 1, "filtros": [{"tipo": "keywords", "valor": "Java"}]},
                ],
            }
        ]
    )
    ctx.handle_sesion = MagicMock()
    ctx.fuente_corriente = ctx.fuentes_filtradas[0]
    return ctx


def test_aplicar_filtros_success_with_results(mock_context: RunContext) -> None:
    with patch.object(LinkedInAdapter, "apply_filters") as mock_apply:
        mock_apply.return_value = SearchResult(
            estado="exito",
            ofertas_primera_pagina=[_oferta()],
            estado_paginacion="hay_mas",
            total_declarado=10,
            indice_set=0,
            numero_de_intentos=1,
        )
        res = aplicar_filtros(mock_context)
        assert res.estado == "ok"
        assert _search_result(mock_context).estado == "exito"
        assert _set_corriente(mock_context).indice == 0


def test_aplicar_filtros_success_no_results(mock_context: RunContext) -> None:
    with patch.object(LinkedInAdapter, "apply_filters") as mock_apply:
        mock_apply.return_value = _resultado_ok(indice=0)
        res = aplicar_filtros(mock_context)
        assert res.estado == "ok"
        assert len(_search_result(mock_context).ofertas_primera_pagina) == 0


def test_aplicar_filtros_empty_set_base_search(mock_context: RunContext) -> None:
    ficha_base = FichaFuente(
        fuente_id="BASE",
        nombre="B",
        enlace="U",
        tipo_acceso="publico",
        credenciales_referencia=[],
        criterio_exito="C",
        timeout_segundos=30,
    )
    mock_context.fuente_corriente = ficha_base
    mock_context._sets_validos["BASE"] = [SetFiltros(fuente_id="BASE", indice=0, filtros=[])]
    mock_context.iterador_sets["BASE"] = -1
    with patch.object(LinkedInAdapter, "apply_filters", return_value=_resultado_ok(indice=0)):
        res = aplicar_filtros(mock_context)
        assert res.estado == "ok"


def test_aplicar_filtros_not_applicable(mock_context: RunContext) -> None:
    with patch.object(LinkedInAdapter, "apply_filters") as mock_apply:
        mock_apply.side_effect = FlowError("filtros_no_aplicables", "Not supported")
        res = aplicar_filtros(mock_context)
        assert res.estado == "ok"
        assert _search_result(mock_context).estado == "fallo"
        assert _search_result(mock_context).codigo_motivo == "filtros_no_aplicables"


def test_aplicar_filtros_retry_success(mock_context: RunContext) -> None:
    with patch.object(LinkedInAdapter, "apply_filters") as mock_apply:
        mock_apply.side_effect = [
            FlowError("fuente_inalcanzable", "Down"),
            _resultado_ok(indice=0),
        ]
        res = aplicar_filtros(mock_context)
        assert res.estado == "ok"
        assert _search_result(mock_context).estado == "exito"


def test_aplicar_filtros_retry_exhausted(mock_context: RunContext) -> None:
    with patch.object(LinkedInAdapter, "apply_filters") as mock_apply:
        mock_apply.side_effect = FlowError("fuente_inalcanzable", "Down")
        res = aplicar_filtros(mock_context)
        assert res.estado == "ok"
        assert _search_result(mock_context).estado == "fallo"
        assert _search_result(mock_context).codigo_motivo == "fuente_inalcanzable"


def test_aplicar_filtros_session_expired(mock_context: RunContext) -> None:
    with patch.object(LinkedInAdapter, "apply_filters") as mock_apply:
        mock_apply.side_effect = FlowError("sesion_expirada", "Expired")
        res = aplicar_filtros(mock_context)
        assert res.estado == "ok"
        assert _search_result(mock_context).estado == "fallo"
        assert _search_result(mock_context).codigo_motivo == "sesion_expirada"


def test_aplicar_filtros_respuesta_invalida_sin_reintento(mock_context: RunContext) -> None:
    with patch.object(LinkedInAdapter, "apply_filters") as mock_apply:
        mock_apply.side_effect = FlowError("respuesta_invalida", "Bad payload")
        res = aplicar_filtros(mock_context)
        assert res.estado == "ok"
        assert _search_result(mock_context).estado == "fallo"
        assert _search_result(mock_context).codigo_motivo == "respuesta_invalida"
        assert mock_apply.call_count == 1


def test_aplicar_filtros_handle_missing(mock_context: RunContext) -> None:
    mock_context.handle_sesion = None
    res = aplicar_filtros(mock_context)
    assert res.estado == "error"
    assert res.codigo == "ERR-01"


def test_aplicar_filtros_source_change_resets_iterator(mock_context: RunContext) -> None:
    with patch.object(LinkedInAdapter, "apply_filters", return_value=_resultado_ok(indice=0)):
        aplicar_filtros(mock_context)
        fuente_corriente = mock_context.fuente_corriente
        assert fuente_corriente is not None
        fuente_id = fuente_corriente.fuente_id
        assert mock_context.iterador_sets[fuente_id] == 0

    ficha_nueva = FichaFuente(
        fuente_id="LI-02",
        nombre="L2",
        enlace="U",
        tipo_acceso="publico",
        credenciales_referencia=[],
        criterio_exito="C",
        timeout_segundos=30,
    )
    mock_context.fuente_corriente = ficha_nueva
    mock_context._sets_validos["LI-02"] = [SetFiltros(fuente_id="LI-02", indice=0, filtros=[])]
    mock_context.iterador_sets["LI-02"] = 5

    with patch.object(LinkedInAdapter, "apply_filters", return_value=_resultado_ok(indice=0)):
        aplicar_filtros(mock_context)
        assert mock_context.iterador_sets["LI-02"] == 0


def test_aplicar_filtros_set_marcado_como_procesado(mock_context: RunContext) -> None:
    with patch.object(LinkedInAdapter, "apply_filters", return_value=_resultado_ok(indice=0)):
        res = aplicar_filtros(mock_context)
        assert res.estado == "ok"
        assert _set_corriente(mock_context).indice == 0
        assert mock_context.iterador_sets["LI-01"] == 0

    with patch.object(LinkedInAdapter, "apply_filters", return_value=_resultado_ok(indice=1)):
        res = aplicar_filtros(mock_context)
        assert res.estado == "ok"
        assert _set_corriente(mock_context).indice == 1
        assert mock_context.iterador_sets["LI-01"] == 1


def test_se_encontraron_ofertas_si(mock_context: RunContext) -> None:
    mock_context.search_result = _resultado_ok(indice=0, con_ofertas=True)
    res = se_encontraron_ofertas(mock_context)
    assert res.decision == "si"


def test_se_encontraron_ofertas_no_empty(mock_context: RunContext) -> None:
    mock_context.search_result = _resultado_ok(indice=0)
    res = se_encontraron_ofertas(mock_context)
    assert res.decision == "no"


def test_se_encontraron_ofertas_no_fallo(mock_context: RunContext) -> None:
    mock_context.search_result = SearchResult(
        estado="fallo",
        ofertas_primera_pagina=[],
        estado_paginacion="fin",
        indice_set=0,
        numero_de_intentos=1,
    )
    res = se_encontraron_ofertas(mock_context)
    assert res.decision == "no"


def test_se_encontraron_ofertas_missing(mock_context: RunContext) -> None:
    mock_context.search_result = None
    res = se_encontraron_ofertas(mock_context)
    assert res.estado == "error"
    assert res.codigo == "ERR-01"
