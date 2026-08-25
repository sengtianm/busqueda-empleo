"""Parser puro de tarjetas de resultados (D42): HTML -> datos.

Extraido de `linkedin.py` para separar la interpretacion del DOM de la
navegacion/sesion; sin Playwright ni estado. Identificadores en espanol
(excepcion D37/D38 aplicada al paquete discovery)."""

import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from shared.utilidades import normalizar_texto

_SEL_ENLACE_TARJETA = "a.base-search-card__link"
_SEL_ENLACE_TARJETA_2026 = "div.job-card-container a.job-card-container__link"
_SEL_ENLACE_TARJETA_GENERICO = "a[href*='/jobs/view/']"
_SEL_TARJETA_SDUI = "div[componentkey^='job-card-component-ref-']"
_SEL_TITULO_TARJETA = ".base-search-card__title"
_SEL_UBICACION_TARJETA_CLASICA = (
    ".job-search-card__location, .base-search-card__location"
)
_RE_ID_EXTERNO = re.compile(r"/jobs/view/(\d+)")
_RE_ID_COMPONENTE = re.compile(r"job-card-component-ref-(\d+)")
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
_URL_JOBS_VIEW = "https://www.linkedin.com/jobs/view"
@dataclass
class _TarjetaExtraida:
    """Datos de una tarjeta de resultado: enlace, titulo, fecha relativa,
    empresa cruda (D41), ubicacion cruda y modalidad canonica ('N/R' cuando
    la tarjeta no las reporta)."""

    enlace: str
    titulo: str
    fecha_relativa: str = ""
    empresa: str = ""
    ubicacion: str = ""
    modalidad: str = "N/R"
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
    empresa, ubicacion, modalidad = _texto_tarjeta_sdui(div, titulo)
    return _TarjetaExtraida(
        enlace=href,
        titulo=titulo,
        fecha_relativa=fecha_relativa,
        empresa=empresa,
        ubicacion=ubicacion,
        modalidad=modalidad,
    )
def _texto_tarjeta_sdui(div: Any, titulo: str) -> tuple[str, str, str]:
    """Empresa cruda + ubicacion cruda + modalidad canonica (D41).

    Misma clasificacion por texto de la etapa anterior (Exp 9), pero
    conservando tambien el PRIMER candidato utilizable como empresa cruda:
    descartados titulo, ruido fijo de la UI y fecha, el primer segmento es
    la empresa y el siguiente la ubicacion (con posible sufijo de
    modalidad). Con un solo candidato hay empresa pero no ubicacion; sin
    candidatos no hay nada.

    Titulos con '|' embebido (COR-0003, oferta 4455899476): el primer
    segmento del bloque de titulo queda truncado en la barra del propio
    titulo, asi que ademas del prefijo sobre el titulo completo se acepta
    la coincidencia exacta contra cualquier segmento del titulo cuando el
    <p> es multiparte (bloque repetido); un candidato de una sola parte
    nunca se descarta por esta via.
    """
    claves_titulo = {
        normalizar_texto(parte) for parte in titulo.split("|")
    } - {""}
    completo_titulo = normalizar_texto(titulo)
    candidatos: list[str] = []
    for p in div.find_all("p"):
        partes = str(p.get_text("|", strip=True)).split("|")
        segmento = partes[0].strip()
        clave = normalizar_texto(segmento)
        if not clave or clave in _RUIDO_TARJETA_SDUI:
            continue
        if _RE_PUBLICADO_SDUI.search(segmento) or clave.startswith("hace "):
            continue
        if titulo and (
            clave.startswith(completo_titulo)
            or (len(partes) > 1 and clave in claves_titulo)
        ):
            continue
        candidatos.append(segmento)
    if not candidatos:
        return "", "", "N/R"
    if len(candidatos) == 1:
        return candidatos[0], "", "N/R"
    ubicacion, modalidad = _modalidad_de_texto(candidatos[1])
    return candidatos[0], ubicacion, modalidad
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



def _texto_de(elemento: Any, selector: str) -> str:
    el = elemento.select_one(selector)
    return el.get_text(strip=True) if el else ""



def _extraer_id_externo(enlace: str) -> str | None:
    match = _RE_ID_EXTERNO.search(enlace)
    return match.group(1) if match else None
