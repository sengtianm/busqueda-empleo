from pathlib import Path

import pytest

from modules.discovery.adapters.linkedin import _URL_LOGIN, FlowError, LinkedInAdapter
from shared.models import FichaFuente, PoliticasCaptura, SetFiltros

FIXTURES = Path(__file__).resolve().parent / "fixtures"

URL_BUSQUEDA = "https://www.linkedin.com/jobs/search"

URL_CON_FILTROS = (
    "https://www.linkedin.com/jobs/search?keywords=Data+Engineer&f_WT=2"
)

URL_RESULTADOS = URL_CON_FILTROS.replace(
    "https://www.linkedin.com/jobs/search",
    "https://www.linkedin.com/jobs/search-results/",
)


def _leer(nombre: str) -> str:
    return (FIXTURES / nombre).read_text(encoding="utf-8")


class FakePage:
    """Playwright-like page served from a dict of URL -> HTML."""

    def __init__(self, por_url: dict[str, str]) -> None:
        self.por_url = por_url
        self._actual = ""
        self.url = ""
        self.gotos: list[str] = []
        self.cerrada = False
        self.keyboard = FakeKeyboard()
        self.esperas: list[tuple[str, str | None, int | None]] = []

    def goto(self, enlace: str, wait_until: str | None = None) -> None:
        self.gotos.append(enlace)
        self.url = enlace
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
        self.esperas.append((selector, state, timeout))

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


def test_capture_batch_lista_ssr_2026(
    ficha_publica: FichaFuente,
    set_filtros: SetFiltros,
    politicas: PoliticasCaptura,
) -> None:
    pagina = FakePage({URL_RESULTADOS: _leer("lista_linkedin_sesion.html")})
    lote, estado = LinkedInAdapter().capture_batch(
        pagina, ficha_publica, set_filtros, politicas
    )
    assert estado.estado == "ok"
    assert len(lote.ofertas) == 2
    assert lote.ofertas[0].titulo == "Oferta Uno"
    assert lote.ofertas[0].id_externo == "77701"
    assert lote.ofertas[0].descripcion_original == ""
    assert not any("/jobs/view/" in enlace for enlace in pagina.gotos)


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
    pagina = FakePage({URL_RESULTADOS: _leer("lista_linkedin.html")})
    lote, estado = LinkedInAdapter().capture_batch(
        pagina, ficha_publica, set_filtros, politicas
    )
    assert estado.estado == "ok"
    assert estado.limite_alcanzado
    assert len(lote.ofertas) == 2
    assert lote.ofertas[0].titulo == "Data Engineer"
    assert lote.ofertas[0].descripcion_original == ""
    assert lote.ofertas[0].id_externo == "12345"
    assert lote.paginas_consumidas == 1


def test_capture_batch_tarjeta_sin_titulo_se_excluye(
    ficha_publica: FichaFuente,
    set_filtros: SetFiltros,
    politicas: PoliticasCaptura,
) -> None:
    html = (
        "<html><body>"
        "<div componentkey='job-card-component-ref-99901'>"
        "<div componentkey='job-card-component-ref-99901'><p>sin titulo</p></div>"
        "</div>"
        "</body></html>"
    )
    pagina = FakePage({URL_RESULTADOS: html})
    adaptador = LinkedInAdapter()
    lote, estado = adaptador.capture_batch(pagina, ficha_publica, set_filtros, politicas)
    assert estado.estado == "ok"
    assert len(lote.ofertas) == 0
    assert adaptador.eventos_declarados == []


def test_capture_batch_recorre_paginas_hasta_ultima(
    ficha_publica: FichaFuente,
    set_filtros: SetFiltros,
) -> None:
    politicas = PoliticasCaptura(
        max_paginas=10,
        max_ofertas_por_corrida=10,
        pausa_entre_lotes_segundos=0,
        estrategia_anti_bloqueo="none",
    )
    pagina = FakePage(
        {
            URL_RESULTADOS: _leer("lista_linkedin_sdui_2026.html"),
            f"{URL_RESULTADOS}&start=3": _leer("lista_linkedin_sdui_2026_pag2.html"),
            f"{URL_RESULTADOS}&start=5": "<html><body><div>sin resultados</div></body></html>",
        }
    )
    lote, estado = LinkedInAdapter().capture_batch(
        pagina, ficha_publica, set_filtros, politicas
    )
    assert estado.estado == "ok"
    assert len(lote.ofertas) == 5
    assert lote.paginas_consumidas == 2
    assert f"{URL_RESULTADOS}&start=3" in pagina.gotos
    assert f"{URL_RESULTADOS}&start=5" not in pagina.gotos
    assert pagina.esperas[0][2] == 5000
    assert pagina.esperas[1][2] == 5000


