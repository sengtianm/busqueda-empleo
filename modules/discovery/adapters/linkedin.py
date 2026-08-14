"""LinkedIn platform adapter (INT-001/INT-003, DOC-12).

Encapsulates the LinkedIn integration contract of the discovery nodes
"Entrar a la fuente", "Aplicar filtros" and "Capturar ofertas" (DOC-04
Section 15, DOC-09 Section 6): URL construction from the official filter sets,
parsing of the search/detail HTML and incremental capture with pauses (RN-10),
classifying failures with the official `codigo_motivo` catalog (DOC-06,
Section 11). Navigation runs on an injected `page` object (Playwright
Page-like), so the adapter is testable with HTML fixtures and a fake page,
without network or database access.

Expected platform failures raise `FlowError` with the official
`codigo_motivo`; `shared.retry.retry_conditional` retries only
`fuente_inalcanzable`/`timeout_*`. Grupo A codes (`bloqueo_plataforma`,
`sesion_expirada`, `criterio_no_cumplido`, ...) are never retried.
"""

import random
import re
import time
from collections.abc import Callable
from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from bs4 import BeautifulSoup
from loguru import logger

from shared.models import (
    CaptureBatch,
    EntryResult,
    EstadoCaptura,
    FichaFuente,
    Offer,
    PoliticasCaptura,
    SearchResult,
    SetFiltros,
)
from shared.utilidades import acotar_evidencia

_PARAMETROS_FILTROS: dict[str, str] = {
    "keywords": "keywords",
    "ubicacion": "location",
    "modalidad": "f_WT",
    "fecha_publicacion": "f_TPR",
    "nivel_experiencia": "f_JT",
}

_MODALIDAD_F_WT: dict[str, str] = {
    "presencial": "1",
    "remoto": "2",
    "hibrido": "3",
}

_SEL_ENLACE_TARJETA = "a.base-search-card__link"
_SEL_ENLACE_TARJETA_2026 = "div.job-card-container a.job-card-container__link"
_SEL_ENLACE_TARJETA_GENERICO = "a[href*='/jobs/view/']"
_SEL_TARJETA_SDUI = "div[componentkey^='job-card-component-ref-']"
_SEL_TITULO_TARJETA = ".base-search-card__title"
_SEL_EMPRESA_TARJETA = ".base-search-card__subtitle"
_SEL_UBICACION_TARJETA = ".base-search-card__location"
_SEL_TOTAL_RESULTADOS = "span.jobs-search-results__total-count"
_SEL_SIGUIENTE = (
    "button[aria-label='Next']",
    "a[aria-label='Next']",
    "button[aria-label='Siguiente']",
    "a[aria-label='Siguiente']",
    "button[aria-label^='Página ']",
    "a[aria-label^='Página ']",
)

_RE_ID_EXTERNO = re.compile(r"/jobs/view/(\d+)")
_RE_ID_COMPONENTE = re.compile(r"job-card-component-ref-(\d+)")

_URL_LOGIN = "https://www.linkedin.com/login/es/?fromSignIn=true"
_URL_JOBS_VIEW = "https://www.linkedin.com/jobs/view"

_RE_FECHA_PUBLICACION = re.compile(r"^r\d+$")


class FlowError(Exception):
    """Expected platform failure carrying a DOC-06 `codigo_motivo`."""

    def __init__(self, codigo_motivo: str, mensaje: str) -> None:
        self.codigo_motivo = codigo_motivo
        self.mensaje = mensaje
        super().__init__(mensaje)


