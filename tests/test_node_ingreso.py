from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest

from modules.discovery.adapters.linkedin import FlowError
from modules.discovery.nodes.ingreso import ejecutar_ingreso, ingreso_exitoso
from modules.discovery.run_context import RunContext
from shared.models import EntryResult


@pytest.fixture
def mock_context() -> RunContext:
    config_fuentes = [
        {
            "fuente_id": "LI-01",
            "nombre": "LinkedIn",
            "ficha_acceso": {
                "enlace": "https://linkedin.com",
                "tipo_acceso": "publico",
                "criterio_exito": "global-nav",
                "timeout_segundos": 10,
            },
        }
    ]
    return RunContext(config_fuentes=config_fuentes)


@pytest.fixture
def mock_adapter() -> Generator[MagicMock, None, None]:
    with patch("modules.discovery.nodes.ingreso.obtener_adaptador") as mock:
        yield mock.return_value


@pytest.fixture
def mock_playwright() -> Generator[MagicMock, None, None]:
    instance = MagicMock()
    instance.start.return_value = instance
    browser = instance.chromium.launch.return_value
    browser.new_page.return_value = MagicMock()
    with patch("modules.discovery.nodes.ingreso.sync_playwright", return_value=instance):
        yield instance


@pytest.fixture(autouse=True)
def _mock_evento_ingreso() -> Generator[MagicMock, None, None]:
    """D30: aislar la escritura de eventos (la rama de éxito la emite)."""
    with patch("modules.discovery.nodes.ingreso.escribir_evento_seguro") as mock:
        yield mock


def _entry_result(ctx: RunContext) -> EntryResult:
    res = ctx.entry_result
    assert res is not None
    return res


def test_ejecutar_ingreso_publico_exito(
    mock_context: RunContext,
    mock_adapter: MagicMock,
    mock_playwright: MagicMock,
) -> None:
    mock_context.fuente_corriente = mock_context.fuentes_filtradas[0]
    mock_adapter.enter_source.return_value = EntryResult(
        estado="exito", evidencia_acotada="ok", numero_de_intentos=1
    )

    res = ejecutar_ingreso(mock_context)

    assert res.estado == "ok"
    assert _entry_result(mock_context).estado == "exito"
    assert mock_context.id_sesion is not None
    assert mock_context.handle_sesion is not None
    assert mock_context.browser is mock_playwright.chromium.launch.return_value
    assert mock_context.playwright_instance is mock_playwright


def test_ejecutar_ingreso_autenticado_exito(
    mock_context: RunContext,
    mock_adapter: MagicMock,
    mock_playwright: MagicMock,
) -> None:
    ficha = mock_context.fuentes_filtradas[0]
    ficha.tipo_acceso = "con_autenticacion"
    ficha.credenciales_referencia = ["USER", "PASS"]
    mock_context.fuente_corriente = ficha

    with patch("modules.discovery.nodes.ingreso.load") as mock_load:
        mock_load.return_value = {"_env": {"USER": "test@test.com", "PASS": "1234"}}
        mock_adapter.enter_source.return_value = EntryResult(
            estado="exito", evidencia_acotada="ok", numero_de_intentos=1
        )

        res = ejecutar_ingreso(mock_context)
        assert res.estado == "ok"
        assert _entry_result(mock_context).estado == "exito"


def test_ejecutar_ingreso_sin_credenciales(
    mock_context: RunContext, mock_playwright: MagicMock
) -> None:
    ficha = mock_context.fuentes_filtradas[0]
    ficha.tipo_acceso = "con_autenticacion"
    ficha.credenciales_referencia = ["USER"]
    mock_context.fuente_corriente = ficha

    with patch("modules.discovery.nodes.ingreso.load") as mock_load:
        mock_load.return_value = {"_env": {}}
        res = ejecutar_ingreso(mock_context)

        assert res.estado == "ok"
        assert _entry_result(mock_context).estado == "fallo"
        assert _entry_result(mock_context).codigo_motivo == "credenciales_no_disponibles"


def test_ejecutar_ingreso_reintento_exito(
    mock_context: RunContext,
    mock_adapter: MagicMock,
    mock_playwright: MagicMock,
) -> None:
    mock_context.fuente_corriente = mock_context.fuentes_filtradas[0]
    mock_adapter.enter_source.side_effect = [
        FlowError("fuente_inalcanzable", "Down"),
        EntryResult(estado="exito", evidencia_acotada="ok", numero_de_intentos=2),
    ]

    with patch("time.sleep"):
        res = ejecutar_ingreso(mock_context)

    assert res.estado == "ok"
    assert _entry_result(mock_context).estado == "exito"
    assert mock_adapter.enter_source.call_count == 2


