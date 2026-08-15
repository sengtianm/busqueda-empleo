import tempfile
from pathlib import Path

import pytest

from modules.discovery.run_context import RunContext
from shared.errors import ConfigurationError
from shared.models import SearchResult

CONFIG_FUENTES_VALIDAS = [
    {
        "fuente_id": "linkedin",
        "nombre": "LinkedIn",
        "ficha_acceso": {
            "enlace": "https://www.linkedin.com/jobs/search",
            "tipo_acceso": "con_autenticacion",
            "credenciales_referencia": ["LINKEDIN_EMAIL", "LINKEDIN_PASSWORD"],
            "criterio_exito": "global-nav",
            "timeout_segundos": 30,
        },
        "sets_de_filtros": [
            {
                "indice_set": 0,
                "filtros": [{"tipo": "keywords", "valor": ["Data Engineer"]}],
            },
            {
                "indice_set": 1,
                "filtros": [{"tipo": "modalidad", "valor": "remoto"}],
            },
        ],
        "politicas_de_captura": {
            "max_paginas": 2,
            "max_ofertas_por_corrida": 10,
            "pausa_entre_lotes_segundos": 1,
            "estrategia_anti_bloqueo": "none",
        },
    }
]


def test_contexto_filtra_fuentes_validas() -> None:
    contexto = RunContext(CONFIG_FUENTES_VALIDAS, id_corrida="COR-TEST-01")
    assert [f.fuente_id for f in contexto.fuentes_filtradas] == ["linkedin"]
    assert contexto.fuentes_filtradas[0].criterio_exito == "global-nav"


def test_contexto_rechaza_fuente_sin_ficha_acceso() -> None:
    conf = [{"fuente_id": "incompleta", "nombre": "Incompleta"}]
    with pytest.raises(ConfigurationError) as exc:
        RunContext(conf, id_corrida="COR-TEST-02")
    assert "ficha_acceso" in str(exc.value)


def test_contexto_rechaza_tipo_acceso_invalido() -> None:
    conf = [
        {
            "fuente_id": "x",
            "nombre": "X",
            "ficha_acceso": {"enlace": "https://x.com", "tipo_acceso": "raro"},
        }
    ]
    with pytest.raises(ConfigurationError):
        RunContext(conf, id_corrida="COR-TEST-03")


def test_contexto_sin_fuentes_error() -> None:
    with pytest.raises(ConfigurationError):
        RunContext([], id_corrida="COR-TEST-04")


def test_contexto_contiene_sets_por_fuente() -> None:
    contexto = RunContext(CONFIG_FUENTES_VALIDAS, id_corrida="COR-TEST-05")
    ficha = contexto.fuentes_filtradas[0]
    sets = contexto.sets_validos(ficha)
    assert [s.indice for s in sets] == [0, 1]


def test_seleccionar_set_aumenta_iterador() -> None:
    contexto = RunContext(CONFIG_FUENTES_VALIDAS, id_corrida="COR-TEST-06")
    assert contexto.iterador_sets["linkedin"] == -1
    assert contexto.seleccionar_siguiente_set("linkedin") == 0
    assert contexto.seleccionar_siguiente_set("linkedin") == 1


def test_reset_iteradores() -> None:
    contexto = RunContext(CONFIG_FUENTES_VALIDAS, id_corrida="COR-TEST-07")
    contexto.seleccionar_siguiente_set("linkedin")
    contexto.bloqueo_adquirido = True
    contexto.reset_iteradores()
    assert contexto.iterador_sets["linkedin"] == -1
    assert contexto.iterador_fuentes == -1
    assert not contexto.bloqueo_adquirido


def test_contexto_recursos_playwright_por_defecto_none() -> None:
    contexto = RunContext(CONFIG_FUENTES_VALIDAS, id_corrida="COR-TEST-09")
    assert contexto.browser is None
    assert contexto.playwright_instance is None


def test_reset_iteradores_limpia_recursos_playwright() -> None:
    contexto = RunContext(CONFIG_FUENTES_VALIDAS, id_corrida="COR-TEST-10")
    contexto.browser = object()
    contexto.playwright_instance = object()
    contexto.handle_sesion = object()
    contexto.reset_iteradores()
    assert contexto.browser is None
    assert contexto.playwright_instance is None
    assert contexto.handle_sesion is None


def test_marcar_cambio_de_fuente() -> None:
    contexto = RunContext(CONFIG_FUENTES_VALIDAS, id_corrida="COR-TEST-11")
    contexto.search_result = SearchResult()
    contexto.marcar_cambio_de_fuente("linkedin")
    assert contexto.search_result is None
    assert contexto.iterador_sets["linkedin"] == -1
    assert contexto._ultimo_fuente_id_sets == "linkedin"
    otras = [f for f in contexto.iterador_sets if f != "linkedin"]
    assert all(contexto.iterador_sets[f] == -1 for f in otras)


def test_marcar_cambio_de_fuente_sin_cambio_no_resetea_iterador() -> None:
    contexto = RunContext(CONFIG_FUENTES_VALIDAS, id_corrida="COR-TEST-12")
    contexto.marcar_cambio_de_fuente("linkedin")
    contexto.search_result = SearchResult()
    contexto.iterador_sets["linkedin"] = 2
    contexto.marcar_cambio_de_fuente("linkedin")
    assert contexto.iterador_sets["linkedin"] == 2
    assert contexto.search_result is not None


def test_run_context_politicas_desde_config() -> None:
    contexto = RunContext(CONFIG_FUENTES_VALIDAS, id_corrida="COR-TEST-08")
    politicas = contexto.politicas(contexto.fuentes_filtradas[0])
    assert politicas.max_paginas == 2
    assert politicas.max_ofertas_por_corrida == 10
    assert politicas.estrategia_anti_bloqueo == "none"


def test_run_crea_run_id_cuando_no_se_proporciona() -> None:
    from shared.persistence import change_path, init_db, reset_path

    with tempfile.TemporaryDirectory() as tmp:
        change_path(Path(tmp) / "test.db")
        init_db()
        try:
            contexto = RunContext(CONFIG_FUENTES_VALIDAS)
        finally:
            reset_path()
    assert contexto.id_corrida.startswith("COR-")
