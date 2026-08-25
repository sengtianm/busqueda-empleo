from collections.abc import Generator
from pathlib import Path

import pytest

from shared.models import (
    Company,
    Location,
    Offer,
    OfferState,
    Profile,
    Source,
)


@pytest.fixture(autouse=True)
def clear_config_cache() -> None:
    from shared.config import reload_config

    reload_config()


@pytest.fixture(autouse=True)
def base_datos_aislada(tmp_path: Path) -> Generator[None, None, None]:
    """Aislamiento global de datos (2026-08-25): toda prueba opera sobre
    una BD SQLite temporal; ninguna escritura alcanza la BD real del
    proyecto (contaminación detectada tras correr la suite completa)."""
    from shared.persistence import change_path, init_db, reset_path

    change_path(tmp_path / "test_aislado.db")
    init_db()
    yield
    reset_path()


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
        id="LI-01",
        nombre="LinkedIn",
        tipo="red_social",
        enlace_base="https://www.linkedin.com",
    )


@pytest.fixture
def example_company() -> Company:
    return Company(
        id="EMP-0001",
        nombre="TechCorp",
        nombre_normalizado="techcorp",
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
        enlace="https://www.linkedin.com/jobs/view/12345",
        titulo="Data Engineer",
        descripcion_original="Descripcion de prueba",
        estado=OfferState.DESCUBIERTA,
    )


@pytest.fixture
def example_profile() -> Profile:
    return Profile(
        tecnologias={"Python": 5, "SQL": 4, "Spark": 3},
        anos_experiencia=8,
        seniority="senior",
        idiomas={"Ingles": "C1", "Espanol": "Nativo"},
        ubicaciones_preferidas=["Madrid", "Remoto"],
        modalidades_preferidas=["remoto", "hibrido"],
        salario_minimo=55000,
        empresas_objetivo=[],
        empresas_excluidas=["EvilCorp"],
        educacion_nivel="grado",
    )