def test_capture_batch_no_entra_al_detalle(
    ficha_publica: FichaFuente,
    set_filtros: SetFiltros,
) -> None:
    politicas = PoliticasCaptura(
        max_paginas=10,
        max_ofertas_por_corrida=10,
        pausa_entre_lotes_segundos=0,
        estrategia_anti_bloqueo="none",
    )
    pagina = FakePage(
        {
            URL_RESULTADOS: _leer("lista_linkedin_sdui_2026.html"),
            f"{URL_RESULTADOS}&start=3": _leer("lista_linkedin_sdui_2026_pag2.html"),
            f"{URL_RESULTADOS}&start=5": "<html><body><div>sin resultados</div></body></html>",
        }
    )
    lote, estado = LinkedInAdapter().capture_batch(
        pagina, ficha_publica, set_filtros, politicas
    )
    assert estado.estado == "ok"
    assert not any("/jobs/view/" in enlace for enlace in pagina.gotos)
    assert len(lote.ofertas) == 5


def test_capture_batch_pagina_parcial_no_corta_recorrido(
    ficha_publica: FichaFuente,
    set_filtros: SetFiltros,
) -> None:
    politicas = PoliticasCaptura(
        max_paginas=10,
        max_ofertas_por_corrida=10,
        pausa_entre_lotes_segundos=0,
        estrategia_anti_bloqueo="none",
    )
    pagina = FakePage(
        {
            URL_RESULTADOS: _leer("lista_linkedin_sdui_2026.html"),
            f"{URL_RESULTADOS}&start=3": (
                "<html><body>"
                "<div componentkey='job-card-component-ref-99901'>"
                "<div componentkey='job-card-component-ref-99901'>"
                "<span aria-hidden='true'>Oferta Unica</span>"
                "</div></div>"
                "<button aria-label='Siguiente'>Siguiente</button>"
                "</body></html>"
            ),
            f"{URL_RESULTADOS}&start=4": "<html><body><div>sin resultados</div></body></html>",
        }
    )
    lote, estado = LinkedInAdapter().capture_batch(
        pagina, ficha_publica, set_filtros, politicas
    )
    assert len(lote.ofertas) == 4
    assert lote.paginas_consumidas == 2


def test_capture_batch_respeta_max_paginas(
    ficha_publica: FichaFuente,
    set_filtros: SetFiltros,
) -> None:
    politicas = PoliticasCaptura(
        max_paginas=1,
        max_ofertas_por_corrida=10,
        pausa_entre_lotes_segundos=0,
        estrategia_anti_bloqueo="none",
    )
    pagina = FakePage({URL_RESULTADOS: _leer("lista_linkedin_sdui_2026.html")})
    lote, estado = LinkedInAdapter().capture_batch(
        pagina, ficha_publica, set_filtros, politicas
    )
    assert estado.estado == "ok"
    assert len(lote.ofertas) == 3
    assert lote.paginas_consumidas == 1


def test_capture_batch_respeta_max_ofertas(
    ficha_publica: FichaFuente,
    set_filtros: SetFiltros,
    politicas: PoliticasCaptura,
) -> None:
    politica = politicas.model_copy(update={"max_ofertas_por_corrida": 4})
    pagina = FakePage(
        {
            URL_RESULTADOS: _leer("lista_linkedin_sdui_2026.html"),
            f"{URL_RESULTADOS}&start=3": _leer("lista_linkedin_sdui_2026_pag2.html"),
        }
    )
    lote, estado = LinkedInAdapter().capture_batch(
        pagina, ficha_publica, set_filtros, politica
    )
    assert len(lote.ofertas) == 4
    assert lote.paginas_consumidas == 2


