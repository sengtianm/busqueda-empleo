from pathlib import Path
from typing import Any

import httpx

from shared.config import cargar
from shared.errors import ErrorConfiguracion, ErrorLLM
from shared.retry import decorador_reintento

_RAIZ_PROYECTO = Path(__file__).resolve().parent.parent
_RUTA_PROMPTS = _RAIZ_PROYECTO / "prompts"


def _ruta_prompt(prompt_id: str) -> Path:
    ruta = _RUTA_PROMPTS / prompt_id
    if not ruta.suffix:
        ruta = ruta.with_suffix(".md")
    return ruta


def cargar_prompt(prompt_id: str) -> str:
    ruta = _ruta_prompt(prompt_id)
    if not ruta.exists():
        raise ErrorConfiguracion(
            "001",
            f"Prompt no encontrado: {ruta}",
            modulo_origen="ia_service",
        )
    return ruta.read_text(encoding="utf-8")


def renderizar_prompt(template: str, contexto: dict[str, Any]) -> str:
    resultado = template
    for clave, valor in contexto.items():
        resultado = resultado.replace("{{ " + clave + " }}", str(valor))
        resultado = resultado.replace("{{" + clave + "}}", str(valor))
    return resultado


def _route_provider(proposito: str) -> str:
    config = cargar()
    routing = config.get("ia_routing", {})
    proveedor = routing.get(proposito, "local")
    if not isinstance(proveedor, str):
        proveedor = "local"
    if proveedor not in ("local", "cloud"):
        raise ErrorConfiguracion(
            "003",
            f"Proveedor de IA invalido para proposito '{proposito}': '{proveedor}'. "
            f"Valores permitidos: 'local', 'cloud'",
            modulo_origen="ia_service",
        )
    return proveedor


def _obtener_config_local() -> dict[str, Any]:
    config = cargar()
    local_cfg = config.get("ia_local", {})
    env = config.get("_env", {})
    return {
        "host": env.get("OLLAMA_HOST") or local_cfg.get("host", "localhost"),
        "puerto": int(env.get("OLLAMA_PORT") or local_cfg.get("puerto", 11434)),
        "modelo": env.get("OLLAMA_MODEL") or local_cfg.get("modelo", "qwen3.5:4b"),
        "timeout": int(local_cfg.get("timeout_segundos", 60)),
    }


def _obtener_config_cloud() -> dict[str, Any]:
    config = cargar()
    cloud_cfg = config.get("ia_cloud", {})
    env = config.get("_env", {})
    return {
        "endpoint": env.get("IA_CLOUD_ENDPOINT") or cloud_cfg.get("endpoint", ""),
        "modelo": cloud_cfg.get("modelo", "gemma4:31b"),
        "api_key": env.get("IA_CLOUD_API_KEY") or "",
        "timeout": int(cloud_cfg.get("timeout_segundos", 120)),
    }


@decorador_reintento()
def _enviar_local(prompt: str) -> str:
    cfg = _obtener_config_local()
    url = f"http://{cfg['host']}:{cfg['puerto']}/api/generate"
    payload = {"model": cfg["modelo"], "prompt": prompt, "stream": False}
    try:
        respuesta = httpx.post(url, json=payload, timeout=cfg["timeout"])
        respuesta.raise_for_status()
        data = respuesta.json()
        return str(data.get("response", ""))
    except httpx.ConnectError:
        raise ErrorLLM(
            "001",
            f"No se pudo conectar a Ollama local en {url}",
            modulo_origen="ia_service",
        )
    except httpx.TimeoutException:
        raise ErrorLLM(
            "002",
            f"Timeout al conectar con Ollama local ({cfg['timeout']}s)",
            modulo_origen="ia_service",
        )
    except httpx.HTTPStatusError as e:
        raise ErrorLLM(
            "003",
            f"Ollama local respondio con codigo {e.response.status_code}",
            modulo_origen="ia_service",
        )


@decorador_reintento()
def _enviar_cloud(prompt: str) -> str:
    cfg = _obtener_config_cloud()
    url = f"{cfg['endpoint']}/api/generate"
    headers: dict[str, str] = {
        "Content-Type": "application/json",
    }
    if cfg["api_key"]:
        headers["Authorization"] = f"Bearer {cfg['api_key']}"
    payload = {"model": cfg["modelo"], "prompt": prompt, "stream": False}
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
            f"No se pudo conectar a IA Cloud en {url}",
            modulo_origen="ia_service",
        )
    except httpx.TimeoutException:
        raise ErrorLLM(
            "002",
            f"Timeout al conectar con IA Cloud ({cfg['timeout']}s)",
            modulo_origen="ia_service",
        )
    except httpx.HTTPStatusError as e:
        raise ErrorLLM(
            "003",
            f"IA Cloud respondio con codigo {e.response.status_code}",
            modulo_origen="ia_service",
        )


def _validar_respuesta(respuesta_raw: str) -> dict[str, Any]:
    import json

    if not respuesta_raw.strip():
        raise ErrorLLM(
            "003",
            "Respuesta vacia del modelo de IA",
            modulo_origen="ia_service",
        )
    try:
        data = json.loads(respuesta_raw)
    except json.JSONDecodeError:
        raise ErrorLLM(
            "003",
            "Respuesta no es JSON valido",
            modulo_origen="ia_service",
        )
    if not isinstance(data, dict):
        raise ErrorLLM(
            "004",
            "Formato de respuesta inesperado: se esperaba un diccionario",
            modulo_origen="ia_service",
        )
    return data


def analizar(
    prompt_id: str, contexto: dict[str, Any], proposito: str = "evaluacion"
) -> dict[str, Any]:
    template = cargar_prompt(prompt_id)
    prompt_final = renderizar_prompt(template, contexto)
    from loguru import logger

    proveedor = _route_provider(proposito)
    logger.debug("Enviando prompt a IA | prompt_id={} | proveedor={}", prompt_id, proveedor)

    if proveedor == "cloud":
        respuesta_raw = _enviar_cloud(prompt_final)
    else:
        respuesta_raw = _enviar_local(prompt_final)

    logger.debug("Respuesta recibida de IA | prompt_id={} | proveedor={}", prompt_id, proveedor)
    return _validar_respuesta(respuesta_raw)
