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
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from bs4 import BeautifulSoup, Comment
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
from shared.utilidades import acotar_evidencia, normalizar_texto

_PARAMETROS_FILTROS: dict[str, str] = {
    "keywords": "keywords",
    "ubicacion": "location",
    "fecha_publicacion": "f_TPR",
    "nivel_experiencia": "f_JT",
}

# D27 (2026-08-17): la UI nueva (SDUi) descarta f_WT de la URL; el remoto se
# codifica como f_SAL=<id interno de taxonomia>. Solo "remoto" es
# representable hoy; presencial/hibrido -> filtros_no_aplicables.
_MODALIDAD_F_SAL: dict[str, str] = {
    "remoto": "f_SA_id_225001:272001",
}

# D27: buckets canonicos de la UI nueva (menu de fecha). Unicos valores
# representables: cualquier otro r<N> -> filtros_no_aplicables (LinkedIn lo
# descarta silenciosamente y degradaria el alcance temporal del set).
_BUCKETS_FECHA_UI: dict[str, str] = {
    "r86400": "Últimas 24 horas",
    "r604800": "Última semana",
    "r2592000": "Último mes",
}
_SEL_CHIP_REMOTO = "div[role='radio'][aria-label='Filtrar por En remoto']"
_SEL_PILL_FECHA = (
    "div[role='button'][aria-expanded='false']"
    "[componentkey^='SearchResults_filter_pill_"
    "JobSearchFacetSuggestionType_TIME_POSTED']"
)
_SEL_RADIO_FECHA = "div[role='radio'][aria-label='{}']"
_SEL_MOSTRAR_RESULTADOS = (
    "button:text-is('Mostrar resultados'), a:text-is('Mostrar resultados')"
)

_RE_TOTAL_DECLARADO = re.compile(r"^(\d+) resultados$")

_SEL_ENLACE_TARJETA = "a.base-search-card__link"
_SEL_ENLACE_TARJETA_2026 = "div.job-card-container a.job-card-container__link"
_SEL_ENLACE_TARJETA_GENERICO = "a[href*='/jobs/view/']"
_SEL_TARJETA_SDUI = "div[componentkey^='job-card-component-ref-']"
_SEL_TITULO_TARJETA = ".base-search-card__title"
_SEL_UBICACION_TARJETA_CLASICA = (
    ".job-search-card__location, .base-search-card__location"
)
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

# D28/D29 (2026-08-17): las clases CSS reales de la tarjeta SDUi estan
# hasheadas por pagina (obfuscacion); el parseo usa el texto de los <p> de la
# tarjeta, validado empiricamente (Exp 9: 75/75 tarjetas, 3 paginas reales).
# (D29) De la tarjeta solo se conservaba la fecha relativa de publicacion.
# Traspaso aprobado (2026-08-25): la tarjeta vuelve a proveer la ubicacion
# cruda y la modalidad — M1 las escribe en `ofertas_descubiertas` y el M2
# deja de extraerlas del HTML de la pagina invitado. La clasificacion por
# <p> sigue la evidencia Exp 9: tras titulo y empresa, el siguiente <p>
# utilizable es la ubicacion; puede llevar sufijo de modalidad "(En remoto)/
# (Hibrido)/(Presencial)". Sin senal -> 'N/R' (fuente no lo reporta).
_RE_PUBLICADO_SDUI = re.compile(
    r"Publicado hace\s+(\d+)\s+(minutos?|horas?|d[ií]as?|semanas?|mes(?:es)?)",
    re.IGNORECASE,
)

_RUIDO_TARJETA_SDUI: frozenset[str] = frozenset(
    {
        "visto",
        "adelantate a solicitar el empleo",
        "solicitar",
        "evaluando solicitudes de forma activa",
    }
)

_MODALIDAD_TARJETA: dict[str, str] = {
    "remoto": "remoto",
    "en remoto": "remoto",
    "remote": "remoto",
    "trabajo remoto": "remoto",
    "hibrido": "hibrido",
    "hybrid": "hibrido",
    "presencial": "presencial",
    "onsite": "presencial",
    "on site": "presencial",
    "en sitio": "presencial",
}

_RE_SUFIJO_MODALIDAD = re.compile(r"\(([^)]+)\)\s*$")

