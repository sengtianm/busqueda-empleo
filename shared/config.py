from pathlib import Path
from typing import Any

import yaml
from dotenv import dotenv_values

_RAIZ_PROYECTO = Path(__file__).resolve().parent.parent
_RUTA_CONFIG = _RAIZ_PROYECTO / "config" / "config.yaml"
_RUTA_ENV = _RAIZ_PROYECTO / "config" / ".env"


def _cargar_yaml(ruta: Path) -> dict[str, Any]:
    with open(ruta, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _cargar_env(ruta: Path) -> dict[str, str]:
    return {k: v for k, v in dotenv_values(ruta).items() if v is not None}


_config_cache: dict[str, Any] | None = None


def cargar() -> dict[str, Any]:
    global _config_cache
    if _config_cache is not None:
        return _config_cache

    base = _cargar_yaml(_RUTA_CONFIG)

    if _RUTA_ENV.exists():
        env_vars = _cargar_env(_RUTA_ENV)
        base["_env"] = env_vars
    else:
        base["_env"] = {}

    _config_cache = base
    return _config_cache


def recargar() -> dict[str, Any]:
    global _config_cache
    _config_cache = None
    return cargar()
