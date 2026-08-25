"""Unit tests for company-profile enrichment (decision D39).

Covers the guest-profile reader (`modules/preparation/nodes/enriquecimiento`)
and the step-2 hook in the Preparation node: extraction from realistic
ES/EN page structures (experiment 2026-08-25), refined wall detection,
retry-after-cooldown, run caches, the optional depth brake and
autocuración of still-incomplete companies.
"""

from pathlib import Path
from typing import Any

import httpx
import pytest

import modules.preparation.nodes.preparacion as preparacion_mod
from modules.preparation.nodes import enriquecimiento as enriquecimiento_mod
from modules.preparation.nodes.enriquecimiento import (
    _es_muro,
    _extraer_campos,
    _limpiar_url_perfil,
    enriquecer_empresa,
)
from modules.preparation.run_context import RunContext
from shared.persistence import escribir_fila, leer_tabla

_FIXTURAS = Path(__file__).parent / "fixtures"
HTML_ES = (_FIXTURAS / "perfil_empresa_es.html").read_text(encoding="utf-8")
HTML_EN = (_FIXTURAS / "perfil_empresa_en.html").read_text(encoding="utf-8")
# Real profile pages carry large payloads (100-400 KB); the wall heuristic
# treats tiny bodies as blocks, so served fixtures get padded past the bar.
_RELLENO = "<!--" + "p" * 12_000 + "-->"

CONFIG: dict[str, Any] = {
    "profundidad_catalogo_empresa": 0,
    "pausa_entre_empresas_segundos": 0,
}


def _contexto(config: dict[str, Any] | None = None) -> RunContext:
    return RunContext(
        config_preparacion=config if config is not None else dict(CONFIG),
        candidatas=[],
        id_corrida="COR-ENR",
    )


def _insertar_empresa(empresa_id: str = "EMP-0001", **extras: Any) -> None:
    fila: dict[str, Any] = {
        "id": empresa_id,
        "nombre": "Deel",
        "nombre_normalizado": "deel",
    }
    fila.update(extras)
    escribir_fila("empresas", fila)


def _cliente(handler: Any) -> httpx.Client:
    return httpx.Client(
        transport=httpx.MockTransport(handler), follow_redirects=True
    )


# ------------------------------------------------------------------ limpieza


@pytest.mark.parametrize(
    "url,esperado",
    [
        (
            "https://www.linkedin.com/company/deel?trk=public_jobs_topcard",
            "https://www.linkedin.com/company/deel",
        ),
        (
            "https://co.linkedin.com/company/bancolombia",
            "https://co.linkedin.com/company/bancolombia",
        ),
        ("https://www.linkedin.com/jobs/view/123", ""),
        ("N/A", ""),
        ("", ""),
    ],
)
def test_limpiar_url_perfil(url: str, esperado: str) -> None:
    assert _limpiar_url_perfil(url) == esperado


# ---------------------------------------------------------------------- muro


def test_muro_por_estados_atipicos() -> None:
    assert _es_muro(httpx.Response(999, text=""))
    assert _es_muro(httpx.Response(429, text=""))


def test_muro_por_cuerpo_diminuto() -> None:
    assert _es_muro(httpx.Response(200, text="<html>stub</html>"))


def test_pagina_grande_con_texto_de_registro_no_es_muro() -> None:
    """False-positive guard: real pages contain sign-up strings."""
    grande = HTML_ES + _RELLENO
    assert not _es_muro(httpx.Response(200, text=grande))


# --------------------------------------------------------------- extraccion


def test_extraccion_etiquetas_espanolas() -> None:
    campos = _extraer_campos(HTML_ES)
    assert campos["sitio_web"] == "https://www.deel.com/"
    assert campos["sector"] == "Servicios de recursos humanos"
    assert campos["tamano"] == "De 5.001 a 10.000 empleados"
    assert campos["sede"] == "San Francisco, California"
    assert campos["tipo"] == "De financiación privada"
    assert campos["fundacion"] == "2019"
    assert campos["especialidades"].startswith("Payment Services")
    assert campos["descripcion"].startswith("Deel is one platform")


def test_extraccion_etiquetas_inglesas() -> None:
    campos = _extraer_campos(HTML_EN)
    assert campos["sitio_web"] == "https://acme.com/"
    assert campos["sector"] == "Industrial Machinery Manufacturing"
    assert campos["tamano"] == "201-500 employees"
    assert campos["sede"] == "Phoenix, Arizona"
    assert campos["tipo"] == "Privately Held"
    assert campos["fundacion"] == "1949"
    assert campos["especialidades"].startswith("Anvils")
    assert campos["descripcion"].startswith("Acme builds rocket-powered")


