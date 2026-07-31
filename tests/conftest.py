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
def clear_config_cache() -> None:
    from shared.config import reload_config

    reload_config()


@pytest.fixture
def tests_dir() -> Path:
    return Path(__file__).resolve().parent


@pytest.fixture
def fixtures_dir(tests_dir: Path) -> Path:
    return tests_dir / "fixtures"


@pytest.fixture
def temp_db_file(tmp_path: Path) -> Generator[Path, None, None]:
    from shared.persistence import change_path, init_db, reset_path

    path = tmp_path / "test.db"
    change_path(path)
    init_db()
    yield path
    reset_path()


@pytest.fixture
def example_source() -> Source:
    return Source(
        id="FNT-0001",
        nombre="LinkedIn",
        tipo="red_social",
        url_base="https://www.linkedin.com",
    )


@pytest.fixture
def example_company() -> Company:
    return Company(
        id="EMP-0001",
        nombre="TechCorp",
        normalized_name="techcorp",
        sector="tecnologia",
    )


@pytest.fixture
def example_location() -> Location:
    return Location(id="UBI-0001", ciudad="Madrid", region="Madrid", pais="Espana")


@pytest.fixture
def example_offer(
    example_source: Source, example_company: Company, example_location: Location
) -> Offer:
    return Offer(
        id="OFE-0001",
        fuente_id=example_source.id,
        empresa_id=example_company.id,
        ubicacion_id=example_location.id,
        url="https://www.linkedin.com/jobs/view/12345",
        titulo="Data Engineer",
        descripcion_original="Descripcion de prueba",
        source_identifier="12345",
        estado=OfferState.DISCOVERED,
    )


@pytest.fixture
def example_processed_offer(example_offer: Offer) -> ProcessedOffer:
    return ProcessedOffer(
        id="OFP-0001",
        offer_id=example_offer.id,
        clean_title="Data Engineer",
        tecnologias=["Python", "SQL", "Spark"],
        requisitos=["Experiencia en ETL"],
    )


@pytest.fixture
def example_evaluation(
    example_processed_offer: ProcessedOffer,
) -> Evaluation:
    return Evaluation(
        id="EVL-0001",
        processed_offer_id=example_processed_offer.id,
        resultado=EvaluationResult.HIGH,
        score=85.0,
        decision=DecisionEvaluation.CONTINUE,
        justification="Buena coincidencia con perfil",
    )


@pytest.fixture
def example_profile() -> Profile:
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
