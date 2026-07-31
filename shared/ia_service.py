from pathlib import Path
from typing import Any

import httpx

from shared.config import load
from shared.errors import ConfigurationError, ErrorLLM
from shared.retry import decorador_reintento

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


def renderizar_prompt(template: str, contexto: dict[str, Any]) -> str:
    resultado = template
    for clave, valor in contexto.items():
        resultado = resultado.replace("{{ " + clave + " }}", str(valor))
        resultado = resultado.replace("{{" + clave + "}}", str(valor))
    return resultado


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


@decorador_reintento()
def _send_local(prompt: str) -> str:
    cfg = _get_local_config()
    url = f"http://{cfg['host']}:{cfg['port']}/api/generate"
    payload = {"model": cfg["model"], "prompt": prompt, "stream": False}
    try:
        respuesta = httpx.post(url, json=payload, timeout=cfg["timeout"])
        respuesta.raise_for_status()
        data = respuesta.json()
        return str(data.get("response", ""))
    except httpx.ConnectError:
        raise ErrorLLM(
            "001",
            f"Could not connect to local Ollama at {url}",
            source_module="ia_service",
        )
    except httpx.TimeoutException:
        raise ErrorLLM(
            "002",
            f"Timeout connecting to local Ollama ({cfg['timeout']}s)",
            source_module="ia_service",
        )
    except httpx.HTTPStatusError as e:
        raise ErrorLLM(
            "003",
            f"Local Ollama responded with code {e.response.status_code}",
            source_module="ia_service",
        )


@decorador_reintento()
def _send_cloud(prompt: str) -> str:
    cfg = _get_cloud_config()
    url = f"{cfg['endpoint']}/api/generate"
    headers: dict[str, str] = {
        "Content-Type": "application/json",
    }
    if cfg["api_key"]:
        headers["Authorization"] = f"Bearer {cfg['api_key']}"
    payload = {"model": cfg["model"], "prompt": prompt, "stream": False}
    try:
        respuesta = httpx.post(
            url, json=payload, headers=headers, timeout=cfg["timeout"]
        )
        respuesta.raise_for_status()
        data = respuesta.json()
        return str(data.get("response", ""))
    except httpx.ConnectError:
        raise ErrorLLM(
            "001",
            f"Could not connect to AI Cloud at {url}",
            source_module="ia_service",
        )
    except httpx.TimeoutException:
        raise ErrorLLM(
            "002",
            f"Timeout connecting to AI Cloud ({cfg['timeout']}s)",
            source_module="ia_service",
        )
    except httpx.HTTPStatusError as e:
        raise ErrorLLM(
            "003",
            f"AI Cloud responded with code {e.response.status_code}",
            source_module="ia_service",
        )


def _validate_response(respuesta_raw: str) -> dict[str, Any]:
    import json

    if not respuesta_raw.strip():
        raise ErrorLLM(
            "003",
            "Empty response from AI model",
            source_module="ia_service",
        )
    try:
        data = json.loads(respuesta_raw)
    except json.JSONDecodeError:
        raise ErrorLLM(
            "003",
            "Response is not valid JSON",
            source_module="ia_service",
        )
    if not isinstance(data, dict):
        raise ErrorLLM(
            "004",
            "Unexpected response format: expected a dictionary",
            source_module="ia_service",
        )
    return data


def analyze(
    prompt_id: str, contexto: dict[str, Any], purpose: str = "evaluation"
) -> dict[str, Any]:
    template = load_prompt(prompt_id)
    prompt_final = renderizar_prompt(template, contexto)
    from loguru import logger

    provider = _route_provider(purpose)
    logger.debug("Sending prompt to AI | prompt_id={} | provider={}", prompt_id, provider)

    if provider == "cloud":
        respuesta_raw = _send_cloud(prompt_final)
    else:
        respuesta_raw = _send_local(prompt_final)

    logger.debug("Response received from AI | prompt_id={} | provider={}", prompt_id, provider)
    return _validate_response(respuesta_raw)
