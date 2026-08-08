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

from shared.models import (
    CaptureBatch,
    EntryResult,
    EstadoCaptura,
    EventoAlmacen,
    FichaFuente,
    Offer,
    PoliticasCaptura,
    SearchResult,
    SetFiltros,
    TipoEvento,
)

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
_SEL_TITULO_TARJETA = ".base-search-card__title"
_SEL_EMPRESA_TARJETA = ".base-search-card__subtitle"
_SEL_UBICACION_TARJETA = ".base-search-card__location"
_SEL_TOTAL_RESULTADOS = "span.jobs-search-results__total-count"
_SEL_SIGUIENTE = ("button[aria-label='Next']", "a[aria-label='Next']")
_SEL_TITULO_DETALLE = "h1.jobs-unified-top-card__title"
_SEL_DESCRIPCION_DETALLE = "div.jobs-description__content"

_RE_ID_EXTERNO = re.compile(r"/jobs/view/(\d+)")


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
        self.eventos_declarados: list[EventoAlmacen] = []

    # ----------------------------- entrance ----------------------------- #

    def enter_source(
        self,
        page: Any,
        ficha: FichaFuente,
        credenciales: dict[str, str] | None = None,
    ) -> EntryResult:
        """Enter the source and verify the DOC-09 Section 6.1 entry criteria."""
        self.eventos_declarados.clear()
        try:
            page.goto(ficha.url)
        except Exception as exc:
            raise FlowError("fuente_inalcanzable", f"Entry navigation failed: {exc}") from exc
        if ficha.tipo_acceso == "con_autenticacion":
            if not credenciales:
                raise FlowError(
                    "credenciales_no_disponibles",
                    "Authenticated source without credentials.",
                )
            self._autenticar(page, credenciales)
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

    def apply_filters(
        self,
        page: Any,
        ficha: FichaFuente,
        set_filtros: SetFiltros,
        politicas: PoliticasCaptura,
    ) -> SearchResult:
        """Apply the official filter set and parse the first results page."""
        self.eventos_declarados.clear()
        url = self._construir_url_busqueda(ficha.url, set_filtros)
        try:
            page.goto(url)
        except Exception as exc:
            raise FlowError("fuente_inalcanzable", f"Search navigation failed: {exc}") from exc
        html = self._contenido(page)
        self._revisar_estado_pagina(html, "timeout_consulta")
        return self._parsear_resultados(html, ficha, set_filtros)

    def capture_batch(
        self,
        page: Any,
        ficha: FichaFuente,
        set_filtros: SetFiltros,
        politicas: PoliticasCaptura,
    ) -> tuple[CaptureBatch, EstadoCaptura]:
        """Incremental capture of the set (RN-10) applying capture policies."""
        self.eventos_declarados.clear()
        ofertas_capturadas: list[Offer] = []
        paginas_consumidas = 0
        url_actual = self._construir_url_busqueda(ficha.url, set_filtros)
        hay_siguiente = True
        while (
            hay_siguiente
            and paginas_consumidas < politicas.max_paginas
            and len(ofertas_capturadas) < politicas.max_ofertas_por_corrida
        ):
            try:
                page.goto(url_actual)
            except Exception as exc:
                raise FlowError(
                    "fuente_inalcanzable", f"Batch navigation failed: {exc}"
                ) from exc
            html = self._contenido(page)
            self._revisar_estado_captura(html, "timeout_captura")
            referencias = self._extraer_referencias(html, ficha.url)
            if not referencias:
                break
            restantes = politicas.max_ofertas_por_corrida - len(ofertas_capturadas)
            for url_referencia in referencias[:restantes]:
                oferta = self._capturar_oferta(page, url_referencia, ficha, set_filtros)
                if oferta is not None:
                    ofertas_capturadas.append(oferta)
            paginas_consumidas += 1
            hay_siguiente = self._hay_pagina_siguiente(html)
            if hay_siguiente:
                self._pausa_entre_lotes(politicas)
                url_actual = self._construir_pagina_siguiente(
                    url_actual, len(referencias)
                )
        capturas_acumuladas = len(ofertas_capturadas)
        estado = EstadoCaptura(
            estado="ok",
            paginas_consumidas=paginas_consumidas,
            capturadas_acumuladas_fuente=capturas_acumuladas,
            limite_alcanzado=capturas_acumuladas >= politicas.max_ofertas_por_corrida,
        )
        lote = CaptureBatch(
            ofertas=ofertas_capturadas,
            run_id="",
            source_id=ficha.source_id,
            set_indice=set_filtros.indice,
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
            page.wait_for_selector("input[name='session_key']")
            page.fill("input[name='session_key']", credenciales.get("username", ""))
            page.fill("input[name='session_password']", credenciales.get("password", ""))
            page.click("button[type='submit']")
        except Exception as exc:
            raise FlowError("autenticacion_rechazada", f"Login failed: {exc}") from exc

    def _criterio_ingreso_cumplido(self, page: Any, ficha: FichaFuente) -> bool:
        html = self._contenido(page)
        self._revisar_estado_pagina(html, "timeout_ingreso")
        return ficha.criterio_exito in html

    def _revisar_estado_pagina(self, html: str, codigo_timeout: str) -> None:
        self._revisar_bloqueo_html(html)
        if not html:
            raise FlowError(codigo_timeout, "Empty page content.")

    def _revisar_estado_captura(self, html: str, codigo_timeout: str) -> None:
        self._revisar_bloqueo_html(html)
        if not html:
            raise FlowError(codigo_timeout, "Empty capture page content.")

    def _revisar_bloqueo_html(self, html: str) -> None:
        html_bajo = html.lower()
        if "challenge" in html_bajo or "show captcha" in html_bajo:
            raise FlowError("bloqueo_plataforma", "Captcha/challenge evidence.")
        if "authwall" in html_bajo:
            raise FlowError("sesion_expirada", "Authwall detected.")

    def _contenido(self, page: Any) -> str:
        return str(page.content())

    def _parsear_resultados(
        self, html: str, ficha: FichaFuente, set_filtros: SetFiltros
    ) -> SearchResult:
        soup = BeautifulSoup(html, "lxml")
        ofertas: list[Offer] = []
        for enlace in soup.select(_SEL_ENLACE_TARJETA):
            href = str(enlace.get("href") or "")
            if "/jobs/view/" not in href:
                continue
            url = _url_absoluta(href, ficha.url)
            tarjeta = enlace.parent
            titulo = _texto_de(tarjeta, _SEL_TITULO_TARJETA)
            ofertas.append(
                Offer(
                    url=url,
                    titulo=titulo,
                    descripcion_original="",
                    fuente_id=ficha.source_id,
                    set_indice=set_filtros.indice,
                    id_externo_url=_extraer_id_externo(url),
                )
            )
        total_el = soup.select_one(_SEL_TOTAL_RESULTADOS)
        total = _parsear_numero(total_el.get_text(strip=True)) if total_el else None
        hay_mas = self._hay_pagina_siguiente(html)
        return SearchResult(
            estado="ok",
            ofertas_primera_pagina=ofertas,
            estado_paginacion="hay_mas" if hay_mas else "fin",
            total_declarado=total,
            set_indice=set_filtros.indice,
            numero_de_intentos=1,
        )

    def _extraer_referencias(self, html: str, base: str) -> list[str]:
        soup = BeautifulSoup(html, "lxml")
        urls: list[str] = []
        for enlace in soup.select(_SEL_ENLACE_TARJETA):
            href = str(enlace.get("href") or "")
            if "/jobs/view/" in href:
                urls.append(_url_absoluta(href, base))
        return urls

    def _hay_pagina_siguiente(self, html: str) -> bool:
        soup = BeautifulSoup(html, "lxml")
        return any(soup.select(sel) for sel in _SEL_SIGUIENTE)

    def _capturar_oferta(
        self,
        page: Any,
        url_referencia: str,
        ficha: FichaFuente,
        set_filtros: SetFiltros,
    ) -> Offer | None:
        try:
            page.goto(url_referencia)
        except Exception as exc:
            raise FlowError("error_interno_captura", f"Detail navigation failed: {exc}") from exc
        html = self._contenido(page)
        self._revisar_estado_captura(html, "timeout_captura")
        soup = BeautifulSoup(html, "lxml")
        titulo_el = soup.select_one(_SEL_TITULO_DETALLE)
        if titulo_el is None:
            self._declarar_evento("EVT-01", "Detalle sin titulo (excluida del lote).")
            return None
        descripcion_el = soup.select_one(_SEL_DESCRIPCION_DETALLE)
        return Offer(
            url=url_referencia,
            titulo=titulo_el.get_text(strip=True),
            descripcion_original=(
                descripcion_el.get_text(separator=" ", strip=True)
                if descripcion_el
                else ""
            ),
            fuente_id=ficha.source_id,
            set_indice=set_filtros.indice,
            id_externo_url=_extraer_id_externo(url_referencia),
        )

    def _declarar_evento(self, codigo: str, evidencia: str) -> None:
        self.eventos_declarados.append(
            EventoAlmacen(
                run_id="",
                source_id="",
                tipo=TipoEvento.SUCESO,
                codigo=codigo,
                evidencia=evidencia,
            )
        )

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
            if not parametro or not valor:
                continue
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

    def _construir_pagina_siguiente(self, url: str, desplazamiento: int) -> str:
        partes = urlparse(url)
        qs = parse_qs(partes.query)
        qs["start"] = [str(desplazamiento)]
        return urlunparse(partes._replace(query=urlencode(qs, doseq=True)))


def _url_absoluta(href: str, base: str) -> str:
    if href.startswith("http"):
        return href
    origen = urlparse(base)
    return f"{origen.scheme}://{origen.netloc}{href}"


def _texto_de(elemento: Any, selector: str) -> str:
    el = elemento.select_one(selector)
    return el.get_text(strip=True) if el else ""


def _extraer_id_externo(url: str) -> str | None:
    match = _RE_ID_EXTERNO.search(url)
    return match.group(1) if match else None


def _parsear_numero(texto: str) -> int | None:
    numeros = re.findall(r"\d+", texto.replace(".", "").replace(",", ""))
    return int(numeros[0]) if numeros else None
