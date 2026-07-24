import sys
from pathlib import Path

from loguru import logger

from shared.config import cargar


def _ruta_logs() -> Path:
    config = cargar()
    return Path(config.get("persistencia", {}).get("ruta_data", "data")).parent / "logs"


def _nivel_log() -> str:
    config = cargar()
    env_nivel = config.get("_env", {}).get("LOG_LEVEL")
    if env_nivel:
        return str(env_nivel).upper()
    return str(config.get("logging", {}).get("nivel", "DEBUG")).upper()


def _rotacion() -> str:
    return str(cargar().get("logging", {}).get("rotacion", "10 MB"))


def _retencion() -> int:
    return int(cargar().get("logging", {}).get("retencion_dias", 30))


def configurar() -> None:
    logger.remove()

    logger.add(
        sys.stderr,
        level=_nivel_log(),
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green>"
            " | <level>{level: <8}</level>"
            " | <cyan>{module}</cyan> | {message}"
        ),
        colorize=True,
    )

    ruta = _ruta_logs()
    ruta.mkdir(parents=True, exist_ok=True)
    archivo_log = ruta / "ejecucion_{time:YYYY-MM-DD}.log"

    logger.add(
        str(archivo_log),
        level=_nivel_log(),
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {module} | {message}",
        rotation=_rotacion(),
        retention=f"{_retencion()} days",
        encoding="utf-8",
    )