def test_capture_batch_dedup_entre_paginas(
    ficha_publica: FichaFuente,
    set_filtros: SetFiltros,
) -> None:
    politicas = PoliticasCaptura(
        max_paginas=10,
        max_ofertas_por_corrida=10,
        pausa_entre_lotes_segundos=0,
        estrategia_anti_bloqueo="none",
    )
    pagina = FakePage(
        {
            URL_RESULTADOS: _leer("lista_linkedin_sdui_2026.html"),
            f"{URL_RESULTADOS}&start=3": (
                "<html><body>"
                "<div componentkey='job-card-component-ref-4415705281'>"
                "<div componentkey='job-card-component-ref-4415705281'>"
                "<span aria-hidden='true'>Data Engineer duplicada</span>"
                "</div></div>"
                "</body></html>"
            ),
        }
    )
    lote, estado = LinkedInAdapter().capture_batch(
        pagina, ficha_publica, set_filtros, politicas
    )
    assert len(lote.ofertas) == 3
    assert estado.estado == "ok"


def test_capture_batch_aplica_pausa_entre_paginas(
    ficha_publica: FichaFuente, set_filtros: SetFiltros
) -> None:
    llamadas: list[float] = []

    def dormir(segundos: float) -> None:
        llamadas.append(segundos)

    politicas = PoliticasCaptura(
        max_paginas=3,
        max_ofertas_por_corrida=10,
        pausa_entre_lotes_segundos=2,
        estrategia_anti_bloqueo="retraso_fijo",
    )
    pagina = FakePage(
        {
            URL_RESULTADOS: _leer("lista_linkedin_sdui_2026.html"),
            f"{URL_RESULTADOS}&start=3": _leer("lista_linkedin_sdui_2026_pag2.html"),
        }
    )
    adaptador = LinkedInAdapter(sleep_fn=dormir)
    adaptador.capture_batch(pagina, ficha_publica, set_filtros, politicas)
    assert llamadas and llamadas[0] == 2.0


def test_capture_batch_reutiliza_pagina_1(
    ficha_publica: FichaFuente,
    set_filtros: SetFiltros,
) -> None:
    politicas = PoliticasCaptura(
        max_paginas=10,
        max_ofertas_por_corrida=10,
        pausa_entre_lotes_segundos=0,
        estrategia_anti_bloqueo="none",
    )
    pagina = FakePage(
        {f"{URL_RESULTADOS}&start=3": "<html><body><div>sin resultados</div></body></html>"}
    )
    pagina.url = URL_RESULTADOS
    pagina._actual = _leer("lista_linkedin_sdui_2026.html")
    lote, estado = LinkedInAdapter().capture_batch(
        pagina, ficha_publica, set_filtros, politicas
    )
    assert estado.estado == "ok"
    assert len(lote.ofertas) == 3
    assert lote.paginas_consumidas == 1
    assert pagina.gotos == [f"{URL_RESULTADOS}&start=3"]


def test_capture_batch_pagina_vacia_con_boton_corta_recorrido(
    ficha_publica: FichaFuente,
    set_filtros: SetFiltros,
) -> None:
    politicas = PoliticasCaptura(
        max_paginas=10,
        max_ofertas_por_corrida=10,
        pausa_entre_lotes_segundos=0,
        estrategia_anti_bloqueo="none",
    )
    pagina = FakePage(
        {
            URL_RESULTADOS: _leer("lista_linkedin_sdui_2026.html"),
            f"{URL_RESULTADOS}&start=3": "<html><body><div>sin resultados</div></body></html>",
        }
    )
    lote, estado = LinkedInAdapter().capture_batch(
        pagina, ficha_publica, set_filtros, politicas
    )
    assert len(lote.ofertas) == 3
    assert lote.paginas_consumidas == 1
    assert f"{URL_RESULTADOS}&start=3" in pagina.gotos


def test_capture_batch_aplica_tope_espera_paginas_sucesivas(
    ficha_publica: FichaFuente,
    set_filtros: SetFiltros,
) -> None:
    politicas = PoliticasCaptura(
        max_paginas=10,
        max_ofertas_por_corrida=10,
        pausa_entre_lotes_segundos=0,
        estrategia_anti_bloqueo="none",
    )
    ficha = ficha_publica.model_copy(update={"timeout_segundos": 30})
    pagina = FakePage(
        {
            URL_RESULTADOS: _leer("lista_linkedin_sdui_2026.html"),
            f"{URL_RESULTADOS}&start=3": _leer("lista_linkedin_sdui_2026_pag2.html"),
        }
    )
    LinkedInAdapter().capture_batch(pagina, ficha, set_filtros, politicas)
    assert pagina.esperas[0][2] == 30000
    assert pagina.esperas[1][2] == 10000


