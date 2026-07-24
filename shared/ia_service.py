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


def _obtener_config_ollama() -> dict[str, Any]:
    config = cargar()
    ollama_cfg = config.get("ollama", {})
    env = config.get("_env", {})
    return {
        "host": env.get("OLLAMA_HOST") or ollama_cfg.get("host", "localhost"),
        "puerto": int(env.get("OLLAMA_PORT") or ollama_cfg.get("puerto", 11434)),
        "modelo": env.get("OLLAMA_MODEL") or ollama_cfg.get("modelo", "qwen:8b"),
        "timeout": int(env.get("OLLAMA_TIMEOUT") or ollama_cfg.get("timeout_segundos", 60)),
    }


@decorador_reintento()
def _enviar_ollama(prompt: str) -> str:
    cfg = _obtener_config_ollama()
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
            f"No se pudo conectar a Ollama en {url}",
            modulo_origen="ia_service",
        )
    except httpx.TimeoutException:
        raise ErrorLLM(
            "002",
            f"Timeout al conectar con Ollama ({cfg['timeout']}s)",
            modulo_origen="ia_service",
        )
    except httpx.HTTPStatusError as e:
        raise ErrorLLM(
            "003",
            f"Ollama respondio con codigo {e.response.status_code}",
            modulo_origen="ia_service",
        )


def _validar_respuesta(respuesta_raw: str) -> dict[str, Any]:
    import json

    if not respuesta_raw.strip():
        raise ErrorLLM(
            "003",
            "Respuesta vacia de Ollama",
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


def analizar(prompt_id: str, contexto: dict[str, Any]) -> dict[str, Any]:
    template = cargar_prompt(prompt_id)
    prompt_final = renderizar_prompt(template, contexto)
    from loguru import logger

    logger.debug("Enviando prompt a Ollama | prompt_id={}", prompt_id)
    respuesta_raw = _enviar_ollama(prompt_final)
    logger.debug("Respuesta recibida de Ollama | prompt_id={}", prompt_id)
    return _validar_respuesta(respuesta_raw)
