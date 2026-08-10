"""Truncation helper for error evidence texts (DOC-06, DOC-13A)."""

_SUFIJO_TRUNCAMIENTO = "..."


def acotar_evidencia(texto: str, maximo: int = 300) -> str:
    """Truncates long evidence texts keeping the DB `evidencia` bounded."""
    if len(texto) <= maximo:
        return texto
    return texto[:maximo] + _SUFIJO_TRUNCAMIENTO