class LinkedInAdapter:
    """Platform adapter that maps LinkedIn into the discovery contracts."""

    def __init__(self, sleep_fn: Callable[[float], None] = time.sleep) -> None:
        self._sleep = sleep_fn

    # ----------------------------- entrance ----------------------------- #

    def enter_source(
        self,
        page: Any,
        ficha: FichaFuente,
        credenciales: dict[str, str] | None = None,
    ) -> EntryResult:
        """Enter the source and verify the DOC-09 Section 6.1 entry criteria."""
        if ficha.tipo_acceso == "con_autenticacion":
            if not credenciales:
                raise FlowError(
                    "credenciales_no_disponibles",
                    "Authenticated source without credentials.",
                )
            self._autenticar(page, credenciales)
            self._esperar_criterio_ingreso(page, ficha)
            return EntryResult(
                estado="exito",
                evidencia_acotada=f"criterio: {ficha.criterio_exito}",
                numero_de_intentos=1,
            )
        try:
            page.goto(ficha.enlace)
        except Exception as exc:
            raise FlowError("fuente_inalcanzable", f"Entry navigation failed: {exc}") from exc
        if not self._criterio_ingreso_cumplido(page, ficha):
            raise FlowError(
                "criterio_no_cumplido",
                f"Entry criterion '{ficha.criterio_exito}' not verified.",
            )
        return EntryResult(
            estado="exito",
            evidencia_acotada=f"criterio: {ficha.criterio_exito}",
            numero_de_intentos=1,
        )

    def _esperar_resultados(self, page: Any, timeout_segundos: int) -> None:
        """Espera a que el listado de tarjetas se renderice antes de parsear.

        LinkedIn 2026 renderiza el SERP de forma asincrona (SDUi): al navegar,
        el DOM inicial es el cascaron sin tarjetas; el listado (tarjetas
        ``componentkey``) aparece ~3-6s despues. Sin esta espera el parseo
        devolveria 0 ofertas reales. Si expira el timeout (pagina
        verdaderamente vacia), se continua y el resultado sera 0 ofertas
        legitimo.
        """
        try:
            page.wait_for_selector(
                _SEL_TARJETA_SDUI, state="attached", timeout=timeout_segundos * 1000
            )
        except Exception:
            pass

    def apply_filters(
        self,
        page: Any,
        ficha: FichaFuente,
        set_filtros: SetFiltros,
        politicas: PoliticasCaptura,
    ) -> SearchResult:
        """Apply the official filter set and parse the first results page."""
        enlace = self._construir_url_busqueda(ficha.enlace, set_filtros)
        try:
            page.goto(enlace)
        except Exception as exc:
            raise FlowError("fuente_inalcanzable", f"Search navigation failed: {exc}") from exc
        self._esperar_resultados(page, ficha.timeout_segundos)
        html = self._contenido(page)
        self._revisar_estado_pagina(html, "tiempo_agotado_consulta")
        resultado = self._parsear_resultados(html, ficha, set_filtros, enlace)
        logger.info(
            f"Busqueda aplicada | url={enlace} | "
            f"total_declarado={resultado.total_declarado} | "
            f"ofertas_primera_pagina={len(resultado.ofertas_primera_pagina)}"
        )
        return resultado

    def capture_batch(
        self,
        page: Any,
        ficha: FichaFuente,
        set_filtros: SetFiltros,
        politicas: PoliticasCaptura,
    ) -> tuple[CaptureBatch, EstadoCaptura]:
        """Captura por listado sin entrar al detalle de cada oferta (v1.2, D11).

        Recorre todas las páginas de la búsqueda (``?start=N``) navegando
        directo al listado SDUi (``/jobs/search-results``, sin el salto por
        ``/jobs/search`` que causaba doble carga) con ``wait_until=commit``.
        La página 1 reutiliza el DOM ya cargado por ``apply_filters``. Fin
        real de la búsqueda: ausencia del botón de paginación ("Siguiente")
        o página sin tarjetas. Redes de seguridad: ``max_paginas`` y
        ``max_ofertas_por_corrida``. Las ofertas se registran con la
        descripción vacía (estado 'descubierta'); el enriquecimiento con la
        descripción es una tarea posterior de Preparación.
        """
        ofertas_capturadas: list[Offer] = []
        paginas_consumidas = 0
        url_resultados = self._construir_url_resultados(ficha.enlace, set_filtros)
        desplazamiento = 0
        enlaces_vistos: set[str] = set()
        while (
            paginas_consumidas < politicas.max_paginas
            and len(ofertas_capturadas) < politicas.max_ofertas_por_corrida
        ):
            if desplazamiento == 0 and "jobs/search-results" in page.url:
                pass
            else:
                url_actual = (
                    url_resultados
                    if desplazamiento == 0
                    else self._construir_pagina_siguiente(
                        url_resultados, desplazamiento
                    )
                )
                try:
                    page.goto(url_actual, wait_until="commit")
                except Exception as exc:
                    raise FlowError(
                        "fuente_inalcanzable", f"Batch navigation failed: {exc}"
                    ) from exc
            timeout_espera = (
                ficha.timeout_segundos
                if paginas_consumidas == 0
                else min(
                    ficha.timeout_segundos,
                    politicas.tope_espera_paginas_sucesivas_segundos,
                )
            )
            self._esperar_resultados(page, timeout_espera)
            html = self._contenido(page)
            self._revisar_estado_captura(html, "tiempo_agotado_captura")
            tarjetas = _tarjetas_resultado(BeautifulSoup(html, "lxml"))
            if not tarjetas:
                break
            restantes = politicas.max_ofertas_por_corrida - len(ofertas_capturadas)
            for enlace, titulo in tarjetas[:restantes]:
                enlace = _url_absoluta(enlace, ficha.enlace)
                if enlace in enlaces_vistos:
                    continue
                enlaces_vistos.add(enlace)
                ofertas_capturadas.append(
                    Offer(
                        enlace=enlace,
                        titulo=titulo,
                        descripcion_original="",
                        fuente_id=ficha.fuente_id,
                        indice_set=set_filtros.indice,
                        id_externo=_extraer_id_externo(enlace),
                    )
                )
            paginas_consumidas += 1
            desplazamiento += len(tarjetas)
            if not self._hay_pagina_siguiente(html):
                break
            if (
                paginas_consumidas < politicas.max_paginas
                and len(ofertas_capturadas) < politicas.max_ofertas_por_corrida
            ):
                self._pausa_entre_lotes(politicas)
        capturas_acumuladas = len(ofertas_capturadas)
        estado = EstadoCaptura(
            estado="ok",
            paginas_consumidas=paginas_consumidas,
            capturadas_acumuladas_fuente=capturas_acumuladas,
            limite_alcanzado=capturas_acumuladas >= politicas.max_ofertas_por_corrida,
        )
        lote = CaptureBatch(
            ofertas=ofertas_capturadas,
            id_corrida="",
            fuente_id=ficha.fuente_id,
            indice_set=set_filtros.indice,
            paginas_consumidas=paginas_consumidas,
        )
        return lote, estado

    def close_session(self, page: Any) -> None:
        """Close the browser page left open after the session."""
        try:
            page.close()
        except Exception:
            pass

    # ------------------------------ internals ---------------------------- #

    def _autenticar(self, page: Any, credenciales: dict[str, str]) -> None:
        try:
            page.goto(_URL_LOGIN)
            self._esperar_form_login(page)
            page.fill(
                "input[autocomplete^='username']:visible",
                credenciales.get("username", ""),
            )
            page.fill(
                "input[autocomplete='current-password']:visible",
                credenciales.get("password", ""),
            )
            page.keyboard.press("Enter")
            try:
                page.wait_for_selector(
                    "input[autocomplete^='username']:visible",
                    state="detached",
                    timeout=15000,
                )
            except Exception:
                try:
                    page.click("button:visible:text-is('Iniciar sesión')", timeout=5000)
                except Exception:
                    pass
                try:
                    page.wait_for_selector(
                        "input[autocomplete^='username']:visible",
                        state="detached",
                        timeout=30000,
                    )
                except Exception:
                    pass
        except Exception as exc:
            raise FlowError(
                "autenticacion_rechazada",
                acotar_evidencia(f"Login failed: {exc}"),
            ) from exc

    def _esperar_form_login(self, page: Any) -> None:
        try:
            page.wait_for_selector(
                "input[autocomplete^='username']:visible", timeout=15000
            )
        except Exception:
            page.wait_for_selector(
                "input[autocomplete*='username']", state="attached", timeout=30000
            )

    def _criterio_ingreso_cumplido(self, page: Any, ficha: FichaFuente) -> bool:
        html = self._contenido(page)
        self._revisar_estado_pagina(html, "tiempo_agotado_ingreso")
        return ficha.criterio_exito in html

    def _esperar_criterio_ingreso(self, page: Any, ficha: FichaFuente) -> None:
        """Wait for the entry criterion, allowing the app shell to hydrate."""
        limite = time.monotonic() + ficha.timeout_segundos
        while time.monotonic() < limite:
            try:
                html = self._contenido(page)
            except Exception as exc:
                if "navigating" not in str(exc):
                    raise
                time.sleep(1)
                continue
            self._revisar_estado_pagina(html, "tiempo_agotado_ingreso")
            if ficha.criterio_exito in html:
                return
            time.sleep(1)
        raise FlowError(
            "criterio_no_cumplido",
            f"Entry criterion '{ficha.criterio_exito}' not verified.",
        )

    def _revisar_estado_pagina(self, html: str, codigo_timeout: str) -> None:
        self._revisar_bloqueo_html(html)
        if not html:
            raise FlowError(codigo_timeout, "Empty page content.")

    def _revisar_estado_captura(self, html: str, codigo_timeout: str) -> None:
        self._revisar_bloqueo_html(html)
        if not html:
            raise FlowError(codigo_timeout, "Empty capture page content.")

    def _revisar_bloqueo_html(self, html: str) -> None:
        """Detect real anti-bot evidence in visible content only.

        The words 'challenge'/'authwall' appear routinely inside JS bundles
        of normal pages (false positives), so script/style content is
        ignored; only concrete visible signals (captcha, identity
        verification, authwall) trigger the block.
        """
        visible = re.sub(
            r"<script.*?</script>|<style.*?</style>",
            " ",
            html,
            flags=re.S | re.I,
        ).lower()
        senales_bloqueo = (
            "show captcha",
            "complete the captcha",
            "verify your identity",
            "verifica tu identidad",
            "verificacion de identidad",
            "introduce el codigo",
            "challenge-login",
            'id="challenge"',
            "no soy un robot",
            "i'm not a robot",
        )
        if any(s in visible for s in senales_bloqueo):
            raise FlowError("bloqueo_plataforma", "Captcha/challenge evidence.")
        if "authwall" in visible:
            raise FlowError("sesion_expirada", "Authwall detected.")

    def _contenido(self, page: Any) -> str:
        return str(page.content())

    def _parsear_resultados(
        self, html: str, ficha: FichaFuente, set_filtros: SetFiltros, enlace: str
    ) -> SearchResult:
        soup = BeautifulSoup(html, "lxml")
        ofertas: list[Offer] = []
        for href, titulo in _tarjetas_resultado(soup):
            enlace_oferta = _url_absoluta(href, ficha.enlace)
            ofertas.append(
                Offer(
                    enlace=enlace_oferta,
                    titulo=titulo,
                    descripcion_original="",
                    fuente_id=ficha.fuente_id,
                    indice_set=set_filtros.indice,
                    id_externo=_extraer_id_externo(enlace_oferta),
                )
            )
        total_el = soup.select_one(_SEL_TOTAL_RESULTADOS)
        total = _parsear_numero(total_el.get_text(strip=True)) if total_el else None
        hay_mas = self._hay_pagina_siguiente(html)
        evidencia = f"url: {enlace}"
        if total is not None:
            evidencia += f" | total: {total}"
        return SearchResult(
            estado="exito",
            ofertas_primera_pagina=ofertas,
            estado_paginacion="hay_mas" if hay_mas else "fin",
            total_declarado=total,
            indice_set=set_filtros.indice,
            numero_de_intentos=1,
            evidencia_acotada=evidencia,
        )

    def _hay_pagina_siguiente(self, html: str) -> bool:
        soup = BeautifulSoup(html, "lxml")
        return any(soup.select(sel) for sel in _SEL_SIGUIENTE)

    def _pausa_entre_lotes(self, politicas: PoliticasCaptura) -> None:
        base = politicas.pausa_entre_lotes_segundos
        estrategia = politicas.estrategia_anti_bloqueo
        if estrategia == "none":
            return
        if estrategia == "pausa_aleatoria":
            delay = base * random.uniform(0.5, 1.5)
        else:
            delay = float(base)
        self._sleep(delay)

    def _construir_url_busqueda(self, base: str, set_filtros: SetFiltros) -> str:
        parametros: dict[str, str] = {}
        for filtro in set_filtros.filtros:
            tipo = str(filtro.get("tipo") or "")
            valor = filtro.get("valor")
            parametro = _PARAMETROS_FILTROS.get(tipo)
            if not parametro:
                raise FlowError(
                    "filtros_no_aplicables",
                    f"Filter type '{tipo}' not supported by this platform.",
                )
            if not valor:
                continue
            if tipo == "fecha_publicacion" and not _RE_FECHA_PUBLICACION.match(
                str(valor)
            ):
                raise FlowError(
                    "filtros_no_aplicables",
                    f"Filter '{tipo}' value '{valor}' is not a "
                    f"valid time window (expected 'r<N>', e.g. 'r86400').",
                )
            if tipo == "modalidad":
                valores: list[str] = valor if isinstance(valor, list) else [str(valor)]
                codigos = [_MODALIDAD_F_WT.get(v.lower(), v) for v in valores]
                parametros[parametro] = ",".join(codigos)
            elif isinstance(valor, list):
                parametros[parametro] = ", ".join(str(v) for v in valor)
            else:
                parametros[parametro] = str(valor)
        if not parametros:
            return base
        separador = "&" if "?" in base else "?"
        return f"{base}{separador}{urlencode(parametros)}"

    def _construir_url_resultados(
        self, base: str, set_filtros: SetFiltros
    ) -> str:
        """URL canonica del listado SDUi (sin el salto por /jobs/search).

        Navegar directo a /jobs/search-results evita la doble carga
        (search -> redirect -> search-results) observada al paginar (D11).
        """
        base_resultados = base.replace(
            "https://www.linkedin.com/jobs/search",
            "https://www.linkedin.com/jobs/search-results/",
        )
        return self._construir_url_busqueda(base_resultados, set_filtros)

    def _construir_pagina_siguiente(self, enlace: str, desplazamiento: int) -> str:
        partes = urlparse(enlace)
        qs = parse_qs(partes.query)
        qs["start"] = [str(desplazamiento)]
        return urlunparse(partes._replace(query=urlencode(qs, doseq=True)))


