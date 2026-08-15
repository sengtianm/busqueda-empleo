import json
from pathlib import Path
from typing import Any

import httpx
from loguru import logger

from shared.config import load
from shared.errors import ConfigurationError, LLMError
from shared.retry import retry_decorator

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_PROMPTS_PATH = _PROJECT_ROOT / "prompts"


def _prompt_path(prompt_id: str) -> Path:
    path = _PROMPTS_PATH / prompt_id
    if not path.suffix:
        path = path.with_suffix(".md")
    return path


def load_prompt(prompt_id: str) -> str:
    path = _prompt_path(prompt_id)
    if not path.exists():
        raise ConfigurationError(
            "001",
            f"Prompt not found: {path}",
            source_module="ia_service",
        )
    return path.read_text(encoding="utf-8")


def render_prompt(template: str, context: dict[str, Any]) -> str:
    result = template
    for key, value in context.items():
        result = result.replace("{{ " + key + " }}", str(value))
        result = result.replace("{{" + key + "}}", str(value))
    return result


def _route_provider(purpose: str) -> str:
    config = load()
    routing = config.get("ai_routing", {})
    provider = routing.get(purpose, "local")
    if not isinstance(provider, str):
        provider = "local"
    if provider not in ("local", "cloud"):
        raise ConfigurationError(
            "003",
            f"Invalid AI provider for purpose '{purpose}': '{provider}'. "
            f"Allowed values: 'local', 'cloud'",
            source_module="ia_service",
        )
    return provider


def _get_local_config() -> dict[str, Any]:
    config = load()
    local_cfg = config.get("ai_local", {})
    env = config.get("_env", {})
    return {
        "host": env.get("OLLAMA_HOST") or local_cfg.get("host", "localhost"),
        "port": int(env.get("OLLAMA_PORT") or local_cfg.get("port", 11434)),
        "model": env.get("OLLAMA_MODEL") or local_cfg.get("model", "qwen3.5:4b"),
        "timeout": int(local_cfg.get("timeout_seconds", 60)),
    }


def _get_cloud_config() -> dict[str, Any]:
    config = load()
    cloud_cfg = config.get("ai_cloud", {})
    env = config.get("_env", {})
    return {
        "endpoint": env.get("IA_CLOUD_ENDPOINT") or cloud_cfg.get("endpoint", ""),
        "model": cloud_cfg.get("model", "gemma4:31b"),
        "api_key": env.get("IA_CLOUD_API_KEY") or "",
        "timeout": int(cloud_cfg.get("timeout_seconds", 120)),
    }


def _enviar(
    url: str,
    headers: dict[str, str],
    payload: dict[str, Any],
    timeout: float,
    servicio: str,
) -> str:
    """POST a un endpoint IA con el mapeo de errores común (LLM-001..003)."""
    try:
        response = httpx.post(url, json=payload, headers=headers, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        return str(data.get("response", ""))
    except httpx.ConnectError:
        raise LLMError(
            "001",
            f"Could not connect to {servicio} at {url}",
            source_module="ia_service",
        )
    except httpx.TimeoutException:
        raise LLMError(
            "002",
            f"Timeout connecting to {servicio} ({timeout}s)",
            source_module="ia_service",
        )
    except httpx.HTTPStatusError as e:
        raise LLMError(
            "003",
            f"{servicio} responded with code {e.response.status_code}",
            source_module="ia_service",
        )


@retry_decorator()
def _send_local(prompt: str) -> str:
    cfg = _get_local_config()
    return _enviar(
        f"http://{cfg['host']}:{cfg['port']}/api/generate",
        {"Content-Type": "application/json"},
        {"model": cfg["model"], "prompt": prompt, "stream": False},
        cfg["timeout"],
        "local Ollama",
    )


@retry_decorator()
def _send_cloud(prompt: str) -> str:
    cfg = _get_cloud_config()
    headers: dict[str, str] = {
        "Content-Type": "application/json",
    }
    if cfg["api_key"]:
        headers["Authorization"] = f"Bearer {cfg['api_key']}"
    return _enviar(
        f"{cfg['endpoint']}/api/generate",
        headers,
        {"model": cfg["model"], "prompt": prompt, "stream": False},
        cfg["timeout"],
        "AI Cloud",
    )


def _validate_response(raw_response: str) -> dict[str, Any]:
    if not raw_response.strip():
        raise LLMError(
            "003",
            "Empty response from AI model",
            source_module="ia_service",
        )
    try:
        data = json.loads(raw_response)
    except json.JSONDecodeError:
        raise LLMError(
            "003",
            "Response is not valid JSON",
            source_module="ia_service",
        )
    if not isinstance(data, dict):
        raise LLMError(
            "004",
            "Unexpected response format: expected a dictionary",
            source_module="ia_service",
        )
    return data


def analyze(
    prompt_id: str, context: dict[str, Any], purpose: str = "evaluation"
) -> dict[str, Any]:
    template = load_prompt(prompt_id)
    final_prompt = render_prompt(template, context)

    provider = _route_provider(purpose)
    logger.debug("Sending prompt to AI | prompt_id={} | provider={}", prompt_id, provider)

    if provider == "cloud":
        raw_response = _send_cloud(final_prompt)
    else:
        raw_response = _send_local(final_prompt)

    logger.debug("Response received from AI | prompt_id={} | provider={}", prompt_id, provider)
    return _validate_response(raw_response)
