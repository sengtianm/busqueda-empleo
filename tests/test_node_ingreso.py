from unittest.mock import MagicMock, patch

import pytest

from modules.discovery.adapters.linkedin import FlowError
from modules.discovery.nodes.ingreso import (
    ejecutar_ingreso,
    ingreso_exitoso,
    registrar_evento_fallo,
)
from modules.discovery.run_context import RunContext
from shared.models import EntryResult, TipoEvento


@pytest.fixture
def mock_context():
    # Mock de config_fuentes para crear RunContext
    config_fuentes = [{
        "source_id": "LI-01",
        "nombre": "LinkedIn",
        "ficha_acceso": {
            "url": "https://linkedin.com",
            "tipo_acceso": "publico",
            "criterio_exito": "global-nav",
            "timeout_segundos": 10
        }
    }]
    return RunContext(config_fuentes=config_fuentes)

@pytest.fixture
def mock_adapter():
    with patch("modules.discovery.nodes.ingreso.LinkedInAdapter") as mock:
        yield mock.return_value

def test_ejecutar_ingreso_publico_exito(mock_context, mock_adapter):
    # Arrange
    mock_context.fuente_corriente = mock_context.fuentes_filtradas[0]
    mock_adapter.enter_source.return_value = EntryResult(
        estado="exito", evidencia_acotada="ok", numero_de_intentos=1
    )

    # Act
    res = ejecutar_ingreso(mock_context)

    # Assert
    assert res.estado == "ok"
    assert mock_context.entry_result.estado == "exito"
    assert mock_context.session_id is not None
    assert mock_context.handle_sesion is not None

def test_ejecutar_ingreso_autenticado_exito(mock_context, mock_adapter):
    # Arrange
    ficha = mock_context.fuentes_filtradas[0]
    ficha.tipo_acceso = "con_autenticacion"
    ficha.credenciales_referencia = ["USER", "PASS"]
    mock_context.fuente_corriente = ficha

    with patch("shared.config.load") as mock_load:
        mock_load.return_value = {"_env": {"USER": "test@test.com", "PASS": "1234"}}
        mock_adapter.enter_source.return_value = EntryResult(
            estado="exito", evidencia_acotada="ok", numero_de_intentos=1
        )

        res = ejecutar_ingreso(mock_context)
        assert res.estado == "ok"
        assert mock_context.entry_result.estado == "exito"

def test_ejecutar_ingreso_sin_credenciales(mock_context):
    # Arrange
    ficha = mock_context.fuentes_filtradas[0]
    ficha.tipo_acceso = "con_autenticacion"
    ficha.credenciales_referencia = ["USER"]
    mock_context.fuente_corriente = ficha

    with patch("shared.config.load") as mock_load:
        mock_load.return_value = {"_env": {}} # Vacío
        res = ejecutar_ingreso(mock_context)

        assert res.estado == "ok"
        assert mock_context.entry_result.estado == "fallo"
        assert mock_context.entry_result.codigo_motivo == "credenciales_no_disponibles"

def test_ejecutar_ingreso_reintento_exito(mock_context, mock_adapter):
    # Arrange
    mock_context.fuente_corriente = mock_context.fuentes_filtradas[0]
    # Fallo reintentable primero, luego éxito
    mock_adapter.enter_source.side_effect = [
        FlowError("fuente_inalcanzable", "Down"),
        EntryResult(estado="exito", evidencia_acotada="ok", numero_de_intentos=2)
    ]

    with patch("time.sleep"): # No esperar en tests
        res = ejecutar_ingreso(mock_context)

    assert res.estado == "ok"
    assert mock_context.entry_result.estado == "exito"
    assert mock_adapter.enter_source.call_count == 2

def test_ejecutar_ingreso_reintentos_agotados(mock_context, mock_adapter):
    # Arrange
    mock_context.fuente_corriente = mock_context.fuentes_filtradas[0]
    mock_adapter.enter_source.side_effect = FlowError("fuente_inalcanzable", "Down")

    with patch("time.sleep"):
        res = ejecutar_ingreso(mock_context)

    assert res.estado == "ok"
    assert mock_context.entry_result.estado == "fallo"
    assert mock_context.entry_result.codigo_motivo == "fuente_inalcanzable"

def test_ejecutar_ingreso_bloqueo_inmediato(mock_context, mock_adapter):
    # Arrange
    mock_context.fuente_corriente = mock_context.fuentes_filtradas[0]
    mock_adapter.enter_source.side_effect = FlowError("bloqueo_plataforma", "Captcha")

    res = ejecutar_ingreso(mock_context)

    assert res.estado == "ok"
    assert mock_context.entry_result.estado == "fallo"
    assert mock_context.entry_result.codigo_motivo == "bloqueo_plataforma"
    assert mock_adapter.enter_source.call_count == 1

