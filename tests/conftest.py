from collections.abc import Generator
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
    Perfil,
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
def archivo_bd_temporal(tmp_path: Path) -> Generator[Path, None, None]:
    from shared.persistence import cambiar_ruta, inicializar_bd, restablecer_ruta

    ruta = tmp_path / "test.db"
    cambiar_ruta(ruta)
    inicializar_bd()
    yield ruta
    restablecer_ruta()


@pytest.fixture
def fuente_ejemplo() -> Fuente:
    return Fuente(
        id="FNT-0001",
        nombre="LinkedIn",
        tipo="red_social",
        url_base="https://www.linkedin.com",
    )


@pytest.fixture
def empresa_ejemplo() -> Empresa:
    return Empresa(
        id="EMP-0001",
        nombre="TechCorp",
        nombre_normalizado="techcorp",
        sector="tecnologia",
    )


@pytest.fixture
def ubicacion_ejemplo() -> Ubicacion:
    return Ubicacion(id="UBI-0001", ciudad="Madrid", region="Madrid", pais="Espana")


@pytest.fixture
def oferta_ejemplo(
    fuente_ejemplo: Fuente, empresa_ejemplo: Empresa, ubicacion_ejemplo: Ubicacion
) -> Oferta:
    return Oferta(
        id="OFE-0001",
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
        id="OFP-0001",
        oferta_id=oferta_ejemplo.id,
        titulo_limpio="Data Engineer",
        tecnologias=["Python", "SQL", "Spark"],
        requisitos=["Experiencia en ETL"],
    )


@pytest.fixture
def evaluacion_ejemplo(oferta_procesada_ejemplo: OfertaProcesada) -> Evaluacion:
    return Evaluacion(
        id="EVL-0001",
        oferta_procesada_id=oferta_procesada_ejemplo.id,
        resultado=ResultadoEvaluacion.ALTA,
        puntaje=85.0,
        decision=DecisionEvaluacion.CONTINUAR,
        justificacion="Buena coincidencia con perfil",
    )


@pytest.fixture
def perfil_ejemplo() -> Perfil:
    return Perfil(
        tecnologias={"Python": 5, "SQL": 4, "Spark": 3},
        experiencia_anios=8,
        seniority="senior",
        idiomas={"Ingles": "C1", "Espanol": "Nativo"},
        ubicaciones_preferidas=["Madrid", "Remoto"],
        modalidades_preferidas=["remoto", "hibrido"],
        salario_minimo=55000,
        empresas_objetivo=[],
        empresas_excluidas=["EvilCorp"],
        educacion_nivel="grado",
    )
