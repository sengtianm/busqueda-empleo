import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import httpx
import pytest

from shared.errors import ErrorConfiguracion, ErrorLLM
from shared.ia_service import (
    _enviar_cloud,
    _enviar_local,
    _route_provider,
    _validar_respuesta,
    analizar,
    cargar_prompt,
    renderizar_prompt,
)


def test_renderizar_prompt_simple() -> None:
    template = "Evalua la oferta {{ titulo }} para el rol {{ rol }}"
    contexto = {"titulo": "Data Engineer", "rol": "Ingeniero de Datos"}
    resultado = renderizar_prompt(template, contexto)
    assert "Data Engineer" in resultado
    assert "Ingeniero de Datos" in resultado


def test_cargar_prompt_inexistente() -> None:
    with pytest.raises(ErrorConfiguracion, match="ER-CFG-001"):
        cargar_prompt("evaluacion_inicial/inexistente")


@patch("shared.ia_service.httpx.post")
def test_enviar_local_exitoso(mock_post: MagicMock) -> None:
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"response": '{"ok": true}'}

    resultado = _enviar_local("test prompt")
    assert resultado == '{"ok": true}'
    mock_post.assert_called_once()


@patch("shared.ia_service.httpx.post")
def test_enviar_local_error_conexion(mock_post: MagicMock) -> None:
    mock_post.side_effect = httpx.ConnectError("No se pudo conectar")

    with pytest.raises(ErrorLLM, match="ER-LLM-001"):
        _enviar_local("test prompt")


@patch("shared.ia_service.httpx.post")
def test_enviar_local_timeout(mock_post: MagicMock) -> None:
    mock_post.side_effect = httpx.TimeoutException("Timeout")

    with pytest.raises(ErrorLLM, match="ER-LLM-002"):
        _enviar_local("test prompt")


@patch("shared.ia_service.httpx.post")
def test_enviar_cloud_exitoso(mock_post: MagicMock) -> None:
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"response": '{"ok": true}'}

    resultado = _enviar_cloud("test prompt")
    assert resultado == '{"ok": true}'
    mock_post.assert_called_once()


@patch("shared.ia_service.httpx.post")
def test_enviar_cloud_error_conexion(mock_post: MagicMock) -> None:
    mock_post.side_effect = httpx.ConnectError("No se pudo conectar")

    with pytest.raises(ErrorLLM, match="ER-LLM-001"):
        _enviar_cloud("test prompt")


@patch("shared.ia_service.httpx.post")
def test_enviar_cloud_http_error(mock_post: MagicMock) -> None:
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Unauthorized", request=MagicMock(), response=mock_response
    )
    mock_post.return_value = mock_response

    with pytest.raises(ErrorLLM, match="ER-LLM-003"):
        _enviar_cloud("test prompt")


def test_route_provider_ok() -> None:
    assert _route_provider("evaluacion") == "cloud"
    assert _route_provider("procesamiento") == "cloud"


@patch("shared.ia_service.cargar")
def test_route_provider_invalido(mock_cargar: MagicMock) -> None:
    mock_cargar.return_value = {
        "ia_routing": {"evaluacion": "local", "procesamiento": "aws"}
    }
    with pytest.raises(ErrorConfiguracion, match="ER-CFG-003"):
        _route_provider("procesamiento")


def test_validar_respuesta_ok() -> None:
    resultado = _validar_respuesta('{"compatibilidad": "alta"}')
    assert resultado == {"compatibilidad": "alta"}


def test_validar_respuesta_vacia() -> None:
    with pytest.raises(ErrorLLM, match="ER-LLM-003"):
        _validar_respuesta("")


def test_validar_respuesta_no_json() -> None:
    with pytest.raises(ErrorLLM, match="ER-LLM-003"):
        _validar_respuesta("no es json")


def test_validar_respuesta_no_dict() -> None:
    with pytest.raises(ErrorLLM, match="ER-LLM-004"):
        _validar_respuesta('["lista", "no valida"]')


@patch("shared.ia_service.httpx.post")
def test_analizar_local(mock_post: MagicMock, tmp_path: Path) -> None:
    prompts_dir = Path(__file__).resolve().parent.parent / "prompts"
    categoria = prompts_dir / "test_categoria"
    categoria.mkdir(parents=True, exist_ok=True)
    archivo_prompt = categoria / "test_prompt.md"
    archivo_prompt.write_text("Evalua {{ titulo }}", encoding="utf-8")

    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "response": json.dumps({"compatibilidad": "alta"})
    }

    resultado = analizar(
        "test_categoria/test_prompt",
        {"titulo": "Data Engineer"},
        proposito="evaluacion",
    )
    assert resultado == {"compatibilidad": "alta"}

    archivo_prompt.unlink()
    categoria.rmdir()