def test_close_session_cierra_pagina() -> None:
    pagina = FakePage({})
    LinkedInAdapter().close_session(pagina)
    assert pagina.cerrada


def test_capture_batch_bloqueo_detiene_batch(
    ficha_publica: FichaFuente,
    set_filtros: SetFiltros,
    politicas: PoliticasCaptura,
) -> None:
    pagina = FakePage({URL_RESULTADOS: _leer("challenge_linkedin.html")})
    with pytest.raises(FlowError) as exc:
        LinkedInAdapter().capture_batch(pagina, ficha_publica, set_filtros, politicas)
    assert exc.value.codigo_motivo == "bloqueo_plataforma"


def test_revisar_bloqueo_ignora_challenge_en_scripts() -> None:
    html = (
        "<html><head><script>var mod = 'challenge-response';</script>"
        "<style>.challenge{color:red}</style></head>"
        "<body><nav id='global-nav'>ok</nav></body></html>"
    )
    LinkedInAdapter()._revisar_bloqueo_html(html)


def test_revisar_bloqueo_detecta_captcha_visible() -> None:
    html = "<html><body><p>Complete the captcha to continue.</p></body></html>"
    with pytest.raises(FlowError) as exc:
        LinkedInAdapter()._revisar_bloqueo_html(html)
    assert exc.value.codigo_motivo == "bloqueo_plataforma"


def test_revisar_bloqueo_ignora_authwall_en_scripts() -> None:
    html = "<html><head><script>const authwall = true;</script></head><body>ok</body></html>"
    LinkedInAdapter()._revisar_bloqueo_html(html)


def test_revisar_bloqueo_detecta_authwall_visible() -> None:
    html = "<html><body><div class='authwall-content'>unete</div></body></html>"
    with pytest.raises(FlowError) as exc:
        LinkedInAdapter()._revisar_bloqueo_html(html)
    assert exc.value.codigo_motivo == "sesion_expirada"


class FakePageRenderizadoTardio(FakePage):
    """Simula el SERP 2026: las tarjetas aparecen al esperar el selector."""

    def __init__(self, cascaron: str, renderizado: str) -> None:
        super().__init__({})
        self._cascaron = cascaron
        self._renderizado = renderizado
        self._actual = cascaron
        self.esperas: list[tuple[str, str | None, int | None]] = []

    def goto(self, enlace: str, wait_until: str | None = None) -> None:
        self.gotos.append(enlace)
        self.url = enlace
        self._actual = self.por_url.get(enlace, self._cascaron)

    def wait_for_selector(
        self,
        selector: str,
        timeout: int | None = None,
        state: str | None = None,
    ) -> None:
        self.esperas.append((selector, state, timeout))
        self._actual = self._renderizado


def test_apply_filters_espera_renderizado_tardio(
    ficha_publica: FichaFuente,
    set_filtros: SetFiltros,
    politicas: PoliticasCaptura,
) -> None:
    cascaron = "<html><body><p>cargando resultados...</p></body></html>"
    pagina = FakePageRenderizadoTardio(cascaron, _leer("lista_linkedin.html"))
    resultado = LinkedInAdapter().apply_filters(pagina, ficha_publica, set_filtros, politicas)
    assert resultado.estado == "exito"
    assert len(resultado.ofertas_primera_pagina) == 2
    assert pagina.esperas and pagina.esperas[0][0].startswith("div[componentkey^='job-card")


def test_apply_filters_espera_renderizado_tardio_ssr_2026(
    ficha_publica: FichaFuente,
    set_filtros: SetFiltros,
    politicas: PoliticasCaptura,
) -> None:
    cascaron = "<html><body><div id='root'></div></body></html>"
    pagina = FakePageRenderizadoTardio(cascaron, _leer("lista_linkedin_sesion.html"))
    resultado = LinkedInAdapter().apply_filters(pagina, ficha_publica, set_filtros, politicas)
    assert resultado.estado == "exito"
    assert len(resultado.ofertas_primera_pagina) == 2


