"""Helpers compartidos (catálogo español D7/D8): evidencia acotada, timestamps y normalización."""

import unicodedata
from datetime import datetime

FORMATO_TIMESTAMP = "%Y-%m-%d %H:%M:%S"

TIPOS_ACCESO = ("publico", "con_autenticacion")

_SUFIJO_TRUNCAMIENTO = "..."


def acotar_evidencia(texto: str, maximo: int = 300) -> str:
    """Truncates long evidence texts keeping the DB `evidencia` bounded."""
    if len(texto) <= maximo:
        return texto
    return texto[:maximo] + _SUFIJO_TRUNCAMIENTO


def ahora() -> str:
    """Timestamp canónico de corrida (misma marca para BD, eventos y contexto)."""
    return datetime.now().strftime(FORMATO_TIMESTAMP)


def normalizar_texto(texto: str) -> str:
    """Normaliza texto para dedup (D33): minúsculas, sin acentos,
    sin puntuación, espacios simples.

    Usada por el Módulo 2 para la tupla de ubicación y los títulos de la
    verificación de duplicidad. Texto vacío devuelve cadena vacía (el
    llamador aplica la regla D31).
    """
    if not texto:
        return ""
    sin_acentos = "".join(
        caracter
        for caracter in unicodedata.normalize("NFD", texto.lower())
        if unicodedata.category(caracter) != "Mn"
    )
    sin_puntuacion = "".join(
        caracter if caracter.isalnum() else " " for caracter in sin_acentos
    )
    return " ".join(sin_puntuacion.split())


def normalizar_nombre_empresa(texto: str) -> str:
    """Clave del catálogo `empresas.nombre_normalizado` (D41): minúsculas y
    espacios múltiples colapsados; conserva TODOS los caracteres (tildes,
    ñ, puntuación, símbolos como `&`, `.`, paréntesis).

    Sustituye a `normalizar_texto` solo para nombres de empresa — ubicaciones
    y títulos de duplicidad mantienen la regla estricta. Texto vacío
    devuelve cadena vacía (el llamador aplica la regla D31).
    """
    if not texto:
        return ""
    return " ".join(texto.lower().split())
