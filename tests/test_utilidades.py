"""Unit tests for the evidence truncation and text normalization helpers (DOC-06, DOC-13A, D33)."""

from shared.utilidades import (
    acotar_evidencia,
    espera_manual_navegador,
    normalizar_nombre_empresa,
    normalizar_texto,
    ruta_perfil_navegador,
    ventana_navegador,
)


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


def test_normalizar_nombre_empresa_conserva_caracteres_d41() -> None:
    assert normalizar_nombre_empresa("CI&T") == "ci&t"
    assert normalizar_nombre_empresa("Claro Colombia S.A.") == "claro colombia s.a."
    assert (
        normalizar_nombre_empresa("Tata Consultancy Services (TCS)")
        == "tata consultancy services (tcs)"
    )


def test_normalizar_nombre_empresa_conserva_tildes_d41() -> None:
    assert normalizar_nombre_empresa("Clínica del País") == "clínica del país"


def test_normalizar_nombre_empresa_colapsa_espacios_d41() -> None:
    assert normalizar_nombre_empresa("  Inetum   \t Colombia\n ") == "inetum colombia"


def test_normalizar_nombre_empresa_vacio_d41() -> None:
    assert normalizar_nombre_empresa("") == ""
    assert normalizar_nombre_empresa("   ") == ""


def test_ruta_perfil_navegador_configurada_y_vacia() -> None:
    assert ruta_perfil_navegador({"profile_path": "data/browser_profile"}) == (
        "data/browser_profile"
    )
    assert ruta_perfil_navegador({"profile_path": "  "}) == ""
    assert ruta_perfil_navegador({}) == ""
    assert ruta_perfil_navegador(None) == ""


def test_ventana_navegador_valores_y_defectos() -> None:
    assert ventana_navegador({"ventana_ancho": 1600, "ventana_alto": 900}) == (1600, 900)
    assert ventana_navegador({}) == (1600, 900)
    assert ventana_navegador({"ventana_ancho": 0, "ventana_alto": -5}) == (1600, 900)
    assert ventana_navegador(None) == (1600, 900)


def test_espera_manual_navegador_valor_y_defecto() -> None:
    assert espera_manual_navegador({"espera_manual_segundos": 300}) == 300
    assert espera_manual_navegador({}) == 300
    assert espera_manual_navegador({"espera_manual_segundos": 0}) == 300