def _url_absoluta(href: str, base: str) -> str:
    if href.startswith("http"):
        return href
    origen = urlparse(base)
    return f"{origen.scheme}://{origen.netloc}{href}"


def _tarjetas_resultado(soup: BeautifulSoup) -> list[tuple[str, str]]:
    """(href, title) pairs of job cards across the known SSR variants.

    Priority: session SDUi cards (2026, ``componentkey`` divs without links),
    session SSR 2026 cards, classic logged-out cards, then any canonical
    ``/jobs/view/`` link. Variants are exclusive per page and each href is
    returned once. ``/apply/`` links are never cards.
    """
    for selector in (
        _SEL_TARJETA_SDUI,
        _SEL_ENLACE_TARJETA_2026,
        _SEL_ENLACE_TARJETA,
        _SEL_ENLACE_TARJETA_GENERICO,
    ):
        enlaces = soup.select(selector)
        if enlaces:
            break
    tarjetas: list[tuple[str, str]] = []
    vistos: set[str] = set()
    for enlace in enlaces:
        if selector == _SEL_TARJETA_SDUI:
            componente = str(enlace.get("componentkey") or "")
            id_oferta = _RE_ID_COMPONENTE.search(componente)
            if id_oferta is None:
                continue
            href = f"{_URL_JOBS_VIEW}/{id_oferta.group(1)}"
            span_titulo = enlace.select_one("span[aria-hidden='true']")
            titulo = span_titulo.get_text(strip=True) if span_titulo else ""
        else:
            href = str(enlace.get("href") or "")
            if "/jobs/view/" not in href or "/apply/" in href:
                continue
            if selector == _SEL_ENLACE_TARJETA_2026:
                lineas = [
                    linea.strip()
                    for linea in enlace.get_text("\n", strip=True).split("\n")
                    if linea.strip()
                ]
                titulo = lineas[0] if lineas else ""
            elif selector == _SEL_ENLACE_TARJETA:
                titulo = _texto_de(enlace.parent, _SEL_TITULO_TARJETA)
            else:
                titulo = enlace.get_text(strip=True)
        if not titulo or href in vistos:
            continue
        vistos.add(href)
        tarjetas.append((href, titulo))
    return tarjetas


def _texto_de(elemento: Any, selector: str) -> str:
    el = elemento.select_one(selector)
    return el.get_text(strip=True) if el else ""


def _extraer_id_externo(enlace: str) -> str | None:
    match = _RE_ID_EXTERNO.search(enlace)
    return match.group(1) if match else None


def _parsear_numero(texto: str) -> int | None:
    numeros = re.findall(r"\d+", texto.replace(".", "").replace(",", ""))
    return int(numeros[0]) if numeros else None
