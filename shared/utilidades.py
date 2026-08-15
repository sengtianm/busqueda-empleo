"""Helpers compartidos (catálogo español D7/D8): evidencia acotada y timestamps."""

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
