from pathlib import Path

import pytest

from modules.discovery.adapters.linkedin import _URL_LOGIN, FlowError, LinkedInAdapter
from shared.models import FichaFuente, PoliticasCaptura, SetFiltros

FIXTURES = Path(__file__).resolve().parent / "fixtures"

URL_BUSQUEDA = "https://www.linkedin.com/jobs/search"

URL_CON_FILTROS = (
    "https://www.linkedin.com/jobs/search?keywords=Data+Engineer&f_WT=2"
)


def _leer(nombre: str) -> str:
    return (FIXTURES / nombre).read_text(encoding="utf-8")


class FakePage:
    """Playwright-like page served from a dict of URL -> HTML."""

    def __init__(self, por_url: dict[str, str]) -> None:
        self.por_url = por_url
        self._actual = ""
        self.gotos: list[str] = []
        self.cerrada = False
        self.keyboard = FakeKeyboard()

    def goto(self, enlace: str) -> None:
        self.gotos.append(enlace)
        self._actual = self.por_url.get(enlace, "")

    def content(self) -> str:
        return self._actual

    def fill(self, selector: str, valor: str) -> None:
        pass

    def click(self, selector: str) -> None:
        pass

    def wait_for_selector(
        self,
        selector: str,
        timeout: int | None = None,
        state: str | None = None,
    ) -> None:
        pass

    def wait_for_timeout(self, ms: int) -> None:
        pass

    def close(self) -> None:
        self.cerrada = True


class FakeKeyboard:
    """Playwright-like keyboard stub with no-op press."""

    def press(self, tecla: str) -> None:
        pass


@pytest.fixture
def ficha_publica() -> FichaFuente:
    return FichaFuente(
        fuente_id="linkedin",
        nombre="LinkedIn",
        enlace="https://www.linkedin.com/jobs/search",
        tipo_acceso="publico",
        criterio_exito="global-nav",
        timeout_segundos=5,
    )


@pytest.fixture
def ficha_autenticada() -> FichaFuente:
    return FichaFuente(
        fuente_id="linkedin",
        nombre="LinkedIn",
        enlace="https://www.linkedin.com/jobs/search",
        tipo_acceso="con_autenticacion",
        credenciales_referencia=["LINKEDIN_EMAIL", "LINKEDIN_PASSWORD"],
        criterio_exito="global-nav",
        timeout_segundos=5,
    )


@pytest.fixture
def set_filtros() -> SetFiltros:
    return SetFiltros(
        fuente_id="linkedin",
        indice=0,
        filtros=[
            {"tipo": "keywords", "valor": ["Data Engineer"]},
            {"tipo": "modalidad", "valor": "remoto"},
        ],
    )


@pytest.fixture
def politicas() -> PoliticasCaptura:
    return PoliticasCaptura(
        max_paginas=2,
        max_ofertas_por_corrida=2,
        pausa_entre_lotes_segundos=0,
        estrategia_anti_bloqueo="none",
    )


def test_enter_source_exito(ficha_publica: FichaFuente) -> None:
    pagina = FakePage({ficha_publica.enlace: _leer("lista_linkedin.html")})
    resultado = LinkedInAdapter().enter_source(pagina, ficha_publica)
    assert resultado.estado == "exito"


def test_enter_source_autenticada_sin_credenciales(
    ficha_autenticada: FichaFuente,
) -> None:
    pagina = FakePage({ficha_autenticada.enlace: _leer("lista_linkedin.html")})
    with pytest.raises(FlowError) as exc:
        LinkedInAdapter().enter_source(pagina, ficha_autenticada)
    assert exc.value.codigo_motivo == "credenciales_no_disponibles"


def test_enter_source_autenticada_con_credenciales(
    ficha_autenticada: FichaFuente,
) -> None:
    pagina = FakePage(
        {
            URL_BUSQUEDA: _leer("lista_linkedin.html"),
            _URL_LOGIN: "<html><body>global-nav login</body></html>",
        }
    )
    resultado = LinkedInAdapter().enter_source(
        pagina,
        ficha_autenticada,
        {"username": "usuario", "password": "clave"},
    )
    assert resultado.estado == "exito"
    assert pagina.gotos == [_URL_LOGIN]


def test_enter_source_criterio_no_cumplido() -> None:
    pagina = FakePage({"https://x.com": "<html><body>sin nav</body></html>"})
    ficha = FichaFuente(
        fuente_id="x",
        nombre="X",
        enlace="https://x.com",
        tipo_acceso="publico",
        criterio_exito="global-nav",
    )
    with pytest.raises(FlowError) as exc:
        LinkedInAdapter().enter_source(pagina, ficha)
    assert exc.value.codigo_motivo == "criterio_no_cumplido"


