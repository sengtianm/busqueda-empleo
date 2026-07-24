from pathlib import Path

import pytest

from shared.models import (
    DecisionEvaluacion,
    Empresa,
    EstadoOferta,
    Evaluacion,
    Fuente,
    Oferta,
    OfertaProcesada,
    ResultadoEvaluacion,
    Ubicacion,
)


@pytest.fixture(autouse=True)
def limpiar_cache_config() -> None:
    from shared.config import recargar

    recargar()


@pytest.fixture
def ruta_tests() -> Path:
    return Path(__file__).resolve().parent


@pytest.fixture
def ruta_fixtures(ruta_tests: Path) -> Path:
    return ruta_tests / "fixtures"


@pytest.fixture
def archivo_xlsx_temporal(tmp_path: Path) -> Path:
    return tmp_path / "test.xlsx"


@pytest.fixture
def fuente_ejemplo() -> Fuente:
    return Fuente(
        nombre="LinkedIn",
        tipo="red_social",
        url_base="https://www.linkedin.com",
    )


@pytest.fixture
def empresa_ejemplo() -> Empresa:
    return Empresa(
        nombre="TechCorp",
        nombre_normalizado="techcorp",
        sector="tecnologia",
    )


@pytest.fixture
def ubicacion_ejemplo() -> Ubicacion:
    return Ubicacion(ciudad="Madrid", region="Madrid", pais="Espana")


@pytest.fixture
def oferta_ejemplo(
    fuente_ejemplo: Fuente, empresa_ejemplo: Empresa, ubicacion_ejemplo: Ubicacion
) -> Oferta:
    return Oferta(
        fuente_id=fuente_ejemplo.id,
        empresa_id=empresa_ejemplo.id,
        ubicacion_id=ubicacion_ejemplo.id,
        url="https://www.linkedin.com/jobs/view/12345",
        titulo="Data Engineer",
        descripcion_original="Descripcion de prueba",
        identificador_fuente="12345",
        estado=EstadoOferta.DESCUBIERTA,
    )


@pytest.fixture
def oferta_procesada_ejemplo(oferta_ejemplo: Oferta) -> OfertaProcesada:
    return OfertaProcesada(
        oferta_id=oferta_ejemplo.id,
        titulo_limpio="Data Engineer",
        tecnologias=["Python", "SQL", "Spark"],
        requisitos=["Experiencia en ETL"],
    )


@pytest.fixture
def evaluacion_ejemplo(oferta_procesada_ejemplo: OfertaProcesada) -> Evaluacion:
    return Evaluacion(
        oferta_procesada_id=oferta_procesada_ejemplo.id,
        resultado=ResultadoEvaluacion.ALTA,
        puntaje=85.0,
        decision=DecisionEvaluacion.CONTINUAR,
        justificacion="Buena coincidencia con perfil",
    )
