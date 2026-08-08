from collections.abc import Generator
from pathlib import Path

import pytest

from modules.discovery.run_context import RunContext
from shared.models import (
    CaptureBatch,
    Company,
    DecisionEvaluation,
    EntryResult,
    Evaluation,
    EvaluationResult,
    FichaFuente,
    Location,
    Offer,
    OfferState,
    PoliticasCaptura,
    ProcessedOffer,
    Profile,
    SearchResult,
    SetFiltros,
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


@pytest.fixture
def example_ficha_fuente() -> FichaFuente:
    return FichaFuente(
        source_id="linkedin",
        nombre="LinkedIn",
        url="https://www.linkedin.com/jobs/search",
        tipo_acceso="con_autenticacion",
        credenciales_referencia=["LINKEDIN_EMAIL", "LINKEDIN_PASSWORD"],
        criterio_exito="global-nav",
        timeout_segundos=30,
    )


@pytest.fixture
def example_set_filtros(example_ficha_fuente: FichaFuente) -> SetFiltros:
    return SetFiltros(
        source_id=example_ficha_fuente.source_id,
        indice=0,
        filtros=[
            {"tipo": "keywords", "valor": ["Data Engineer", "Analista de Datos"]},
            {"tipo": "ubicacion", "valor": "Madrid"},
            {"tipo": "modalidad", "valor": "remoto"},
        ],
    )


@pytest.fixture
def example_politicas_captura() -> PoliticasCaptura:
    return PoliticasCaptura(
        max_paginas=5,
        max_ofertas_por_corrida=25,
        pausa_entre_lotes_segundos=10,
        estrategia_anti_bloqueo="pausa_aleatoria",
    )


@pytest.fixture
def example_run_context() -> RunContext:
    config_fuentes = [
        {
            "source_id": "linkedin",
            "nombre": "LinkedIn",
            "ficha_acceso": {
                "url": "https://www.linkedin.com/jobs/search",
                "tipo_acceso": "con_autenticacion",
                "credenciales_referencia": ["LINKEDIN_EMAIL", "LINKEDIN_PASSWORD"],
                "criterio_exito": "global-nav",
                "timeout_segundos": 30,
            },
            "sets_de_filtros": [
                {
                    "set_indice": 0,
                    "filtros": [
                        {"tipo": "keywords", "valor": ["Data Engineer"]},
                    ],
                }
            ],
            "politicas_de_captura": {
                "max_paginas": 2,
                "max_ofertas_por_corrida": 10,
                "pausa_entre_lotes_segundos": 1,
                "estrategia_anti_bloqueo": "none",
            },
        }
    ]
    return RunContext(config_fuentes=config_fuentes, run_id="COR-0001")


@pytest.fixture
def example_entry_result() -> EntryResult:
    return EntryResult(estado="exito", evidencia_acotada="global-nav", numero_de_intentos=1)


@pytest.fixture
def example_entry_result_fallo() -> EntryResult:
    return EntryResult(
        estado="error",
        codigo_motivo="bloqueo_plataforma",
        evidencia_acotada="captcha",
    )


@pytest.fixture
def example_search_result() -> SearchResult:
    ofertas = [
        Offer(
            url="https://www.linkedin.com/jobs/view/12345",
            titulo="Data Engineer",
            descripcion_original="",
            fuente_id="linkedin",
            set_indice=0,
            id_externo_url="12345",
        ),
        Offer(
            url="https://www.linkedin.com/jobs/view/12346",
            titulo="Analista de Datos",
            descripcion_original="",
            fuente_id="linkedin",
            set_indice=0,
            id_externo_url="12346",
        ),
    ]
    return SearchResult(
        estado="ok",
        ofertas_primera_pagina=ofertas,
        estado_paginacion="hay_mas",
        total_declarado=42,
        set_indice=0,
        numero_de_intentos=1,
    )


@pytest.fixture
def example_capture_batch() -> CaptureBatch:
    ofertas = [
        Offer(
            url="https://www.linkedin.com/jobs/view/12345",
            titulo="Data Engineer",
            descripcion_original="Descripcion de prueba",
            fuente_id="linkedin",
            set_indice=0,
            id_externo_url="12345",
        )
    ]
    return CaptureBatch(
        ofertas=ofertas,
        run_id="COR-0001",
        source_id="linkedin",
        session_id="SES-0001",
        set_indice=0,
        paginas_consumidas=1,
    )
