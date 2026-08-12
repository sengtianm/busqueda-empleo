import pytest

from modules.discovery.adapters.linkedin import FlowError, LinkedInAdapter
from modules.discovery.adapters.registry import (
    REGISTRO_ADAPTADORES,
    obtener_adaptador,
)


def test_registro_contiene_linkedin() -> None:
    assert "linkedin" in REGISTRO_ADAPTADORES
    assert REGISTRO_ADAPTADORES["linkedin"] is LinkedInAdapter


def test_obtener_adaptador_linkedin_devuelve_instancia() -> None:
    adaptador = obtener_adaptador("linkedin")
    assert isinstance(adaptador, LinkedInAdapter)


def test_obtener_adaptador_fuente_desconocida_falla_limpio() -> None:
    with pytest.raises(FlowError) as exc:
        obtener_adaptador("fuente_desconocida")
    assert exc.value.codigo_motivo == "fuente_no_soportada"
    assert "fuente_desconocida" in exc.value.mensaje


def test_obtener_adaptador_devuelve_instancia_nueva_cada_vez() -> None:
    assert obtener_adaptador("linkedin") is not obtener_adaptador("linkedin")
