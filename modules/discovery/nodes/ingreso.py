from dataclasses import dataclass
from typing import Any, cast

from loguru import logger
from playwright.sync_api import sync_playwright

from modules.discovery.adapters.linkedin import FlowError
from modules.discovery.adapters.registry import AdaptadorPlataforma, obtener_adaptador
from modules.discovery.run_context import RunContext
from shared.config import load
from shared.models import EntryResult, FichaFuente
from shared.persistence import generar_id
from shared.retry import ejecutar_con_reintento
from shared.utilidades import acotar_evidencia


@dataclass
class ResultadoIngreso:
    estado: str  # "ok" | "error"
    contexto: RunContext | None = None
    codigo: str = ""
    descripcion: str = ""
    decision: str = ""  # "si" | "no"


def ejecutar_ingreso(contexto: RunContext) -> ResultadoIngreso:
    """
    Nodo: Entrar a la fuente seleccionada (v1.1).
    Abre el canal de comunicación y verifica el criterio de ingreso.
    """
    ficha = contexto.fuente_corriente
    if ficha is None:
        logger.error(f"ERR-01: fuente_corriente ausente en corrida {contexto.id_corrida}")
        return ResultadoIngreso(
            estado="error", codigo="ERR-01", descripcion="Fuente corriente ausente"
        )

    # Paso 2: Resolver credenciales
    if ficha.tipo_acceso == "con_autenticacion":
        env_vars = load().get("_env", {})
        valores: list[str] = []
        for ref in ficha.credenciales_referencia:
            val = env_vars.get(ref)
            if not val:
                # ERR-02: Credenciales no disponibles
                contexto.entry_result = EntryResult(
                    estado="fallo",
                    codigo_motivo="credenciales_no_disponibles",
                    evidencia_acotada="Credenciales ausentes en .env",
                    numero_de_intentos=0,
                )
                return ResultadoIngreso(estado="ok", contexto=contexto)
            valores.append(val)

    # Paso 3, 4, 5: Abrir canal y acceder con reintentos (config-driven)
    adapter = obtener_adaptador(ficha.fuente_id)

    return _ejecutar_ingreso_loop(contexto, adapter, ficha)

def _resolver_headless() -> bool:
    """Resuelve el modo headless: BROWSER_HEADLESS en .env gana sobre config.yaml."""
    cfg = load()
    env_raw = cfg.get("_env", {})
    env: dict[str, Any] = env_raw if isinstance(env_raw, dict) else {}
    override = env.get("BROWSER_HEADLESS")
    if isinstance(override, str):
        return override.strip().lower() != "false"
    cfg_browser = cfg.get("browser", {})
    if not isinstance(cfg_browser, dict):
        return True
    return cfg_browser.get("headless", True) is not False


