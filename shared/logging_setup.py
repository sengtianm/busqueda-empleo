import sys
from pathlib import Path

from loguru import logger

from shared.config import load


def _logs_path() -> Path:
    config = load()
    return Path(config.get("persistence", {}).get("data_path", "data")).parent / "logs"


def _log_level() -> str:
    config = load()
    env_nivel = config.get("_env", {}).get("LOG_LEVEL")
    if env_nivel:
        return str(env_nivel).upper()
    return str(config.get("logging", {}).get("nivel", "DEBUG")).upper()


def _rotation() -> str:
    return str(load().get("logging", {}).get("rotacion", "10 MB"))


def _retention() -> int:
    return int(load().get("logging", {}).get("retencion_dias", 30))


def configurar() -> None:
    logger.remove()

    logger.add(
        sys.stderr,
        level=_log_level(),
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green>"
            " | <level>{level: <8}</level>"
            " | <cyan>{module}</cyan> | {message}"
        ),
        colorize=True,
    )

    ruta = _logs_path()
    ruta.mkdir(parents=True, exist_ok=True)
    log_file = ruta / "ejecucion_{time:YYYY-MM-DD}.log"

    logger.add(
        str(log_file),
        level=_log_level(),
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {module} | {message}",
        rotation=_rotation(),
        retention=f"{_retention()} days",
        encoding="utf-8",
    )
