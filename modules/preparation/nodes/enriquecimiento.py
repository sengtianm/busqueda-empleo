"""Company-profile enrichment for the Preparation node (decision D39).

Visits each company's public LinkedIn profile as a guest (no login, same
httpx technique as the offer capture) right after the company is registered
in the catalog — sheet step 2 placement, approved over the original
decoupled Finalizar Proceso step 6 (H2 stub removed). Extracts
`sitio_web`/`sector`/`tamano`/`descripcion` plus the approved extra fields
`sede`/`tipo`/`fundacion`/`especialidades`; anything the page does not show
stays `'N/R'` (D31 no-empty rule: the source did not report it).

Blocking strategy measured empirically (experiment 2026-08-25): a 2 s pause
between visits keeps guest access clean (10/10 loaded); LinkedIn answers
rapid bursts with transient 999 responses — one retry after ~40 s cleared a
previously blocked profile. A company still blocked is skipped for the rest
of the run (per-run failure cache) and self-heals on the next run via
autocuración (offers pointing at incomplete companies trigger a new visit).
Enrichment never aborts the run: failures are logged locally only — no
events, no error counters (traceability decision D39-6).
"""

import json
import re
import time

import httpx
from loguru import logger

from modules.preparation.run_context import RunContext
from shared.persistence import actualizar_fila
from shared.utilidades import normalizar_texto

# Guest-page wall heuristic for COMPANY profiles: LinkedIn answers with
# status 999/429 or a tiny stub body. Successful profile pages are large
# (~100-400 KB in the experiment) even though they contain sign-up strings,
# so body size — not marker strings — separates real walls from content
# (the offer-page `_es_authwall` markers would false-positive here).
ESTADOS_MURO_HTTP = {999, 429}
UMBRAL_CUERPO_MINIMO_CARACTERES = 10_000
# Measured cooldown: a blocked profile loaded fine again after ~45 s.
ESPERA_REINTENTO_MURO_SEGUNDOS = 40.0
DESCRIPCION_MAX_CARACTERES = 2_000

_ETIQUETAS_CAMPOS: dict[str, tuple[str, ...]] = {
    "sitio_web": ("sitio web", "website"),
    "sector": ("sector", "industria", "industry"),
    "tamano": ("tamano de la empresa", "company size"),
    "sede": ("sede", "headquarters"),
    "tipo": ("tipo", "type"),
    "fundacion": ("fundacion", "founded"),
    "especialidades": ("especialidades", "specialties"),
}
_TODAS_ETIQUETAS: tuple[str, ...] = tuple(
    etiqueta for pares in _ETIQUETAS_CAMPOS.values() for etiqueta in pares
)


class PerfilNoDisponible(Exception):
    """The profile URL cannot be fetched (network failure or wall)."""


def _limpiar_url_perfil(url_perfil: str) -> str:
    """Canonical profile URL: drops tracking params; '' when unusable."""
    url = (url_perfil or "").strip()
    if not url.startswith("http") or "/company/" not in url:
        return ""
    return url.split("?", 1)[0]


def _es_muro(respuesta: httpx.Response) -> bool:
    """Company-profile wall check: atypical status or tiny stub body."""
    if respuesta.status_code in ESTADOS_MURO_HTTP:
        return True
    return len(respuesta.text) < UMBRAL_CUERPO_MINIMO_CARACTERES


def _descargar_perfil(cliente: httpx.Client, url: str) -> str:
    """Fetch the profile HTML; raises `PerfilNoDisponible` on any failure."""
    try:
        respuesta = cliente.get(url)
    except Exception as exc:
        raise PerfilNoDisponible(f"fallo de red: {exc}") from exc
    if _es_muro(respuesta):
        raise PerfilNoDisponible(
            f"perfil bloqueado (estado={respuesta.status_code} "
            f"caracteres={len(respuesta.text)})"
        )
    return respuesta.text


def _lineas_visibles(html: str) -> list[str]:
    """Visible text lines of the page (tag-stripped, blanks dropped)."""
    crudo = re.sub(r"<[^>]+>", "\n", html)
    return [linea.strip() for linea in crudo.split("\n") if linea.strip()]


def _valor_tras_etiqueta(lineas: list[str], etiquetas: tuple[str, ...]) -> str:
    """First non-label line following a label line (normalized matching)."""
    objetivos = {normalizar_texto(etiqueta) for etiqueta in etiquetas}
    todas = {normalizar_texto(etiqueta) for etiqueta in _TODAS_ETIQUETAS}
    for indice, linea in enumerate(lineas):
        normalizada = normalizar_texto(linea)
        if not any(normalizada.startswith(objetivo) for objetivo in objetivos):
            continue
        for siguiente in lineas[indice + 1:]:
            normalizado = normalizar_texto(siguiente)
            if normalizado not in todas:
                return siguiente
    return ""


