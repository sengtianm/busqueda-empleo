from collections.abc import Generator
from pathlib import Path

import pytest

from shared.models import (
    Company,
    DecisionEvaluation,
    Evaluation,
    EvaluationResult,
    Location,
    Offer,
    OfferState,
    ProcessedOffer,
    Profile,
    Source,
)


@pytest.fixture(autouse=True)
def limpiar_cache_config() -> None:
    from shared.config import reload_config

    reload_config()


@pytest.fixture
def ruta_tests() -> Path:
    return Path(__file__).resolve().parent


@pytest.fixture
def ruta_fixtures(ruta_tests: Path) -> Path:
    return ruta_tests / "fixtures"


@pytest.fixture
def archivo_bd_temporal(tmp_path: Path) -> Generator[Path, None, None]:
    from shared.persistence import change_path, init_db, reset_path

    ruta = tmp_path / "test.db"
    change_path(ruta)
    init_db()
    yield ruta
    reset_path()


@pytest.fixture
def fuente_ejemplo() -> Source:
    return Source(
        id="FNT-0001",
        nombre="LinkedIn",
        tipo="red_social",
        url_base="https://www.linkedin.com",
    )


@pytest.fixture
def empresa_ejemplo() -> Company:
    return Company(
        id="EMP-0001",
        nombre="TechCorp",
        normalized_name="techcorp",
        sector="tecnologia",
    )


@pytest.fixture
def ubicacion_ejemplo() -> Location:
    return Location(id="UBI-0001", ciudad="Madrid", region="Madrid", pais="Espana")


@pytest.fixture
def oferta_ejemplo(
    fuente_ejemplo: Source, empresa_ejemplo: Company, ubicacion_ejemplo: Location
) -> Offer:
    return Offer(
        id="OFE-0001",
        fuente_id=fuente_ejemplo.id,
        empresa_id=empresa_ejemplo.id,
        ubicacion_id=ubicacion_ejemplo.id,
        url="https://www.linkedin.com/jobs/view/12345",
        titulo="Data Engineer",
        descripcion_original="Descripcion de prueba",
        source_identifier="12345",
        estado=OfferState.DISCOVERED,
    )


@pytest.fixture
def oferta_procesada_ejemplo(oferta_ejemplo: Offer) -> ProcessedOffer:
    return ProcessedOffer(
        id="OFP-0001",
        offer_id=oferta_ejemplo.id,
        clean_title="Data Engineer",
        tecnologias=["Python", "SQL", "Spark"],
        requisitos=["Experiencia en ETL"],
    )


@pytest.fixture
def evaluacion_ejemplo(oferta_procesada_ejemplo: ProcessedOffer) -> Evaluation:
    return Evaluation(
        id="EVL-0001",
        processed_offer_id=oferta_procesada_ejemplo.id,
        resultado=EvaluationResult.HIGH,
        score=85.0,
        decision=DecisionEvaluation.CONTINUE,
        justification="Buena coincidencia con perfil",
    )


@pytest.fixture
def perfil_ejemplo() -> Profile:
    return Profile(
        tecnologias={"Python": 5, "SQL": 4, "Spark": 3},
        experience_years=8,
        seniority="senior",
        idiomas={"Ingles": "C1", "Espanol": "Nativo"},
        ubicaciones_preferidas=["Madrid", "Remoto"],
        modalidades_preferidas=["remoto", "hibrido"],
        salario_minimo=55000,
        empresas_objetivo=[],
        empresas_excluidas=["EvilCorp"],
        educacion_nivel="grado",
    )