def test_apply_filters_parsea_resultados_sdui_2026(
    ficha_publica: FichaFuente,
    set_filtros: SetFiltros,
    politicas: PoliticasCaptura,
) -> None:
    pagina = FakePage({URL_CON_FILTROS: _leer("lista_linkedin_sdui_2026.html")})
    resultado = LinkedInAdapter().apply_filters(pagina, ficha_publica, set_filtros, politicas)
    assert resultado.estado == "exito"
    ofertas = resultado.ofertas_primera_pagina
    assert len(ofertas) == 3
    assert ofertas[0].titulo == "Data Engineer"
    assert ofertas[0].id_externo == "4415705281"
    assert ofertas[0].enlace == "https://www.linkedin.com/jobs/view/4415705281"
    assert ofertas[1].titulo == "Data Engineer (Ingeniero de Datos)"
    assert ofertas[1].id_externo == "4449035947"
    assert ofertas[2].id_externo == "4450160439"
    assert resultado.total_declarado is None


def test_apply_filters_sdui_ignora_apply_y_anchors_duplicados(
    ficha_publica: FichaFuente,
    set_filtros: SetFiltros,
    politicas: PoliticasCaptura,
) -> None:
    pagina = FakePage({URL_CON_FILTROS: _leer("lista_linkedin_sdui_2026.html")})
    resultado = LinkedInAdapter().apply_filters(pagina, ficha_publica, set_filtros, politicas)
    assert len(resultado.ofertas_primera_pagina) == 3


def test_capture_batch_espera_renderizado_tardio(
    ficha_publica: FichaFuente,
    set_filtros: SetFiltros,
    politicas: PoliticasCaptura,
) -> None:
    cascaron = "<html><body><p>cargando...</p></body></html>"
    pagina = FakePageRenderizadoTardio(cascaron, _leer("lista_linkedin.html"))
    pagina.por_url = {
        "https://www.linkedin.com/jobs/view/12345": _leer("detalle_linkedin.html"),
        "https://www.linkedin.com/jobs/view/12346": _leer("detalle_linkedin.html"),
    }
    lote, estado = LinkedInAdapter().capture_batch(
        pagina, ficha_publica, set_filtros, politicas
    )
    assert estado.estado == "ok"
    assert len(lote.ofertas) == 2
    assert pagina.esperas


def test_capture_batch_espera_por_cada_pagina(
    ficha_publica: FichaFuente,
    set_filtros: SetFiltros,
    politicas: PoliticasCaptura,
) -> None:
    pagina = FakePageRenderizadoTardio(
        "<html><body><p>cargando...</p></body></html>", _leer("lista_linkedin.html")
    )
    pagina.por_url = {
        "https://www.linkedin.com/jobs/view/12345": _leer("detalle_linkedin.html"),
        "https://www.linkedin.com/jobs/view/12346": _leer("detalle_linkedin.html"),
    }
    LinkedInAdapter().capture_batch(pagina, ficha_publica, set_filtros, politicas)
    assert len(pagina.esperas) >= 1


def test_esperar_resultados_usa_timeout_de_ficha() -> None:
    pagina = FakePage({})
    adaptador = LinkedInAdapter()
    ficha = FichaFuente(
        fuente_id="linkedin",
        nombre="LinkedIn",
        enlace="https://www.linkedin.com/jobs/search",
        tipo_acceso="publico",
        criterio_exito="global-nav",
        timeout_segundos=5,
    )
    adaptador._esperar_resultados(pagina, ficha.timeout_segundos)
    assert pagina.esperas == [(
        "div[componentkey^='job-card-component-ref-']",
        "attached",
        5000,
    )]


def test_esperar_resultados_tolerante_a_timeout() -> None:
    class PageSinTarjetas(FakePage):
        def wait_for_selector(
            self,
            selector: str,
            timeout: int | None = None,
            state: str | None = None,
        ) -> None:
            raise TimeoutError("no cards")

    pagina = PageSinTarjetas({})
    LinkedInAdapter()._esperar_resultados(pagina, 5)
    assert not pagina.cerrada
