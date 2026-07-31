from pathlib import Path
from typing import Any

import yaml
from dotenv import dotenv_values

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_CONFIG_PATH = _PROJECT_ROOT / "config" / "config.yaml"
_ENV_PATH = _PROJECT_ROOT / "config" / ".env"


def _load_yaml(path: Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _load_env(path: Path) -> dict[str, str]:
    return {k: v for k, v in dotenv_values(path).items() if v is not None}


_config_cache: dict[str, Any] | None = None


def load() -> dict[str, Any]:
    global _config_cache
    if _config_cache is not None:
        return _config_cache

    base = _load_yaml(_CONFIG_PATH)

    if _ENV_PATH.exists():
        env_vars = _load_env(_ENV_PATH)
        base["_env"] = env_vars
    else:
        base["_env"] = {}

    _config_cache = base
    return _config_cache


def reload_config() -> dict[str, Any]:
    global _config_cache
    _config_cache = None
    return load()