def _ejecutar_ingreso_loop(
    contexto: RunContext,
    adapter: AdaptadorPlataforma,
    ficha: FichaFuente,
) -> ResultadoIngreso:
    playwright_instance: Any = None
    browser: Any = None
    page: Any = None
    playwright_activo = False

    def _cerrar_canal() -> None:
        """Cierra page/browser del intento; el canal vuelve a abrirse al
        reintentar. No detiene la instancia Playwright (se reutiliza)."""
        nonlocal page, browser
        if page:
            page.close()
        if browser:
            browser.close()
        page = None
        browser = None

    def _cerrar_playwright_local() -> None:
        """Detiene la instancia Playwright solo si esta invocación la arrancó."""
        nonlocal playwright_instance, playwright_activo
        if playwright_activo:
            if playwright_instance:
                playwright_instance.stop()
            playwright_activo = False

    def _intento() -> EntryResult:
        nonlocal playwright_instance, browser, page, playwright_activo
        # No usar sync_playwright() con 'with': cierra el navegador al salir
        # del bloque. Se inicia manualmente para mantener la página abierta.
        if playwright_instance is None:
            playwright_instance = sync_playwright().start()
            playwright_activo = True

        headless = _resolver_headless()
        browser = playwright_instance.chromium.launch(headless=headless)
        page = browser.new_page()

        # Cast context.fuente_corriente to FichaFuente since we verified it's not
        # None in ejecutar_ingreso
        ficha_actual = contexto.fuente_corriente
        if ficha_actual is None:
            raise RuntimeError("Fuente corriente must be present")

        page.set_default_timeout(ficha_actual.timeout_segundos * 1000)

        # Llamada al adaptador que encapsula navegación + auth + criterio
        # enter_source ya hace page.goto y _autenticar
        return adapter.enter_source(
            page,
            ficha_actual,
            None if ficha_actual.tipo_acceso == "publico"
            else _obtener_credenciales(ficha_actual),
        )

    def _fallo_final(fe: BaseException, intentos: int) -> ResultadoIngreso:
        _cerrar_canal()
        _cerrar_playwright_local()
        error = cast(FlowError, fe)
        contexto.entry_result = EntryResult(
            estado="fallo",
            codigo_motivo=error.codigo_motivo,
            evidencia_acotada=acotar_evidencia(error.mensaje),
            numero_de_intentos=intentos,
        )
        contexto.id_sesion = None
        contexto.handle_sesion = None
        contexto.browser = None
        contexto.playwright_instance = None
        return ResultadoIngreso(estado="ok", contexto=contexto)

    def _error_interno(exc: Exception, intentos: int) -> ResultadoIngreso:
        _cerrar_canal()
        _cerrar_playwright_local()
        contexto.browser = None
        contexto.playwright_instance = None
        logger.error(f"ERR-09: Error interno en nodo ingreso: {exc}")
        return ResultadoIngreso(estado="error", codigo="ERR-09", descripcion=str(exc))

    res, _ = ejecutar_con_reintento(
        _intento,
        al_reintento=_cerrar_canal,
        al_fallo_final=_fallo_final,
        al_error_interno=_error_interno,
        contexto_log=contexto.id_corrida,
    )
    if isinstance(res, ResultadoIngreso):
        return res

    # Éxito: se conserva la sesión para los nodos siguientes
    contexto.id_sesion = generar_id("sesiones")
    contexto.handle_sesion = page
    contexto.browser = browser
    contexto.playwright_instance = playwright_instance
    contexto.entry_result = res
    playwright_activo = False
    return ResultadoIngreso(estado="ok", contexto=contexto)



def _obtener_credenciales(ficha: FichaFuente) -> dict[str, str]:
    """Mapea las referencias declaradas en la ficha a las claves canónicas
    que consume el adaptador (`username`, `password`).

    Convención (MVP): ``credenciales_referencia[0]`` → ``username``,
    ``credenciales_referencia[1]`` → ``password``. El resto de refs (si
    existieran) se ignoran para mantener el contrato con el adaptador.
    """
    env_vars = load().get("_env", {})
    valores = [env_vars.get(ref, "") for ref in ficha.credenciales_referencia]
    return {
        "username": valores[0] if len(valores) > 0 else "",
        "password": valores[1] if len(valores) > 1 else "",
    }


def ingreso_exitoso(contexto: RunContext) -> ResultadoIngreso:
    """
    Nodo: ¿El ingreso fue exitoso? (v1.0).
    Valida el resultado del ingreso y decide la bifurcación.
    """
    res = contexto.entry_result
    if res is None:
        logger.error(f"ERR-01: entry_result ausente en corrida {contexto.id_corrida}")
        return ResultadoIngreso(estado="error", codigo="ERR-01", descripcion="entry_result ausente")

    # Validación de consistencia
    attrs = ["estado", "codigo_motivo", "evidencia_acotada", "numero_de_intentos"]
    if not all(hasattr(res, attr) for attr in attrs):
        logger.error(
            f"ERR-02: estructura de entry_result inválida en corrida {contexto.id_corrida}"
        )
        return ResultadoIngreso(
            estado="error", codigo="ERR-02", descripcion="Estructura EntryResult inválida"
        )

    if res.estado == "exito":
        if contexto.id_sesion is None or contexto.handle_sesion is None:
            logger.error(
                f"ERR-02: Éxito de ingreso sin sesión activa en corrida {contexto.id_corrida}"
            )
            return ResultadoIngreso(
                estado="error", codigo="ERR-02", descripcion="Éxito sin sesión activa"
            )

    decision = "si" if res.estado == "exito" else "no"
    return ResultadoIngreso(estado="ok", decision=decision, contexto=contexto)