def test_campos_ausentes_quedan_nr() -> None:
    campos = _extraer_campos("<html><body><p>Sector</p></body></html>")
    assert campos["sector"] == "N/R"
    for campo in ("sitio_web", "tamano", "sede", "tipo", "fundacion",
                  "especialidades"):
        assert campos[campo] == "N/R"
    assert campos["descripcion"] == "N/R"


def test_descripcion_colapsa_espacios_y_se_acota() -> None:
    largo = "palabra " * 600
    html = '{"description":"' + largo.replace(" ", r"\n") + '"}'
    descripcion = _extraer_campos(html)["descripcion"]
    assert len(descripcion) <= 2_000
    assert "\n" not in descripcion


# ------------------------------------------------------------- orquestacion


@pytest.fixture
def dormir(monkeypatch: pytest.MonkeyPatch) -> list[float]:
    esperas: list[float] = []
    monkeypatch.setattr("time.sleep", esperas.append)
    return esperas


def test_exito_persiste_y_cachea(
    dormir: list[float], monkeypatch: pytest.MonkeyPatch
) -> None:
    peticiones: list[str] = []

    def handler(peticion: httpx.Request) -> httpx.Response:
        peticiones.append(str(peticion.url))
        return httpx.Response(200, text=HTML_ES + _RELLENO)

    contexto = _contexto({"profundidad_catalogo_empresa": 0,
                          "pausa_entre_empresas_segundos": 2})
    _insertar_empresa()
    cliente = _cliente(handler)
    url = "https://www.linkedin.com/company/deel?trk=public_jobs"
    enriquecer_empresa(contexto, "EMP-0001", url, cliente)
    enriquecer_empresa(contexto, "EMP-0001", url, cliente)

    assert peticiones == ["https://www.linkedin.com/company/deel"]
    fila = leer_tabla("empresas", {"id": "EMP-0001"})[0]
    assert fila["sitio_web"] == "https://www.deel.com/"
    assert fila["sector"] == "Servicios de recursos humanos"
    assert "EMP-0001" in contexto.cache_empresas_enriquecidas
    assert dormir == [2.0]


def test_bloqueo_una_vez_reintenta_y_persiste(
    dormir: list[float], monkeypatch: pytest.MonkeyPatch
) -> None:
    intentos: list[int] = []

    def handler(peticion: httpx.Request) -> httpx.Response:
        intentos.append(1)
        if len(intentos) == 1:
            return httpx.Response(999)
        return httpx.Response(200, text=HTML_EN + _RELLENO)

    _insertar_empresa()
    enriquecer_empresa(
        _contexto(), "EMP-0001",
        "https://www.linkedin.com/company/acme", _cliente(handler),
    )
    assert len(intentos) == 2
    assert dormir[-1] == 40.0
    fila = leer_tabla("empresas", {"id": "EMP-0001"})[0]
    assert fila["sector"] == "Industrial Machinery Manufacturing"


def test_bloqueo_doble_queda_pendiente_para_autocuracion(
    dormir: list[float],
) -> None:
    intentos: list[int] = []

    def handler(peticion: httpx.Request) -> httpx.Response:
        intentos.append(1)
        return httpx.Response(999)

    contexto = _contexto()
    url = "https://www.linkedin.com/company/acme"
    enriquecer_empresa(contexto, "EMP-0001", url, _cliente(handler))
    enriquecer_empresa(contexto, "EMP-0001", url, _cliente(handler))

    assert len(intentos) == 2
    assert "EMP-0001" in contexto.cache_empresas_fallidas
    assert "EMP-0001" not in contexto.cache_empresas_enriquecidas