_URL_LOGIN = "https://www.linkedin.com/login/es/?fromSignIn=true"
_URL_JOBS_VIEW = "https://www.linkedin.com/jobs/view"

_RE_FECHA_PUBLICACION = re.compile(r"^r\d+$")


@dataclass
class _TarjetaExtraida:
    """Datos de una tarjeta de resultado: enlace, titulo, fecha relativa,
    ubicacion cruda y modalidad canonica ('N/R' cuando la tarjeta no la
    reporta)."""

    enlace: str
    titulo: str
    fecha_relativa: str = ""
    ubicacion: str = ""
    modalidad: str = "N/R"


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
        """Navigate straight to the SDUi results list and parse the first page.

        (D26, 2026-08-14) The entry goes directly to ``/jobs/search-results``
        instead of ``/jobs/search``: the results list is the view that serves
        the real offer set (the canonical page only redirects and shows an
        unreliable total label), and ``wait_until="commit"`` (same as
        pagination, D11) avoids the transient ``fuente_inalcanzable`` right
        after login. Validation (cards render, anti-bot checks) runs on the
        real list.

        (D27, 2026-08-17) The new UI drops ``f_WT``/``location`` from the URL
        and honors only canonical date buckets; the remote filter must be
        requested as ``f_SAL=<internal taxonomy id>``. Since params can stop
        being honored silently, the applied filter state is verified in the
        DOM (chips) after loading; if the expected chips are not active, a
        best-effort UI click fallback is attempted and verified again. If the
        filters still are not applied, the set fails with
        ``filtros_no_aplicables`` instead of capturing non-conforming offers.
        """
        enlace = self._construir_url_resultados(ficha.enlace, set_filtros)
        try:
            page.goto(enlace, wait_until="commit")
        except Exception as exc:
            raise FlowError("fuente_inalcanzable", f"Search navigation failed: {exc}") from exc
        self._esperar_resultados(page, ficha.timeout_segundos)
        html = self._contenido(page)
        self._revisar_estado(html, "tiempo_agotado_consulta")
        esperados = self._filtros_esperados(set_filtros)
        if esperados and not self._verificar_filtros_aplicados(html, esperados):
            self._aplicar_filtros_por_ui(page, esperados, html)
            self._esperar_resultados(page, ficha.timeout_segundos)
            html = self._contenido(page)
            self._revisar_estado(html, "tiempo_agotado_consulta")
            if not self._verificar_filtros_aplicados(html, esperados):
                raise FlowError(
                    "filtros_no_aplicables",
                    "LinkedIn no aplico los filtros esperados "
                    f"({', '.join(esperados)}) tras URL ni fallback UI.",
                )
            enlace = page.url
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
        url_resultados = (
            page.url
            if "jobs/search-results" in page.url
            else self._construir_url_resultados(ficha.enlace, set_filtros)
        )
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
            self._revisar_estado(html, "tiempo_agotado_captura")
            tarjetas = _tarjetas_resultado(BeautifulSoup(html, "lxml"), ficha.enlace)
            if not tarjetas:
                break
            restantes = politicas.max_ofertas_por_corrida - len(ofertas_capturadas)
            for tarjeta in tarjetas[:restantes]:
                enlace = _url_absoluta(tarjeta.enlace, ficha.enlace)
                if enlace in enlaces_vistos:
                    continue
                enlaces_vistos.add(enlace)
                ofertas_capturadas.append(
                    Offer(
                        enlace=enlace,
                        titulo=tarjeta.titulo,
                        descripcion_original="",
                        fuente_id=ficha.fuente_id,
                        indice_set=set_filtros.indice,
                        id_externo=_extraer_id_externo(enlace),
                        fecha_publicacion=_fecha_relativa_a_datetime(
                            tarjeta.fecha_relativa
                        ),
                        observaciones=tarjeta.fecha_relativa,
                        ubicacion=tarjeta.ubicacion or "N/R",
                        modalidad=tarjeta.modalidad or "N/R",
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

    # --------------------------- filter verification ---------------------- #

    def _filtros_esperados(self, set_filtros: SetFiltros) -> list[str]:
        """Chips que deben estar activos en el DOM para el set de filtros.

        Solo los filtros verificables en la UI nueva: modalidad (remoto) y
        ventana de fecha (bucket canonico). ``keywords``/``location`` no
        tienen chip verificable (LinkedIn conserva la ubicacion en estado,
        no en la URL).
        """
        esperados: list[str] = []
        for filtro in set_filtros.filtros:
            tipo = str(filtro.get("tipo") or "")
            valor = filtro.get("valor")
            if not valor:
                continue
            if tipo == "modalidad":
                esperados.append("remoto")
            elif tipo == "fecha_publicacion":
                esperados.append(_BUCKETS_FECHA_UI[str(valor)])
        return esperados

    def _verificar_filtros_aplicados(self, html: str, esperados: list[str]) -> bool:
        """True si los chips esperados estan activos en el DOM (D27)."""
        soup = BeautifulSoup(html, "lxml")
        for esperado in esperados:
            if esperado == "remoto":
                if not soup.select(f"{_SEL_CHIP_REMOTO}[aria-checked='true']"):
                    return False
                continue
            if not self._checkbox_fecha_marcado(soup, esperado):
                return False
        return True

    def _checkbox_fecha_marcado(self, soup: BeautifulSoup, etiqueta: str) -> bool:
        """Checkbox de fecha marcado cuyo label[for] coincide exactamente.

        (D27, debug COR-0275) El DOM real usa input + label HERMANOS
        (<input id=...><label for=...>), no anidados; el id es inestable por
        render, por eso se resuelve siempre via label[for].
        """
        for label in soup.find_all("label"):
            if label.get_text(strip=True) != etiqueta:
                continue
            id_input = label.get("for")
            if not id_input:
                continue
            casilla = soup.find(
                "input", {"id": id_input, "type": "checkbox", "checked": True}
            )
            if casilla is not None:
                return True
        return False

    def _aplicar_filtros_por_ui(
        self, page: Any, esperados: list[str], html: str
    ) -> None:
        """Fallback por clics en la UI (D27): mejores esfuerzos, sin excepciones.

        Solo clica los filtros que NO estan activos en el DOM actual (el
        clic sobre un radio activo lo DESACTIVA). El estado final lo decide
        la verificacion posterior; los timeouts se absorben y el flujo
        continua.
        """
        try:
            sopa = BeautifulSoup(html, "lxml")
            for esperado in esperados:
                if esperado == "remoto":
                    if sopa.select(f"{_SEL_CHIP_REMOTO}[aria-checked='true']"):
                        continue
                    page.click(_SEL_CHIP_REMOTO, timeout=5000)
                else:
                    if self._checkbox_fecha_marcado(sopa, esperado):
                        continue
                    page.click(_SEL_PILL_FECHA, timeout=5000)
                    page.click(_SEL_RADIO_FECHA.format(esperado), timeout=5000)
                    page.click(_SEL_MOSTRAR_RESULTADOS, timeout=5000)
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
        self._revisar_estado(html, "tiempo_agotado_ingreso")
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
            self._revisar_estado(html, "tiempo_agotado_ingreso")
            if ficha.criterio_exito in html:
                return
            time.sleep(1)
        raise FlowError(
            "criterio_no_cumplido",
            f"Entry criterion '{ficha.criterio_exito}' not verified.",
        )

    def _revisar_estado(self, html: str, codigo_timeout: str) -> None:
        """Revisión común de página: bloqueo anti-bot o contenido vacío."""
        self._revisar_bloqueo_html(html)
        if not html:
            raise FlowError(codigo_timeout, "Empty page content.")

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
        for tarjeta in _tarjetas_resultado(soup, ficha.enlace):
            ofertas.append(
                Offer(
                    enlace=tarjeta.enlace,
                    titulo=tarjeta.titulo,
                    descripcion_original="",
                    fuente_id=ficha.fuente_id,
                    indice_set=set_filtros.indice,
                    id_externo=_extraer_id_externo(tarjeta.enlace),
                    fecha_publicacion=_fecha_relativa_a_datetime(
                        tarjeta.fecha_relativa
                    ),
                    observaciones=tarjeta.fecha_relativa,
                    ubicacion=tarjeta.ubicacion or "N/R",
                    modalidad=tarjeta.modalidad or "N/R",
                )
            )
        total: int | None = None
        for nodo in _nodos_texto_visibles(soup):
            coincidencia = _RE_TOTAL_DECLARADO.match(nodo.strip())
            if coincidencia:
                total = int(coincidencia.group(1))
                break
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
            if tipo == "modalidad":
                if not valor:
                    continue
                valores: list[str] = valor if isinstance(valor, list) else [str(valor)]
                normales = [v.strip().lower() for v in valores]
                if any(v not in _MODALIDAD_F_SAL for v in normales):
                    raise FlowError(
                        "filtros_no_aplicables",
                        f"Modalidad '{valores}' no representable en la UI "
                        f"actual (solo 'remoto', D27).",
                    )
                parametros["f_SAL"] = _MODALIDAD_F_SAL["remoto"]
                continue
            parametro = _PARAMETROS_FILTROS.get(tipo)
            if not parametro:
                raise FlowError(
                    "filtros_no_aplicables",
                    f"Filter type '{tipo}' not supported by this platform.",
                )
            if not valor:
                continue
            if tipo == "fecha_publicacion":
                if not _RE_FECHA_PUBLICACION.match(str(valor)):
                    raise FlowError(
                        "filtros_no_aplicables",
                        f"Filter '{tipo}' value '{valor}' is not a "
                        f"valid time window (expected 'r<N>', e.g. 'r86400').",
                    )
                if str(valor) not in _BUCKETS_FECHA_UI:
                    raise FlowError(
                        "filtros_no_aplicables",
                        f"Filter '{tipo}' value '{valor}' no es un bucket "
                        f"canonico de la UI (D27): "
                        f"{', '.join(sorted(_BUCKETS_FECHA_UI))}.",
                    )
                parametros[parametro] = str(valor)
                continue
            if isinstance(valor, list):
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
        (D27) La UI nueva elimina location/f_WT de la URL final pero honra
        los parametros al aplicarlos (estado de busqueda conservado); por eso
        siguen enviandose en la URL construida.
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


def _tarjetas_resultado(soup: BeautifulSoup, base: str = "") -> list[_TarjetaExtraida]:
    """Tarjetas de oferta de las variantes SSR conocidas (titulo, fecha
    relativa, ubicacion y modalidad donde la variante las expone).

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
    tarjetas: list[_TarjetaExtraida] = []
    vistos: set[str] = set()
    for enlace in enlaces:
        if selector == _SEL_TARJETA_SDUI:
            tarjeta = _extraer_tarjeta_sdui(enlace)
            if tarjeta is None:
                continue
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
            ubicacion, modalidad = "", "N/R"
            if selector == _SEL_ENLACE_TARJETA:
                texto_ubi = _texto_de(enlace, _SEL_UBICACION_TARJETA_CLASICA)
                if texto_ubi:
                    ubicacion, modalidad = _modalidad_de_texto(texto_ubi)
            tarjeta = _TarjetaExtraida(
                enlace=_url_absoluta(href, base),
                titulo=titulo,
                fecha_relativa="",
                ubicacion=ubicacion,
                modalidad=modalidad,
            )
        if not tarjeta.titulo or tarjeta.enlace in vistos:
            continue
        vistos.add(tarjeta.enlace)
        tarjetas.append(tarjeta)
    return tarjetas


def _extraer_tarjeta_sdui(div: Any) -> _TarjetaExtraida | None:
    """Construye la tarjeta desde el div SDUi (componentkey + texto)."""
    componente = str(div.get("componentkey") or "")
    id_oferta = _RE_ID_COMPONENTE.search(componente)
    if id_oferta is None:
        return None
    href = f"{_URL_JOBS_VIEW}/{id_oferta.group(1)}"
    span_titulo = div.select_one("span[aria-hidden='true']")
    titulo = span_titulo.get_text(strip=True) if span_titulo else ""
    fecha_relativa = _fecha_relativa_sdui(div)
    ubicacion, modalidad = _ubicacion_sdui(div, titulo)
    return _TarjetaExtraida(
        enlace=href,
        titulo=titulo,
        fecha_relativa=fecha_relativa,
        ubicacion=ubicacion,
        modalidad=modalidad,
    )


def _ubicacion_sdui(div: Any, titulo: str) -> tuple[str, str]:
    """Ubicacion cruda + modalidad canonica desde los <p> de la tarjeta SDUi.

    Clasificacion por texto (Exp 9): descartados titulo, empresa (primer
    candidato utilizable), ruido fijo de la UI y la fecha, el siguiente
    segmento es la ubicacion; puede llevar sufijo de modalidad "(En remoto)".
    Sin segundo candidato -> sin ubicacion ('', 'N/R').
    """
    candidatos: list[str] = []
    for p in div.find_all("p"):
        segmento = str(p.get_text("|", strip=True)).split("|")[0].strip()
        clave = normalizar_texto(segmento)
        if not clave or clave in _RUIDO_TARJETA_SDUI:
            continue
        if _RE_PUBLICADO_SDUI.search(segmento) or clave.startswith("hace "):
            continue
        if titulo and clave.startswith(normalizar_texto(titulo)):
            continue
        candidatos.append(segmento)
    if len(candidatos) < 2:
        return "", "N/R"
    return _modalidad_de_texto(candidatos[1])


def _modalidad_de_texto(texto: str) -> tuple[str, str]:
    """Separa un sufijo de modalidad "(…)" del texto de ubicacion.

    Devuelve (texto_sin_sufijo, modalidad_canonica); 'N/R' cuando el texto
    no declara modalidad. Si el texto COMPLETO es una modalidad ("Remoto"),
    no queda ubicacion utilizable.
    """
    clave = normalizar_texto(texto)
    if clave in _MODALIDAD_TARJETA:
        return "", _MODALIDAD_TARJETA[clave]
    sufijo = _RE_SUFIJO_MODALIDAD.search(texto)
    if sufijo:
        canonica = _MODALIDAD_TARJETA.get(normalizar_texto(sufijo.group(1)))
        if canonica:
            return texto[: sufijo.start()].rstrip(), canonica
    return texto, "N/R"


def _fecha_relativa_sdui(card: Any) -> str:
    """Texto "Publicado hace N <unidad>" desde los <p> de la tarjeta SDUi.

    (D28/D29) En la tarjeta SDUi el <p> de la fecha es "Publicado hace 9
    horas|hace 9 horas": se toma el primer segmento (texto visible) y se
    ignora el texto accesible duplicado (Exp 9: 75/75 tarjetas).
    """
    for p in card.find_all("p"):
        texto = p.get_text("|", strip=True)
        if "Publicado hace" in texto:
            return str(texto.split("|")[0].strip())
    return ""


def _fecha_relativa_a_datetime(texto: str) -> datetime | None:
    """Convierte 'Publicado hace N <unidad>' a timestamp absoluto aproximado.

    D28: LinkedIn redondea la antiguedad publicada (error hasta ~1 h); el
    texto crudo se conserva en `observaciones` de la oferta. La unidad mes se
    aproxima a 30 dias (documentado en la ficha).
    """
    if not texto:
        return None
    coincidencia = _RE_PUBLICADO_SDUI.search(texto)
    if coincidencia is None:
        return None
    cantidad = int(coincidencia.group(1))
    if cantidad > 365:
        return None
    unidad = coincidencia.group(2).lower()
    if unidad.startswith("minuto"):
        delta = timedelta(minutes=cantidad)
    elif unidad.startswith("hora"):
        delta = timedelta(hours=cantidad)
    elif unidad.startswith("d"):
        delta = timedelta(days=cantidad)
    elif unidad.startswith("semana"):
        delta = timedelta(weeks=cantidad)
    elif unidad.startswith("mes"):
        delta = timedelta(days=30 * cantidad)
    else:
        return None
    return datetime.now() - delta


def _nodos_texto_visibles(soup: BeautifulSoup) -> list[str]:
    """Nodos de texto fuera de script/style (D28): el total declarado debe
    leerse del DOM visible; los bundles JS contienen numeros que podrian
    falsificarlo."""
    return [
        str(nodo)
        for nodo in soup.find_all(string=True)
        if nodo.parent is not None
        and nodo.parent.name not in ("script", "style")
        and not isinstance(nodo, Comment)
    ]


def _texto_de(elemento: Any, selector: str) -> str:
    el = elemento.select_one(selector)
    return el.get_text(strip=True) if el else ""


def _extraer_id_externo(enlace: str) -> str | None:
    match = _RE_ID_EXTERNO.search(enlace)
    return match.group(1) if match else None
