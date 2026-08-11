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
        identificador_origen="12345",
        estado=OfferState.DESCUBIERTA,
    )


@pytest.fixture
def example_processed_offer(example_offer: Offer) -> ProcessedOffer:
    return ProcessedOffer(
        id="OFP-0001",
        id_oferta=example_offer.id,
        titulo_limpio="Data Engineer",
        tecnologias=["Python", "SQL", "Spark"],
        requisitos=["Experiencia en ETL"],
    )


@pytest.fixture
def example_evaluation(
    example_processed_offer: ProcessedOffer,
) -> Evaluation:
    return Evaluation(
        id="EVL-0001",
        id_oferta_procesada=example_processed_offer.id,
        resultado=EvaluationResult.HIGH,
        score=85.0,
        decision=DecisionEvaluation.CONTINUE,
        justificacion="Buena coincidencia con perfil",
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


@pytest.fixture
def example_ficha_fuente() -> FichaFuente:
    return FichaFuente(
        fuente_id="linkedin",
        nombre="LinkedIn",
        enlace="https://www.linkedin.com/jobs/search",
        tipo_acceso="con_autenticacion",
        credenciales_referencia=["LINKEDIN_EMAIL", "LINKEDIN_PASSWORD"],
        criterio_exito="global-nav",
        timeout_segundos=30,
    )


@pytest.fixture
def example_set_filtros(example_ficha_fuente: FichaFuente) -> SetFiltros:
    return SetFiltros(
        fuente_id=example_ficha_fuente.fuente_id,
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
            "fuente_id": "linkedin",
            "nombre": "LinkedIn",
            "ficha_acceso": {
                "enlace": "https://www.linkedin.com/jobs/search",
                "tipo_acceso": "con_autenticacion",
                "credenciales_referencia": ["LINKEDIN_EMAIL", "LINKEDIN_PASSWORD"],
                "criterio_exito": "global-nav",
                "timeout_segundos": 30,
            },
            "sets_de_filtros": [
                {
                    "indice_set": 0,
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
    return RunContext(config_fuentes=config_fuentes, id_corrida="COR-0001")


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
            enlace="https://www.linkedin.com/jobs/view/12345",
            titulo="Data Engineer",
            descripcion_original="",
            fuente_id="linkedin",
            indice_set=0,
            id_externo="12345",
        ),
        Offer(
            enlace="https://www.linkedin.com/jobs/view/12346",
            titulo="Analista de Datos",
            descripcion_original="",
            fuente_id="linkedin",
            indice_set=0,
            id_externo="12346",
        ),
    ]
    return SearchResult(
        estado="ok",
        ofertas_primera_pagina=ofertas,
        estado_paginacion="hay_mas",
        total_declarado=42,
        indice_set=0,
        numero_de_intentos=1,
    )


@pytest.fixture
def example_capture_batch() -> CaptureBatch:
    ofertas = [
        Offer(
            enlace="https://www.linkedin.com/jobs/view/12345",
            titulo="Data Engineer",
            descripcion_original="Descripcion de prueba",
            fuente_id="linkedin",
            indice_set=0,
            id_externo="12345",
        )
    ]
    return CaptureBatch(
        ofertas=ofertas,
        id_corrida="COR-0001",
        fuente_id="linkedin",
        id_sesion="SES-0001",
        indice_set=0,
        paginas_consumidas=1,
    )
