"""Unit tests for the evidence truncation helper (DOC-06, DOC-13A)."""

from shared.utilidades import acotar_evidencia


def test_acotar_evidencia_texto_corto() -> None:
    assert acotar_evidencia("evidencia corta") == "evidencia corta"


def test_acotar_evidencia_limite_exacto() -> None:
    assert acotar_evidencia("x" * 300) == "x" * 300


def test_acotar_evidencia_texto_largo() -> None:
    assert acotar_evidencia("x" * 400) == "x" * 300 + "..."
