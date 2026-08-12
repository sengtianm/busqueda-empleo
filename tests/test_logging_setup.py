"""Tests for shared/logging_setup.py (restored from sub-fase 4.8)."""

import sys
from pathlib import Path
from unittest.mock import patch

from loguru import logger

from shared.logging_setup import setup


def _restaurar_handler() -> None:
    logger.remove()
    logger.add(sys.stderr, level="DEBUG")


def test_setup_crea_archivo_de_log(tmp_path: Path) -> None:
    with patch("shared.logging_setup._logs_path", return_value=tmp_path):
        setup()
    try:
        logger.info("mensaje de prueba verificacion")
        archivos = list(tmp_path.glob("execution_*.log"))
        assert archivos, "No se creo el log de archivo"
        contenido = archivos[0].read_text(encoding="utf-8")
        assert "mensaje de prueba verificacion" in contenido
    finally:
        _restaurar_handler()


def test_setup_aplica_nivel_desde_config(tmp_path: Path) -> None:
    with (
        patch("shared.logging_setup._logs_path", return_value=tmp_path),
        patch("shared.logging_setup._log_level", return_value="WARNING"),
    ):
        setup()
    try:
        logger.info("nivel INFO no debe aparecer")
        logger.warning("nivel WARNING si debe aparecer")
        archivo = next(tmp_path.glob("execution_*.log"))
        contenido = archivo.read_text(encoding="utf-8")
        assert "nivel WARNING si debe aparecer" in contenido
        assert "nivel INFO no debe aparecer" not in contenido
    finally:
        _restaurar_handler()


def test_setup_rotacion_y_retencion_desde_config(tmp_path: Path) -> None:
    add_mock = logger.add
    with (
        patch("shared.logging_setup._logs_path", return_value=tmp_path),
        patch("shared.logging_setup._rotation", return_value="5 MB"),
        patch("shared.logging_setup._retention", return_value=14),
        patch.object(logger, "add", wraps=add_mock) as mock_add,
    ):
        setup()
    try:
        llamadas_archivo = [
            c for c in mock_add.call_args_list if "execution_" in str(c.args[0])
        ]
        assert llamadas_archivo, "No se registro el sink de archivo"
        kwargs = llamadas_archivo[0].kwargs
        assert kwargs.get("rotation") == "5 MB"
        assert kwargs.get("retention") == "14 days"
    finally:
        _restaurar_handler()
