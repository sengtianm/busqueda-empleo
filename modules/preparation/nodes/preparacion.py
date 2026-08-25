"""Preparación de ofertas node of the Preparation flow (ficha M2 v1.0).

Process node, re-entrant per pass (sheet pasos funcionales 1-9). For every
offer in `descubierta` (FIFO): capture the offer page without login (guest
httpx session with browser headers, no Playwright on the critical path —
D4), populate the `empresas` catalog (dedup by `nombre_normalizado`, no AI)
and the `ubicaciones` catalog (AI classifies the raw location text only —
PRM-006, purpose routing `ai_routing.preparacion`), update the offer and
write the per-offer event with `id_oferta` (RN-09). Duplication is NOT
verified here (next node) and `fecha_ultima_verificacion` is never touched
(RN-11).

Traspaso aprobado (2026-08-25): the raw location (`ubicacion`) and the
modality are captured by Module 1 from the SDUi card and live on the offer
row; this node no longer extracts them from the page HTML — it only
classifies the stored text via PRM-006 and links `ubicacion_id`.

Two lots per pass (H1, RN-01): (a) `descubierta` — full capture steps 1-5;
(b) `preparada` with `ubicacion_id = 'N/A'` — only classify / seek-create /
update, without re-capturing the page (the raw text is already stored in
`ubicacion`). Lot (b) is re-queried AFTER lot (a) so offers whose AI
classification failed in this same pass are retried immediately (RN-02:
every pass re-queries the database; the INICIO iterator is never reused).

AI never blocks the capture (RN-07): on failure or Ollama down the offer is
still prepared with `ubicacion_id = 'N/A'` (pending, ERR-08) and only
successful classifications are cached per distinct raw text — caching
failures would neutralize lot (b).

Interpretation note: the sheet's functional-step table maps the lot
determination failure to ERR-05, but ERR-05 in this node's error table is
`respuesta_invalida` (capture). A database failure while determining lots is
therefore registered as ERR-09 (persistence corruption family) and aborts
the run, consistent with the abort branch of the sheet.
"""

import time
from dataclasses import dataclass
from typing import Any
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup, Tag
from loguru import logger
from pydantic import BaseModel

from modules.preparation.nodes.enriquecimiento import enriquecer_empresa
from modules.preparation.nodes.inicio import _validar_preparacion
from modules.preparation.run_context import RunContext
from shared.ia_service import analyze
from shared.persistence import (
    actualizar_fila,
    escribir_evento_seguro,
    escribir_fila,
    leer_candidatas_descubiertas,
    leer_tabla,
)
from shared.retry import ejecutar_con_reintento
from shared.utilidades import acotar_evidencia, ahora, normalizar_texto

# Technical capture constants (module-level like Module 1 selector constants;
# business parameters — pauses, retries, session lifetime — come from config).
PROMPT_UBICACION = "preparacion/ubicacion"
BASE_LINKEDIN = "https://www.linkedin.com"
TIMEOUT_CAPTURA_SEGUNDOS = 15.0
HEADERS_NAVEGADOR = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "es-CO,es;q=0.9,en;q=0.8",
}
# Authwall multi-signal heuristic (approved in the 5.3 analysis): atypical
# HTTP statuses, login/authwall redirects, or known wall markers in the body.
ESTADOS_AUTHWALL_HTTP = {999, 429}
MARCADORES_AUTHWALL = (
    "authwall",
    "sign up | linkedin",
    "join linkedin",
    "iniciar sesion para continuar",
)


class ClasificacionUbicacion(BaseModel):
    """Validated `{ciudad, region, pais}` JSON returned by PRM-006."""

    ciudad: str = "N/A"
    region: str = "N/A"
    pais: str = "N/A"


class FalloPreparacion(Exception):
    """Failure carrying a sheet flow code (`codigo_motivo`) for the retry
    helper; created by the capture steps and the local nodes' DB reads."""

    def __init__(self, codigo_motivo: str, detalle: str) -> None:
        super().__init__(f"{codigo_motivo}: {detalle}")
        self.codigo_motivo = codigo_motivo
        self.detalle = detalle