def test_enter_source_bloqueo_captcha() -> None:
    pagina = FakePage({"https://www.linkedin.com/jobs/search": _leer("challenge_linkedin.html")})
    ficha_fuente = FichaFuente(
        fuente_id="linkedin",
        nombre="LinkedIn",
        enlace="https://www.linkedin.com/jobs/search",
        tipo_acceso="publico",
        criterio_exito="global-nav",
    )
    with pytest.raises(FlowError) as exc:
        LinkedInAdapter().enter_source(pagina, ficha_fuente)
    assert exc.value.codigo_motivo == "bloqueo_plataforma"


def test_apply_filters_parsea_resultados(
    ficha_publica: FichaFuente,
    set_filtros: SetFiltros,
    politicas: PoliticasCaptura,
) -> None:
    pagina = FakePage({URL_CON_FILTROS: _leer("lista_linkedin.html")})
    resultado = LinkedInAdapter().apply_filters(pagina, ficha_publica, set_filtros, politicas)
    assert resultado.estado == "exito"
    assert len(resultado.ofertas_primera_pagina) == 2
    oferta = resultado.ofertas_primera_pagina[0]
    assert oferta.titulo == "Data Engineer"
    assert oferta.id_externo == "12345"
    assert oferta.enlace == "https://www.linkedin.com/jobs/view/12345"
    assert resultado.total_declarado == 2
    assert pagina.gotos[-1] == URL_CON_FILTROS


def test_apply_filters_bloqueo(
    ficha_publica: FichaFuente, set_filtros: SetFiltros, politicas: PoliticasCaptura
) -> None:
    pagina = FakePage({URL_CON_FILTROS: _leer("challenge_linkedin.html")})
    with pytest.raises(FlowError) as exc:
        LinkedInAdapter().apply_filters(pagina, ficha_publica, set_filtros, politicas)
    assert exc.value.codigo_motivo == "bloqueo_plataforma"


def test_apply_filters_parsea_resultados_ssr_2026(
    ficha_publica: FichaFuente,
    set_filtros: SetFiltros,
    politicas: PoliticasCaptura,
) -> None:
    pagina = FakePage({URL_CON_FILTROS: _leer("lista_linkedin_sesion.html")})
    resultado = LinkedInAdapter().apply_filters(pagina, ficha_publica, set_filtros, politicas)
    assert resultado.estado == "exito"
    assert len(resultado.ofertas_primera_pagina) == 2
    oferta = resultado.ofertas_primera_pagina[0]
    assert oferta.titulo == "Oferta Uno"
    assert oferta.id_externo == "77701"
    assert oferta.enlace == "https://www.linkedin.com/jobs/view/77701/?refId=abc"
    assert resultado.total_declarado is None


def test_apply_filters_fallback_enlace_generico(
    ficha_publica: FichaFuente,
    set_filtros: SetFiltros,
    politicas: PoliticasCaptura,
) -> None:
    html = "<html><body><a href='/jobs/view/99901'>Titulo Generico</a></body></html>"
    pagina = FakePage({URL_CON_FILTROS: html})
    resultado = LinkedInAdapter().apply_filters(pagina, ficha_publica, set_filtros, politicas)
    assert len(resultado.ofertas_primera_pagina) == 1
    assert resultado.ofertas_primera_pagina[0].titulo == "Titulo Generico"


def test_capture_batch_detalle_ssr_2026(
    ficha_publica: FichaFuente,
    set_filtros: SetFiltros,
    politicas: PoliticasCaptura,
) -> None:
    pagina = FakePage(
        {
            URL_CON_FILTROS: _leer("lista_linkedin_sesion.html"),
            "https://www.linkedin.com/jobs/view/77701/?refId=abc": _leer(
                "detalle_linkedin_sesion.html"
            ),
            "https://www.linkedin.com/jobs/view/77702/": _leer(
                "detalle_linkedin_sesion.html"
            ),
        }
    )
    lote, estado = LinkedInAdapter().capture_batch(
        pagina, ficha_publica, set_filtros, politicas
    )
    assert estado.estado == "ok"
    assert len(lote.ofertas) == 2
    assert lote.ofertas[0].titulo == "Oferta Uno"
    assert lote.ofertas[0].id_externo == "77701"
    assert "analítica" in lote.ofertas[0].descripcion_original


def test_apply_filters_filtro_tipo_no_soportado(
    ficha_publica: FichaFuente, politicas: PoliticasCaptura
) -> None:
    set_no_soportado = SetFiltros(
        fuente_id=ficha_publica.fuente_id,
        indice=0,
        filtros=[{"tipo": "salario", "valor": "50000"}],
    )
    pagina = FakePage({})
    with pytest.raises(FlowError) as exc:
        LinkedInAdapter().apply_filters(pagina, ficha_publica, set_no_soportado, politicas)
    assert exc.value.codigo_motivo == "filtros_no_aplicables"