def _extraer_descripcion(html: str) -> str:
    """Clean embedded description (JSON first, share-card meta fallback)."""
    texto = ""
    coincidencia = re.search(r'"description":"((?:[^"\\]|\\.)*)"', html)
    if coincidencia:
        try:
            texto = json.loads(f'"{coincidencia.group(1)}"')
        except json.JSONDecodeError:
            texto = ""
    if not texto:
        meta = re.search(
            r'<meta property="og:description" content="([^"]+)"', html
        )
        if meta:
            texto = meta.group(1)
    texto = " ".join(texto.split())[:DESCRIPCION_MAX_CARACTERES]
    return texto or "N/R"


def _extraer_campos(html: str) -> dict[str, str]:
    """Extract the eight enrichment fields; absent ones stay `'N/R'`."""
    lineas = _lineas_visibles(html)
    campos: dict[str, str] = {}
    for campo, etiquetas in _ETIQUETAS_CAMPOS.items():
        valor = _valor_tras_etiqueta(lineas, etiquetas).strip()
        if campo == "sitio_web" and not valor.lower().startswith("http"):
            valor = ""
        campos[campo] = valor[:DESCRIPCION_MAX_CARACTERES] if valor else "N/R"
    campos["descripcion"] = _extraer_descripcion(html)
    return campos


def enriquecer_empresa(
    contexto: RunContext,
    empresa_id: str,
    url_perfil: str,
    cliente: httpx.Client,
) -> None:
    """Complete one company row from its public profile (never aborts).

    Skips companies already enriched or already failed this run, honors the
    optional `profundidad_catalogo_empresa` brake (> 0 = max visits per
    run), applies the configured pause before each visit and retries once
    after a fixed cooldown when LinkedIn blocks the profile.
    """
    if (
        empresa_id in contexto.cache_empresas_enriquecidas
        or empresa_id in contexto.cache_empresas_fallidas
    ):
        return
    url = _limpiar_url_perfil(url_perfil)
    if not url:
        logger.debug(
            f"enriquecimiento omitido | run={contexto.id_corrida} "
            f"| empresa={empresa_id} | perfil_no_disponible"
        )
        contexto.cache_empresas_enriquecidas.add(empresa_id)
        return
    profundidad = int(contexto.config_preparacion.get(
        "profundidad_catalogo_empresa", 0
    ))
    if profundidad > 0 and contexto.visitas_empresas >= profundidad:
        logger.debug(
            f"enriquecimiento omitido | run={contexto.id_corrida} "
            f"| empresa={empresa_id} | freno alcanzado ({profundidad})"
        )
        return
    pausa = float(contexto.config_preparacion.get(
        "pausa_entre_empresas_segundos", 0
    ))
    if pausa > 0:
        time.sleep(pausa)
    contexto.visitas_empresas += 1
    try:
        html = _descargar_perfil(cliente, url)
    except PerfilNoDisponible:
        logger.warning(
            f"perfil bloqueado; esperando {ESPERA_REINTENTO_MURO_SEGUNDOS:g}s "
            f"| run={contexto.id_corrida} | empresa={empresa_id}"
        )
        time.sleep(ESPERA_REINTENTO_MURO_SEGUNDOS)
        try:
            html = _descargar_perfil(cliente, url)
        except PerfilNoDisponible as fallo:
            logger.warning(
                f"enriquecimiento fallido tras reintento; queda pendiente "
                f"para autocuracion | run={contexto.id_corrida} "
                f"| empresa={empresa_id} | {fallo}"
            )
            contexto.cache_empresas_fallidas.add(empresa_id)
            return
    campos = _extraer_campos(html)
    try:
        actualizar_fila("empresas", empresa_id, campos)
    except Exception as exc:
        logger.error(
            f"enriquecimiento no persistido | run={contexto.id_corrida} "
            f"| empresa={empresa_id} | {exc}"
        )
        contexto.cache_empresas_fallidas.add(empresa_id)
        return
    contexto.cache_empresas_enriquecidas.add(empresa_id)
    logger.info(
        f"Empresa enriquecida | run={contexto.id_corrida} "
        f"| empresa={empresa_id} "
        f"| campos={[c for c, v in campos.items() if v != 'N/R']}"
    )