@dataclass
class ResultadoPreparacion:
    """Outcome handed to the flow: `completada` or `abortada` (ERR-01/09)."""

    estado: str
    contexto: RunContext | None = None
    codigo: str = ""
    descripcion: str = ""


@dataclass
class DatosCaptura:
    """Raw data extracted from one offer page (paso 1).

    La ubicación y la modalidad ya no se extraen aquí: llegan en la fila de
    la oferta escritas por el Módulo 1 (traspaso aprobado 2026-08-25).
    """

    titulo_h1: str | None
    descripcion: str
    empresa_nombre: str
    empresa_perfil: str


def _construir_cliente() -> httpx.Client:
    """Guest-session factory; tests replace it with a MockTransport client."""
    return httpx.Client(
        headers=HEADERS_NAVEGADOR,
        follow_redirects=True,
        timeout=TIMEOUT_CAPTURA_SEGUNDOS,
    )


def _obtener_sesion(contexto: RunContext, renovar: bool = False) -> httpx.Client:
    """RN-03: reuse the session; renew at `limite_vida_sesion` or on demand."""
    limite = int(contexto.config_preparacion["limite_vida_sesion"])
    cliente = contexto.sesion_http
    if (
        isinstance(cliente, httpx.Client)
        and not renovar
        and contexto.ofertas_en_sesion < limite
    ):
        return cliente
    if isinstance(cliente, httpx.Client):
        try:
            cliente.close()
        except Exception:  # pragma: no cover - close is best-effort
            pass
    cliente = _construir_cliente()
    contexto.sesion_http = cliente
    contexto.ofertas_en_sesion = 0
    return cliente


def _es_authwall(respuesta: httpx.Response) -> bool:
    """Multi-signal wall detection: status, final URL and body markers."""
    if respuesta.status_code in ESTADOS_AUTHWALL_HTTP:
        return True
    url_final = str(respuesta.url).lower()
    if "/authwall" in url_final or "login" in url_final:
        return True
    cuerpo = respuesta.text[:20000].lower()
    return any(marcador in cuerpo for marcador in MARCADORES_AUTHWALL)


def _primer_texto(soup: BeautifulSoup, selectores: list[str]) -> str:
    for selector in selectores:
        nodo = soup.select_one(selector)
        if nodo is not None:
            texto = nodo.get_text(" ", strip=True)
            if texto:
                return texto
    return ""


def _extraer_datos(html: str) -> DatosCaptura:
    """Extract title/description/company (paso 1).

    La ubicación y la modalidad NO se extraen de la página (traspaso
    aprobado 2026-08-25: las escribe el Módulo 1 desde la tarjeta); esta
    extracción degrada con gracia (vacío → `N/R`/`N/A` downstream).
    """
    soup = BeautifulSoup(html, "lxml")
    h1 = soup.select_one("h1")
    titulo_h1 = h1.get_text(" ", strip=True) if isinstance(h1, Tag) else None
    if titulo_h1 == "":
        titulo_h1 = None
    descripcion = _primer_texto(
        soup,
        [
            ".show-more-less-html__markup",
            "div[class*='description__text']",
            "main",
            "section",
        ],
    )
    ancla = soup.select_one(
        "a.topcard__org-name-link, a.jobs-unified-top-card__company-name"
    ) or soup.select_one("a[href^='/company/']")
    empresa_nombre = ""
    empresa_perfil = ""
    if isinstance(ancla, Tag):
        empresa_nombre = ancla.get_text(" ", strip=True)
        href = ancla.get("href")
        if isinstance(href, str) and href:
            empresa_perfil = urljoin(BASE_LINKEDIN, href)
    if not any([titulo_h1, descripcion, empresa_nombre]):
        raise ValueError("html sin contenido interpretable")
    return DatosCaptura(
        titulo_h1=titulo_h1,
        descripcion=descripcion,
        empresa_nombre=empresa_nombre,
        empresa_perfil=empresa_perfil,
    )