def test_ejecutar_ingreso_auth_rechazada(mock_context, mock_adapter):
    # Arrange
    ficha = mock_context.fuentes_filtradas[0]
    ficha.tipo_acceso = "con_autenticacion"
    ficha.credenciales_referencia = ["U"]
    mock_context.fuente_corriente = ficha

    with patch("shared.config.load") as mock_load:
        mock_load.return_value = {"_env": {"U": "val"}}
        mock_adapter.enter_source.side_effect = FlowError("autenticacion_rechazada", "Bad pass")

        res = ejecutar_ingreso(mock_context)
        assert res.estado == "ok"
        assert mock_context.entry_result.estado == "fallo"
        assert mock_context.entry_result.codigo_motivo == "autenticacion_rechazada"

def test_ejecutar_ingreso_criterio_no_cumplido(mock_context, mock_adapter):
    # Arrange
    mock_context.fuente_corriente = mock_context.fuentes_filtradas[0]
    mock_adapter.enter_source.side_effect = FlowError("criterio_no_cumplido", "Not found")

    res = ejecutar_ingreso(mock_context)

    assert res.estado == "ok"
    assert mock_context.entry_result.estado == "fallo"
    assert mock_context.entry_result.codigo_motivo == "criterio_no_cumplido"

def test_ejecutar_ingreso_fuente_ausente(mock_context):
    # Arrange
    mock_context.fuente_corriente = None

    res = ejecutar_ingreso(mock_context)

    assert res.estado == "error"
    assert res.codigo == "ERR-01"

def test_ingreso_exitoso_si(mock_context):
    # Arrange
    mock_context.entry_result = EntryResult(
        estado="exito", codigo_motivo="", evidencia_acotada="ok", numero_de_intentos=1
    )
    mock_context.session_id = "SES-1"
    mock_context.handle_sesion = MagicMock()

    res = ingreso_exitoso(mock_context)
    assert res.decision == "si"

def test_ingreso_exitoso_no(mock_context):
    # Arrange
    mock_context.entry_result = EntryResult(
        estado="fallo", codigo_motivo="error", evidencia_acotada="bad", numero_de_intentos=1
    )

    res = ingreso_exitoso(mock_context)
    assert res.decision == "no"

def test_ingreso_exitoso_ausente(mock_context):
    # Arrange
    mock_context.entry_result = None

    res = ingreso_exitoso(mock_context)
    assert res.estado == "error"
    assert res.codigo == "ERR-01"

def test_ingreso_exitoso_inconsistente(mock_context):
    # Arrange
    mock_context.entry_result = EntryResult(
        estado="exito", codigo_motivo="", evidencia_acotada="ok", numero_de_intentos=1
    )
    mock_context.session_id = None # Error: éxito sin sesión

    res = ingreso_exitoso(mock_context)
    assert res.estado == "error"
    assert res.codigo == "ERR-02"

def test_registrar_evento_fallo_error(mock_context):
    # Arrange
    mock_context.fuente_corriente = MagicMock(source_id="S1")
    mock_context.entry_result = EntryResult(
        estado="fallo", codigo_motivo="ERR_X", evidencia_acotada="evid", numero_de_intentos=2
    )

    with patch("modules.discovery.nodes.ingreso.write_evento") as mock_write:
        res = registrar_evento_fallo(mock_context)
        assert res.estado == "ok"
        mock_write.assert_called_once()
        args = mock_write.call_args.kwargs
        assert args["tipo"] == TipoEvento.ERROR
        assert args["codigo"] == "ERR_X"

def test_registrar_evento_exito(mock_context):
    # Arrange
    mock_context.fuente_corriente = MagicMock(source_id="S1")
    mock_context.entry_result = EntryResult(
        estado="exito", codigo_motivo="OK", evidencia_acotada="evid", numero_de_intentos=1
    )

    with patch("modules.discovery.nodes.ingreso.write_evento") as mock_write:
        res = registrar_evento_fallo(mock_context)
        assert res.estado == "ok"
        args = mock_write.call_args.kwargs
        assert args["tipo"] == TipoEvento.SUCESO

def test_registrar_evento_db_fail(mock_context):
    # Arrange
    mock_context.fuente_corriente = MagicMock(source_id="S1")
    mock_context.entry_result = EntryResult(
        estado="fallo", codigo_motivo="X", evidencia_acotada="evid", numero_de_intentos=1
    )

    with patch("modules.discovery.nodes.ingreso.write_evento", side_effect=Exception("DB Down")):
        res = registrar_evento_fallo(mock_context)
        assert res.estado == "ok" # No aborta
