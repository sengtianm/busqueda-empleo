"""Unit tests for the evidence truncation and text normalization helpers (DOC-06, DOC-13A, D33)."""

from shared.utilidades import acotar_evidencia, normalizar_texto


def test_acotar_evidencia_texto_corto() -> None:
    assert acotar_evidencia("evidencia corta") == "evidencia corta"


def test_acotar_evidencia_limite_exacto() -> None:
    assert acotar_evidencia("x" * 300) == "x" * 300


def test_acotar_evidencia_texto_largo() -> None:
    assert acotar_evidencia("x" * 400) == "x" * 300 + "..."


def test_normalizar_texto_minusculas_sin_acentos_ni_puntuacion() -> None:
    assert normalizar_texto("Bogotá D.C.") == "bogota d c"


def test_normalizar_texto_colapsa_espacios() -> None:
    assert normalizar_texto("  Data   Engineer\tSenior  ") == "data engineer senior"


def test_normalizar_texto_simbolos() -> None:
    assert normalizar_texto("H&M Group, S.A.") == "h m group s a"


def test_normalizar_texto_vacio() -> None:
    assert normalizar_texto("") == ""