def _capturar_pagina(contexto: RunContext, enlace: str) -> DatosCaptura:
    """Paso 1 with the configured retry policy (ERR-02/03/04 retryable).

    On `authwall_detectado` the guest session is renewed before the next
    attempt (ERR-04); exhausted retries raise `FalloPreparacion` and the
    offer stays `descubierta` (RN-04).
    """
    reintentos = contexto.config_preparacion["retries"]
    ultimo_codigo: list[str] = []

    def _intentar() -> DatosCaptura:
        cliente = _obtener_sesion(contexto)
        try:
            respuesta = cliente.get(enlace)
        except httpx.TimeoutException as exc:
            # TimeoutException es subclase de HTTPError: capturar primero.
            raise FalloPreparacion("tiempo_agotado_captura", str(exc)) from exc
        except httpx.HTTPError as exc:
            raise FalloPreparacion("pagina_inalcanzable", str(exc)) from exc
        if _es_authwall(respuesta):
            raise FalloPreparacion(
                "authwall_detectado",
                f"status={respuesta.status_code} url={respuesta.url}",
            )
        if respuesta.status_code >= 400:
            raise FalloPreparacion(
                "pagina_inalcanzable", f"status={respuesta.status_code}"
            )
        contexto.ofertas_en_sesion += 1
        try:
            return _extraer_datos(respuesta.text)
        except ValueError as exc:
            raise FalloPreparacion("respuesta_invalida", str(exc)) from exc
        except Exception as exc:
            raise FalloPreparacion("error_interno_captura", str(exc)) from exc

    def _intentar_registrado() -> DatosCaptura:
        try:
            return _intentar()
        except FalloPreparacion as fallo:
            ultimo_codigo.append(fallo.codigo_motivo)
            raise

    def _al_reintento() -> None:
        if ultimo_codigo and ultimo_codigo[-1] == "authwall_detectado":
            _obtener_sesion(contexto, renovar=True)

    resultado, _intentos = ejecutar_con_reintento(
        _intentar_registrado,
        al_reintento=_al_reintento,
        max_attempts=int(reintentos["max_attempts"]),
        base_wait=float(reintentos["base_wait_seconds"]),
        max_wait=float(reintentos["max_wait_seconds"]),
        multiplier=float(reintentos["multiplier"]),
        contexto_log=contexto.id_corrida,
    )
    return resultado


def _diligenciar_empresa(
    contexto: RunContext, nombre: str, perfil: str
) -> str:
    """Paso 2: cache → normalize → upsert by `nombre_normalizado` (RN-05)."""
    if not nombre or not nombre.strip():
        # ERR-07: página sin empresa; continúa con `N/A` (D31).
        logger.warning(
            f"ERR-07 | run={contexto.id_corrida} | empresa_no_disponible"
        )
        return "N/A"
    clave = normalizar_texto(nombre)
    en_cache = contexto.cache_empresas.get(clave)
    if en_cache:
        return en_cache
    existentes = leer_tabla("empresas", {"nombre_normalizado": clave})
    if existentes:
        empresa_id = str(existentes[0]["id"])
    else:
        empresa_id = escribir_fila(
            "empresas",
            {
                "nombre": nombre.strip(),
                "nombre_normalizado": clave,
                "perfil_linkedin": perfil.strip() if perfil.strip() else "N/A",
            },
        )
    contexto.cache_empresas[clave] = empresa_id
    return empresa_id


_CAMPOS_ENRIQUECIMIENTO: tuple[str, ...] = (
    "sitio_web",
    "sector",
    "tamano",
    "descripcion",
    "sede",
    "tipo",
    "fundacion",
    "especialidades",
)