def test_fallo_de_persistencia_queda_pendiente(
    monkeypatch: pytest.MonkeyPatch, dormir: list[float]
) -> None:
    peticiones: list[str] = []

    def handler(peticion: httpx.Request) -> httpx.Response:
        peticiones.append(str(peticion.url))
        return httpx.Response(200, text=HTML_ES + _RELLENO)

    def _explotar(*args: Any, **kwargs: Any) -> None:
        raise RuntimeError("bd caida")

    _insertar_empresa()
    monkeypatch.setattr(enriquecimiento_mod, "actualizar_fila", _explotar)
    contexto = _contexto()
    url = "https://www.linkedin.com/company/deel"
    enriquecer_empresa(contexto, "EMP-0001", url, _cliente(handler))
    enriquecer_empresa(contexto, "EMP-0001", url, _cliente(handler))

    assert len(peticiones) == 1
    assert "EMP-0001" in contexto.cache_empresas_fallidas
    fila = leer_tabla("empresas", {"id": "EMP-0001"})[0]
    assert fila["sector"] == "N/R"


def test_freno_limita_las_visitas(dormir: list[float]) -> None:
    vistas: list[str] = []

    def handler(peticion: httpx.Request) -> httpx.Response:
        vistas.append(str(peticion.url))
        return httpx.Response(200, text=HTML_ES + _RELLENO)

    contexto = _contexto({"profundidad_catalogo_empresa": 1,
                          "pausa_entre_empresas_segundos": 0})
    _insertar_empresa("EMP-0001", nombre_normalizado="deel")
    _insertar_empresa("EMP-0002", nombre="Acme", nombre_normalizado="acme")
    url = "https://www.linkedin.com/company/x"
    enriquecer_empresa(contexto, "EMP-0001", url, _cliente(handler))
    enriquecer_empresa(contexto, "EMP-0002", url, _cliente(handler))

    assert len(vistas) == 1
    assert contexto.visitas_empresas == 1
    assert "EMP-0002" not in contexto.cache_empresas_fallidas


def test_sin_perfil_no_hace_peticiones() -> None:
    contexto = _contexto()

    def _explota(peticion: httpx.Request) -> httpx.Response:
        raise AssertionError("no debe haber peticiones")

    _insertar_empresa()
    enriquecer_empresa(contexto, "EMP-0001", "N/A", _cliente(_explota))
    assert "EMP-0001" in contexto.cache_empresas_enriquecidas


# --------------------------------------------------- gancho paso 2 (lote a)


def _sesion_simulada(html: str) -> httpx.Client:
    return _cliente(
        lambda peticion: httpx.Response(200, text=html + _RELLENO)
    )


def test_gancho_enriquece_empresa_incompleta(
    monkeypatch: pytest.MonkeyPatch, dormir: list[float]
) -> None:
    _insertar_empresa()
    monkeypatch.setattr(
        preparacion_mod,
        "_obtener_sesion",
        lambda ctx: _sesion_simulada(HTML_ES),
    )
    preparacion_mod._enriquecer_si_aplica(
        _contexto(), "EMP-0001", "https://www.linkedin.com/company/deel"
    )
    fila = leer_tabla("empresas", {"id": "EMP-0001"})[0]
    assert fila["sector"] == "Servicios de recursos humanos"


def test_gancho_omite_empresa_completa(
    monkeypatch: pytest.MonkeyPatch, dormir: list[float]
) -> None:
    _insertar_empresa(sitio_web="https://www.deel.com/")
    llamadas: list[str] = []
    monkeypatch.setattr(
        preparacion_mod,
        "_obtener_sesion",
        lambda ctx: llamadas.append("llamada"),
    )
    preparacion_mod._enriquecer_si_aplica(
        _contexto(), "EMP-0001", "https://www.linkedin.com/company/deel"
    )
    assert llamadas == []


def test_gancho_interrumpido_no_aborta(
    monkeypatch: pytest.MonkeyPatch, dormir: list[float]
) -> None:
    _insertar_empresa()

    def _explota(ctx: Any) -> httpx.Client:
        raise RuntimeError("sesion caida")

    monkeypatch.setattr(preparacion_mod, "_obtener_sesion", _explota)
    contexto = _contexto()
    preparacion_mod._enriquecer_si_aplica(
        contexto, "EMP-0001", "https://www.linkedin.com/company/deel"
    )
    assert "EMP-0001" in contexto.cache_empresas_fallidas


def test_gancho_con_empresa_inexistente_no_toca_sesion(
    monkeypatch: pytest.MonkeyPatch, dormir: list[float]
) -> None:
    llamadas: list[str] = []
    monkeypatch.setattr(
        preparacion_mod,
        "_obtener_sesion",
        lambda ctx: llamadas.append("llamada"),
    )
    preparacion_mod._enriquecer_si_aplica(
        _contexto(), "EMP-9999", "https://www.linkedin.com/company/x"
    )
    assert llamadas == []