def test_ejecutar_ingreso_reintentos_agotados(
    mock_context: RunContext,
    mock_adapter: MagicMock,
    mock_playwright: MagicMock,
) -> None:
    mock_context.fuente_corriente = mock_context.fuentes_filtradas[0]
    mock_adapter.enter_source.side_effect = FlowError("fuente_inalcanzable", "Down")

    with patch("time.sleep"):
        res = ejecutar_ingreso(mock_context)

    assert res.estado == "ok"
    assert _entry_result(mock_context).estado == "fallo"
    assert _entry_result(mock_context).codigo_motivo == "fuente_inalcanzable"
    assert mock_context.browser is None
    assert mock_context.playwright_instance is None


def test_ejecutar_ingreso_bloqueo_inmediato(
    mock_context: RunContext,
    mock_adapter: MagicMock,
    mock_playwright: MagicMock,
) -> None:
    mock_context.fuente_corriente = mock_context.fuentes_filtradas[0]
    mock_adapter.enter_source.side_effect = FlowError("bloqueo_plataforma", "Captcha")

    res = ejecutar_ingreso(mock_context)

    assert res.estado == "ok"
    assert _entry_result(mock_context).estado == "fallo"
    assert _entry_result(mock_context).codigo_motivo == "bloqueo_plataforma"
    assert mock_adapter.enter_source.call_count == 1


def test_ejecutar_ingreso_auth_rechazada(
    mock_context: RunContext,
    mock_adapter: MagicMock,
    mock_playwright: MagicMock,
) -> None:
    ficha = mock_context.fuentes_filtradas[0]
    ficha.tipo_acceso = "con_autenticacion"
    ficha.credenciales_referencia = ["U"]
    mock_context.fuente_corriente = ficha

    with patch("modules.discovery.nodes.ingreso.load") as mock_load:
        mock_load.return_value = {"_env": {"U": "val"}}
        mock_adapter.enter_source.side_effect = FlowError(
            "autenticacion_rechazada", "Bad pass"
        )

        res = ejecutar_ingreso(mock_context)
        assert res.estado == "ok"
        assert _entry_result(mock_context).estado == "fallo"
        assert _entry_result(mock_context).codigo_motivo == "autenticacion_rechazada"


def test_ejecutar_ingreso_criterio_no_cumplido(
    mock_context: RunContext,
    mock_adapter: MagicMock,
    mock_playwright: MagicMock,
) -> None:
    mock_context.fuente_corriente = mock_context.fuentes_filtradas[0]
    mock_adapter.enter_source.side_effect = FlowError("criterio_no_cumplido", "Not found")

    res = ejecutar_ingreso(mock_context)

    assert res.estado == "ok"
    assert _entry_result(mock_context).estado == "fallo"
    assert _entry_result(mock_context).codigo_motivo == "criterio_no_cumplido"


def test_ejecutar_ingreso_credenciales_claves_canonicas(
    mock_context: RunContext,
    mock_adapter: MagicMock,
    mock_playwright: MagicMock,
) -> None:
    """El dict de credenciales entregado al adaptador usa las claves
    canónicas `username` y `password`, no las referencias del .env.
    """
    ficha = mock_context.fuentes_filtradas[0]
    ficha.tipo_acceso = "con_autenticacion"
    ficha.credenciales_referencia = ["LINKEDIN_EMAIL", "LINKEDIN_PASSWORD"]
    mock_context.fuente_corriente = ficha

    with patch("modules.discovery.nodes.ingreso.load") as mock_load:
        mock_load.return_value = {
            "_env": {"LINKEDIN_EMAIL": "x@y.com", "LINKEDIN_PASSWORD": "s3cr3t"}
        }
        mock_adapter.enter_source.return_value = EntryResult(
            estado="exito", evidencia_acotada="ok", numero_de_intentos=1
        )

        ejecutar_ingreso(mock_context)

        creds_pasadas = mock_adapter.enter_source.call_args.args[2]
        assert creds_pasadas == {"username": "x@y.com", "password": "s3cr3t"}


def test_ejecutar_ingreso_fuente_ausente(mock_context: RunContext) -> None:
    mock_context.fuente_corriente = None

    res = ejecutar_ingreso(mock_context)

    assert res.estado == "error"
    assert res.codigo == "ERR-01"