def _enriquecer_si_aplica(
    contexto: RunContext, empresa_id: str, url_perfil: str
) -> None:
    """D39 step-2 hook: enrich new or still-incomplete companies.

    Autocuración: a company already in the catalog whose profile fields are
    all 'N/R' (e.g. blocked on a previous run) is visited again; complete
    ones and this-run failures/fallbacks are skipped via the run caches.
    Enrichment never aborts the run — unexpected interruptions are logged
    and cached as failures for the next run.
    """
    if (
        empresa_id in contexto.cache_empresas_enriquecidas
        or empresa_id in contexto.cache_empresas_fallidas
    ):
        return
    try:
        filas = leer_tabla("empresas", {"id": empresa_id})
        if not filas:
            return
        fila = filas[0]
        if any(
            str(fila.get(campo, "N/R")) != "N/R"
            for campo in _CAMPOS_ENRIQUECIMIENTO
        ):
            contexto.cache_empresas_enriquecidas.add(empresa_id)
            return
        enriquecer_empresa(
            contexto, empresa_id, url_perfil, _obtener_sesion(contexto)
        )
    except Exception as exc:
        logger.warning(
            f"enriquecimiento interrumpido | run={contexto.id_corrida} "
            f"| empresa={empresa_id} | {exc}"
        )
        contexto.cache_empresas_fallidas.add(empresa_id)


def _normalizar_componente(componente: str) -> str:
    """Normalize one tuple component, preserving the `N/A` sentinel (D31)."""
    if componente == "N/A":
        return "N/A"
    return normalizar_texto(componente) or "N/A"


def _diligenciar_ubicacion(contexto: RunContext, texto_crudo: str) -> str:
    """Paso 3: remote → `N/R`; cache → AI (PRM-006) → tuple → seek/create.

    Only successful classifications enter `cache_ia` (RN-07): failures stay
    uncached so lot (b) of this same pass retries them. Stored tuple
    components are normalized (VAL-04) so SQL equality dedups across casing
    variants; `Remoto` never creates a catalog row (RN-06).
    """
    texto = (texto_crudo or "").strip()
    if not texto or texto in {"N/R", "N/A"}:
        # Sin texto crudo utilizable: no reportada → gestionada terminal
        # (RN-08); nunca se invoca la IA con centinelas.
        return "N/R"
    if normalizar_texto(texto) in {"remoto", "trabajo remoto", "remote"}:
        return "N/R"
    tupla = contexto.cache_ia.get(texto)
    if tupla is None:
        try:
            respuesta = analyze(
                PROMPT_UBICACION,
                {"texto_ubicacion": texto},
                purpose="preparacion",
            )
            clasificacion = ClasificacionUbicacion.model_validate(respuesta)
        except Exception as exc:  # LLMError, ValidationError, JSON inválido
            logger.warning(
                f"ERR-08 | run={contexto.id_corrida} | ubicacion_no_clasificada"
                f" | {exc}"
            )
            return "N/A"  # pendiente: la IA jamás bloquea
        tupla = (clasificacion.ciudad, clasificacion.region, clasificacion.pais)
        if all(componente == "N/A" for componente in tupla):
            # JSON válido pero sin información geográfica: pendiente (ERR-08),
            # sin crear una fila de catálogo inútil ni cachear el vacío.
            logger.warning(
                f"ERR-08 | run={contexto.id_corrida} | ubicacion_no_clasificada"
                " | la IA no determino ningun componente"
            )
            return "N/A"
        contexto.cache_ia[texto] = tupla
    clave_tupla: tuple[str, str, str] = (
        _normalizar_componente(tupla[0]),
        _normalizar_componente(tupla[1]),
        _normalizar_componente(tupla[2]),
    )
    en_cache = contexto.cache_ubicaciones.get(clave_tupla)
    if en_cache:
        return en_cache
    existentes = leer_tabla(
        "ubicaciones",
        {"ciudad": clave_tupla[0], "region": clave_tupla[1], "pais": clave_tupla[2]},
    )
    if existentes:
        ubicacion_id = str(existentes[0]["id"])
    else:
        ubicacion_id = escribir_fila(
            "ubicaciones",
            {
                "ciudad": clave_tupla[0],
                "region": clave_tupla[1],
                "pais": clave_tupla[2],
            },
        )
    contexto.cache_ubicaciones[clave_tupla] = ubicacion_id
    return ubicacion_id


