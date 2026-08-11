import time
from dataclasses import dataclass

from loguru import logger
from playwright.sync_api import sync_playwright

from modules.discovery.adapters.linkedin import FlowError, LinkedInAdapter
from modules.discovery.run_context import RunContext
from shared.config import load
from shared.models import EntryResult, FichaFuente
from shared.persistence import generate_id
from shared.retry import should_retry
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

    # Paso 3, 4, 5: Abrir canal y acceder con reintentos
    cfg_retries = load().get("retries", {})
    max_attempts = cfg_retries.get("max_attempts", 3)
    base_wait = cfg_retries.get("base_wait_seconds", 2)
    multiplier = cfg_retries.get("multiplier", 2)
    max_wait = cfg_retries.get("max_wait_seconds", 30)

    adapter = LinkedInAdapter()

    return _ejecutar_ingreso_loop(
        contexto, adapter, max_attempts, base_wait, multiplier, max_wait
    )

def _ejecutar_ingreso_loop(
    contexto: RunContext,
    adapter: LinkedInAdapter,
    max_attempts: int,
    base_wait: float,
    multiplier: float,
    max_wait: float,
) -> ResultadoIngreso:
    # import time moved to top-level

    playwright_instance = None
    browser = None
    page = None
    playwright_activo = False
    attempt = 0

    try:
        while attempt < max_attempts:
            attempt += 1
            try:
                # We must not use sync_playwright() with 'with' because it closes the browser
                # when exiting the block. We start it manually to keep the page open.
                if playwright_instance is None:
                    playwright_instance = sync_playwright().start()
                    playwright_activo = True

                headless = load().get("browser", {}).get("headless", True)
                browser = playwright_instance.chromium.launch(headless=headless)
                page = browser.new_page()

                # Cast context.fuente_corriente to FichaFuente since we verified it's not
                # None in ejecutar_ingreso
                ficha = contexto.fuente_corriente
                if ficha is None:
                    raise RuntimeError("Fuente corriente must be present")

                page.set_default_timeout(ficha.timeout_segundos * 1000)

                # Llamada al adaptador que encapsula navegación + auth + criterio
                # enter_source ya hace page.goto y _autenticar
                res = adapter.enter_source(
                    page,
                    ficha,
                    None if ficha.tipo_acceso == "publico"
                    else _obtener_credenciales(ficha),
                )

                # Éxito
                contexto.id_sesion = generate_id("sesiones")
                contexto.handle_sesion = page
                contexto.entry_result = res
                playwright_activo = False  # se conserva la sesión para los nodos siguientes
                return ResultadoIngreso(estado="ok", contexto=contexto)

            except FlowError as fe:
                # Cerrar canal antes de reintentar o fallar
                if page:
                    page.close()
                if browser:
                    browser.close()

                if should_retry(fe.codigo_motivo) and attempt < max_attempts:
                    # Backoff
                    wait_time = min(base_wait * (multiplier ** (attempt - 1)), max_wait)
                    time.sleep(wait_time)
                    continue
                else:
                    # Fallo definitivo
                    contexto.entry_result = EntryResult(
                        estado="fallo",
                        codigo_motivo=fe.codigo_motivo,
                        evidencia_acotada=acotar_evidencia(fe.mensaje),
                        numero_de_intentos=attempt,
                    )
                    contexto.id_sesion = None
                    contexto.handle_sesion = None
                    return ResultadoIngreso(estado="ok", contexto=contexto)
            except Exception as e:
                # Error no esperado (corrupción o sistema)
                if page:
                    page.close()
                if browser:
                    browser.close()
                logger.error(f"ERR-09: Error interno en nodo ingreso: {e}")
                return ResultadoIngreso(estado="error", codigo="ERR-09", descripcion=str(e))
    finally:
        # El flag local es la fuente de verdad: si esta invocación arrancó
        # un playwright y no estamos en éxito, lo cerramos. Esto evita leaks
        # cuando llegan valores stale de id_sesion/handle_sesion desde una
        # fuente previa (multi-fuente).
        if playwright_activo:
            if playwright_instance:
                playwright_instance.stop()
            playwright_activo = False

    # Path unreachable with max_attempts > 0; satisfies mypy strict.
    return ResultadoIngreso(estado="error", codigo="ERR-09", descripcion="sin intentos")



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

