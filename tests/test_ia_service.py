import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import httpx
import pytest

from shared.errors import ConfigurationError, LLMError
from shared.ia_service import (
    _route_provider,
    _send_cloud,
    _send_local,
    _validate_response,
    analyze,
    load_prompt,
    render_prompt,
)


def test_render_prompt_simple() -> None:
    template = "Evalua la oferta {{ titulo }} para el rol {{ rol }}"
    context = {"titulo": "Data Engineer", "rol": "Ingeniero de Datos"}
    result = render_prompt(template, context)
    assert "Data Engineer" in result
    assert "Ingeniero de Datos" in result


def test_load_prompt_missing() -> None:
    with pytest.raises(ConfigurationError, match="ER-CFG-001"):
        load_prompt("initial_evaluation/nonexistent")


@patch("shared.ia_service.httpx.post")
def test_send_local_success(mock_post: MagicMock) -> None:
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"response": '{"ok": true}'}

    result = _send_local("test prompt")
    assert result == '{"ok": true}'
    mock_post.assert_called_once()


@patch("shared.ia_service.httpx.post")
def test_send_local_connection_error(mock_post: MagicMock) -> None:
    mock_post.side_effect = httpx.ConnectError("No se pudo conectar")

    with pytest.raises(LLMError, match="ER-LLM-001"):
        _send_local("test prompt")


@patch("shared.ia_service.httpx.post")
def test_send_local_timeout(mock_post: MagicMock) -> None:
    mock_post.side_effect = httpx.TimeoutException("Timeout")

    with pytest.raises(LLMError, match="ER-LLM-002"):
        _send_local("test prompt")


@patch("shared.ia_service.httpx.post")
def test_send_cloud_success(mock_post: MagicMock) -> None:
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"response": '{"ok": true}'}

    result = _send_cloud("test prompt")
    assert result == '{"ok": true}'
    mock_post.assert_called_once()


@patch("shared.ia_service.httpx.post")
def test_send_cloud_connection_error(mock_post: MagicMock) -> None:
    mock_post.side_effect = httpx.ConnectError("No se pudo conectar")

    with pytest.raises(LLMError, match="ER-LLM-001"):
        _send_cloud("test prompt")


@patch("shared.ia_service.httpx.post")
def test_send_cloud_http_error(mock_post: MagicMock) -> None:
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Unauthorized", request=MagicMock(), response=mock_response
    )
    mock_post.return_value = mock_response

    with pytest.raises(LLMError, match="ER-LLM-003"):
        _send_cloud("test prompt")


def test_route_provider_ok() -> None:
    assert _route_provider("evaluation") == "cloud"
    assert _route_provider("processing") == "cloud"


@patch("shared.ia_service.load")
def test_route_provider_invalid(mock_load: MagicMock) -> None:
    mock_load.return_value = {
        "ai_routing": {"evaluation": "local", "processing": "aws"}
    }
    with pytest.raises(ConfigurationError, match="ER-CFG-003"):
        _route_provider("processing")


def test_validate_response_ok() -> None:
    result = _validate_response('{"compatibilidad": "alta"}')
    assert result == {"compatibilidad": "alta"}


def test_validate_response_empty() -> None:
    with pytest.raises(LLMError, match="ER-LLM-003"):
        _validate_response("")


def test_validate_response_not_json() -> None:
    with pytest.raises(LLMError, match="ER-LLM-003"):
        _validate_response("no es json")


def test_validate_response_not_dict() -> None:
    with pytest.raises(LLMError, match="ER-LLM-004"):
        _validate_response('["lista", "no valida"]')


@patch("shared.ia_service.httpx.post")
def test_analyze_local(mock_post: MagicMock, tmp_path: Path) -> None:
    prompts_dir = Path(__file__).resolve().parent.parent / "prompts"
    category = prompts_dir / "test_category"
    category.mkdir(parents=True, exist_ok=True)
    prompt_file = category / "test_prompt.md"
    prompt_file.write_text("Evalua {{ titulo }}", encoding="utf-8")

    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "response": json.dumps({"compatibilidad": "alta"})
    }

    result = analyze(
        "test_category/test_prompt",
        {"titulo": "Data Engineer"},
        purpose="evaluation",
    )
    assert result == {"compatibilidad": "alta"}

    prompt_file.unlink()
    category.rmdir()