def _actualizar_oferta(
    oferta: dict[str, Any], datos: DatosCaptura, empresa_id: str, ubicacion_id: str
) -> None:
    """Pasos 4: faithful update; never `fecha_ultima_verificacion` (RN-11).

    `ubicacion` y `modalidad` NO se tocan: son propiedad del Módulo 1
    desde el traspaso aprobado (2026-08-25).
    """
    campos: dict[str, Any] = {
        "empresa_id": empresa_id,
        "ubicacion_id": ubicacion_id,
        "estado": "preparada",
    }
    if datos.titulo_h1:
        campos["titulo"] = datos.titulo_h1  # RN-10: solo si existe el <h1>
    if datos.descripcion:
        campos["descripcion_original"] = datos.descripcion
    else:
        # Punto 1 aprobado (análisis 5.3): sin descripción extraíble → `N/R`
        # con evidencia en `observaciones`, preservando el texto previo.
        campos["descripcion_original"] = "N/R"
        marca = "descripcion no extraible en la captura"
        base = str(oferta.get("observaciones", "N/A"))
        if marca not in base:
            campos["observaciones"] = (
                f"{base} | {marca}" if base and base != "N/A" else marca
            )
    for clave, valor in list(campos.items()):
        if valor is None or str(valor).strip() == "":
            campos[clave] = "N/A"  # VAL-04/D31: sin vacíos
    actualizar_fila("ofertas_descubiertas", str(oferta["id"]), campos)


def _registrar_evento(
    id_corrida: str, tipo: str, codigo: str, evidencia: str, id_oferta: str
) -> None:
    """RN-09/VAL-05: every offer event carries `id_oferta`; evidence bounded."""
    escribir_evento_seguro(
        {
            "id_corrida": id_corrida,
            "fuente_id": "N/A",
            "tipo": tipo,
            "codigo": codigo,
            "evidencia": acotar_evidencia(evidencia),
            "id_oferta": id_oferta,
            "marca_temporal": ahora(),
        },
        contexto_log=id_corrida,
    )


def _procesar_lote_a(contexto: RunContext, lote: list[dict[str, Any]]) -> bool:
    """Lots (a) steps 1-5 per offer; returns False on ERR-09 (abort)."""
    pausa = float(contexto.config_preparacion["pausa_entre_ofertas_segundos"])
    total = len(lote)
    for indice, oferta in enumerate(lote):
        id_oferta = str(oferta["id"])
        try:
            datos = _capturar_pagina(contexto, str(oferta["enlace"]))
        except FalloPreparacion as fallo:
            contexto.contador_errores += 1
            _registrar_evento(
                contexto.id_corrida,
                "error",
                "preparacion_fallida",
                f"{fallo.codigo_motivo}: {fallo.detalle}",
                id_oferta,
            )
            continue  # RN-04: queda `descubierta` para la siguiente pasada
        try:
            empresa_id = _diligenciar_empresa(
                contexto, datos.empresa_nombre, datos.empresa_perfil
            )
            _enriquecer_si_aplica(
                contexto, empresa_id, datos.empresa_perfil
            )
            ubicacion_id = _diligenciar_ubicacion(
                contexto, str(oferta.get("ubicacion", "") or "")
            )
            _actualizar_oferta(oferta, datos, empresa_id, ubicacion_id)
            contexto.contador_preparadas += 1
            _registrar_evento(
                contexto.id_corrida,
                "suceso",
                "oferta_preparada",
                f"empresa={empresa_id} ubicacion={ubicacion_id} "
                f"modalidad={str(oferta.get('modalidad', 'N/R') or 'N/R')}",
                id_oferta,
            )
        except Exception as error:
            _registrar_evento(
                contexto.id_corrida,
                "error",
                "ERR-09",
                f"corrupcion al persistir la oferta: {error}",
                id_oferta,
            )
            return False
        if indice < total - 1 and pausa > 0:
            time.sleep(pausa)  # VAL-03: pausa entre ofertas, no tras la última
    return True