def test_ingreso_exitoso_si(mock_context: RunContext) -> None:
    mock_context.entry_result = EntryResult(
        estado="exito", codigo_motivo="", evidencia_acotada="ok", numero_de_intentos=1
    )
    mock_context.id_sesion = "SES-1"
    mock_context.handle_sesion = MagicMock()

    res = ingreso_exitoso(mock_context)
    assert res.decision == "si"


def test_ingreso_exitoso_no(mock_context: RunContext) -> None:
    mock_context.entry_result = EntryResult(
        estado="fallo", codigo_motivo="error", evidencia_acotada="bad", numero_de_intentos=1
    )

    res = ingreso_exitoso(mock_context)
    assert res.decision == "no"


def test_ingreso_exitoso_ausente(mock_context: RunContext) -> None:
    mock_context.entry_result = None

    res = ingreso_exitoso(mock_context)
    assert res.estado == "error"
    assert res.codigo == "ERR-01"


def test_ingreso_exitoso_inconsistente(mock_context: RunContext) -> None:
    mock_context.entry_result = EntryResult(
        estado="exito", codigo_motivo="", evidencia_acotada="ok", numero_de_intentos=1
    )
    mock_context.id_sesion = None
    res = ingreso_exitoso(mock_context)
    assert res.estado == "error"
    assert res.codigo == "ERR-02"

def test_ejecutar_ingreso_headless_override(
    mock_context: RunContext,
    mock_adapter: MagicMock,
    mock_playwright: MagicMock,
) -> None:
    """Verifica que BROWSER_HEADLESS=false en .env fuerza headless=False."""
    mock_context.fuente_corriente = mock_context.fuentes_filtradas[0]
    mock_adapter.enter_source.return_value = EntryResult(
        estado="exito", evidencia_acotada="ok", numero_de_intentos=1
    )

    with patch("modules.discovery.nodes.ingreso.load") as mock_load:
        mock_load.return_value = {
            "_env": {"BROWSER_HEADLESS": "false"},
            "browser": {"headless": True},
        }
        res = ejecutar_ingreso(mock_context)

        assert res.estado == "ok"
        mock_playwright.chromium.launch.assert_called_once_with(headless=False)


def test_ejecutar_ingreso_headless_default(
    mock_context: RunContext,
    mock_adapter: MagicMock,
    mock_playwright: MagicMock,
) -> None:
    """Verifica que sin BROWSER_HEADLESS se use browser.headless de config.yaml."""
    mock_context.fuente_corriente = mock_context.fuentes_filtradas[0]
    mock_adapter.enter_source.return_value = EntryResult(
        estado="exito", evidencia_acotada="ok", numero_de_intentos=1
    )

    with patch("modules.discovery.nodes.ingreso.load") as mock_load:
        mock_load.return_value = {"_env": {}, "browser": {"headless": True}}
        res = ejecutar_ingreso(mock_context)

        assert res.estado == "ok"
        mock_playwright.chromium.launch.assert_called_once_with(headless=True)


def test_ejecutar_ingreso_exito_escribe_evento_ingreso_exitoso(
    mock_context: RunContext,
    mock_adapter: MagicMock,
    mock_playwright: MagicMock,
    _mock_evento_ingreso: MagicMock,
) -> None:
    """D30: el ingreso exitoso deja el evento `ingreso_exitoso` (contrato ficha)."""
    mock_context.fuente_corriente = mock_context.fuentes_filtradas[0]
    mock_adapter.enter_source.return_value = EntryResult(
        estado="exito", evidencia_acotada="ok", numero_de_intentos=1
    )

    ejecutar_ingreso(mock_context)

    _mock_evento_ingreso.assert_called_once()
    args = _mock_evento_ingreso.call_args.args[0]
    assert args["codigo"] == "ingreso_exitoso"
    assert args["tipo"] == "suceso"
    assert args["id_sesion"] == mock_context.id_sesion
    assert args["evidencia"] == f"sesion={mock_context.id_sesion}"


def test_ejecutar_ingreso_fallo_no_escribe_evento_exito(
    mock_context: RunContext,
    mock_adapter: MagicMock,
    mock_playwright: MagicMock,
    _mock_evento_ingreso: MagicMock,
) -> None:
    """D30: el ingreso fallido no emite `ingreso_exitoso` (lo tipifica el registro)."""
    mock_context.fuente_corriente = mock_context.fuentes_filtradas[0]
    mock_adapter.enter_source.side_effect = FlowError("fuente_inalcanzable", "Down")

    with patch("time.sleep"):
        ejecutar_ingreso(mock_context)

    _mock_evento_ingreso.assert_not_called()