def test_apply_filters_filtro_valor_vacio_se_ignora(
    ficha_publica: FichaFuente, politicas: PoliticasCaptura
) -> None:
    set_valor_vacio = SetFiltros(
        fuente_id=ficha_publica.fuente_id,
        indice=0,
        filtros=[
            {"tipo": "keywords", "valor": ""},
            {"tipo": "modalidad", "valor": "remoto"},
        ],
    )
    url_solo_modalidad = "https://www.linkedin.com/jobs/search?f_WT=2"
    pagina = FakePage({url_solo_modalidad: _leer("lista_linkedin.html")})
    resultado = LinkedInAdapter().apply_filters(pagina, ficha_publica, set_valor_vacio, politicas)
    assert resultado.estado == "exito"
    assert pagina.gotos[-1] == url_solo_modalidad


def test_capture_batch_captura_dos_ofertas(
    ficha_publica: FichaFuente,
    set_filtros: SetFiltros,
    politicas: PoliticasCaptura,
) -> None:
    pagina = FakePage(
        {
            URL_CON_FILTROS: _leer("lista_linkedin.html"),
            "https://www.linkedin.com/jobs/view/12345": _leer("detalle_linkedin.html"),
            "https://www.linkedin.com/jobs/view/12346": _leer("detalle_linkedin.html"),
        }
    )
    lote, estado = LinkedInAdapter().capture_batch(
        pagina, ficha_publica, set_filtros, politicas
    )
    assert estado.estado == "ok"
    assert estado.limite_alcanzado
    assert len(lote.ofertas) == 2
    assert lote.ofertas[0].titulo == "Data Engineer"
    assert lote.ofertas[0].descripcion_original != ""
    assert lote.ofertas[0].id_externo == "12345"
    assert lote.paginas_consumidas == 1


def test_capture_batch_oferta_sin_titulo_se_excluye_y_genera_evento(
    ficha_publica: FichaFuente,
    set_filtros: SetFiltros,
    politicas: PoliticasCaptura,
) -> None:
    pagina = FakePage(
        {
            URL_CON_FILTROS: _leer("lista_linkedin.html"),
            "https://www.linkedin.com/jobs/view/12345": "<html><body>x</body></html>",
            "https://www.linkedin.com/jobs/view/12346": _leer("detalle_linkedin.html"),
            f"{URL_CON_FILTROS}&start=2": "<html><body><nav id='global-nav'></nav></body></html>",
        }
    )
    adaptador = LinkedInAdapter()
    lote, estado = adaptador.capture_batch(pagina, ficha_publica, set_filtros, politicas)
    assert len(lote.ofertas) == 1
    assert any(e.codigo == "EVT-01" for e in adaptador.eventos_declarados)


def test_capture_batch_aplica_pausa_entre_lotes(
    ficha_publica: FichaFuente, set_filtros: SetFiltros
) -> None:
    llamadas: list[float] = []

    def dormir(segundos: float) -> None:
        llamadas.append(segundos)

    politicas = PoliticasCaptura(
        max_paginas=3,
        max_ofertas_por_corrida=2,
        pausa_entre_lotes_segundos=2,
        estrategia_anti_bloqueo="retraso_fijo",
    )
    pagina = FakePage(
        {
            URL_CON_FILTROS: _leer("lista_linkedin.html"),
            "https://www.linkedin.com/jobs/view/12345": _leer("detalle_linkedin.html"),
            "https://www.linkedin.com/jobs/view/12346": _leer("detalle_linkedin.html"),
        }
    )
    adaptador = LinkedInAdapter(sleep_fn=dormir)
    adaptador.capture_batch(pagina, ficha_publica, set_filtros, politicas)
    assert llamadas and llamadas[0] == 2.0


def test_close_session_cierra_pagina() -> None:
    pagina = FakePage({})
    LinkedInAdapter().close_session(pagina)
    assert pagina.cerrada


def test_capture_batch_bloqueo_detiene_batch(
    ficha_publica: FichaFuente,
    set_filtros: SetFiltros,
    politicas: PoliticasCaptura,
) -> None:
    pagina = FakePage({URL_CON_FILTROS: _leer("challenge_linkedin.html")})
    with pytest.raises(FlowError) as exc:
        LinkedInAdapter().capture_batch(pagina, ficha_publica, set_filtros, politicas)
    assert exc.value.codigo_motivo == "bloqueo_plataforma"