def _procesar_lote_b(contexto: RunContext, lote: list[dict[str, Any]]) -> bool:
    """Lot (b) steps 3-5 without capture; returns False on ERR-09 (abort)."""
    for oferta in lote:
        id_oferta = str(oferta["id"])
        texto_crudo = str(oferta.get("ubicacion", "") or "")
        try:
            ubicacion_id = _diligenciar_ubicacion(contexto, texto_crudo)
            if ubicacion_id == "N/A":
                continue  # la IA sigue caída: pendiente para la próxima pasada
            actualizar_fila(
                "ofertas_descubiertas", id_oferta, {"ubicacion_id": ubicacion_id}
            )
            _registrar_evento(
                contexto.id_corrida,
                "suceso",
                "oferta_preparada",
                f"ubicacion resuelta en lote (b): {ubicacion_id}",
                id_oferta,
            )
        except Exception as error:
            _registrar_evento(
                contexto.id_corrida,
                "error",
                "ERR-09",
                f"corrupcion al persistir la oferta: {error}",
                id_oferta,
            )
            return False
    return True


def ejecutar_preparacion(contexto: RunContext | None) -> ResultadoPreparacion:
    """Run the Preparación de ofertas node (sheet pasos funcionales 1-9)."""
    if contexto is None or not isinstance(contexto, RunContext):
        logger.error(
            "ERR-01 | sin id_corrida | contexto ausente o corrupto: "
            "no se puede ejecutar la preparación"
        )
        return ResultadoPreparacion(
            estado="abortada",
            codigo="ERR-01",
            descripcion="contexto ausente o corrupto",
        )
    id_corrida = contexto.id_corrida

    # Paso 1 — VAL-01: insumos presentes (configuración validada por INICIO).
    problema = _validar_preparacion(contexto.config_preparacion)
    if problema is not None:
        _registrar_evento(
            id_corrida, "error", "ERR-01", f"insumos invalidos: {problema}", "N/A"
        )
        return ResultadoPreparacion(
            estado="abortada",
            contexto=contexto,
            codigo="ERR-01",
            descripcion=f"insumos ausentes o corruptos: {problema}",
        )

    # Paso 2 (lote a) — re-consulta FIFO (RN-02).
    try:
        lote_a = leer_candidatas_descubiertas()
    except Exception as error:
        _registrar_evento(
            id_corrida, "error", "ERR-09", f"fallo al determinar lotes: {error}",
            "N/A",
        )
        return ResultadoPreparacion(
            estado="abortada",
            contexto=contexto,
            codigo="ERR-09",
            descripcion="database failure determining lots",
        )

    # Pasos 3-7 — lote (a): captura completa.
    if not _procesar_lote_a(contexto, lote_a):
        return ResultadoPreparacion(
            estado="abortada",
            contexto=contexto,
            codigo="ERR-09",
            descripcion="persistence corruption processing lot (a)",
        )

    # Paso 8 — lote (b): re-consultado DESPUÉS del (a) (H1: las ofertas
    # recién preparadas con IA caída se gestionan en la misma pasada).
    try:
        lote_b = leer_tabla(
            "ofertas_descubiertas", {"estado": "preparada", "ubicacion_id": "N/A"}
        )
    except Exception as error:
        _registrar_evento(
            id_corrida, "error", "ERR-09", f"fallo al consultar el lote b: {error}",
            "N/A",
        )
        return ResultadoPreparacion(
            estado="abortada",
            contexto=contexto,
            codigo="ERR-09",
            descripcion="database failure reading pending-location lot",
        )
    if not _procesar_lote_b(contexto, lote_b):
        return ResultadoPreparacion(
            estado="abortada",
            contexto=contexto,
            codigo="ERR-09",
            descripcion="persistence corruption processing lot (b)",
        )

    # Paso 9 — entregar control a "Verificación de duplicidad".
    return ResultadoPreparacion(estado="completada", contexto=contexto)
