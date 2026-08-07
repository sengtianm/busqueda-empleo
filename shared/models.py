from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class OfferState(str, Enum):
    DISCOVERED = "discovered"
    PREPARED = "prepared"
    EVALUATED = "evaluated"
    ACCEPTED = "accepted"
    DISCARDED = "discarded"
    PROCESSED = "processed"
    FINALIZED = "finalized"


class EvaluationResult(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class DecisionEvaluation(str, Enum):
    CONTINUE = "continue"
    DISCARD = "discard"


class Source(BaseModel):
    id: str = ""
    nombre: str
    tipo: str = ""
    url_base: str = ""
    creation_date: str = ""
    last_edit_date: str = ""


class Company(BaseModel):
    id: str = ""
    nombre: str
    normalized_name: str = ""
    sitio_web: str = ""
    linkedin: str = ""
    sector: str = ""
    size: str = ""
    descripcion: str = ""
    creation_date: str = ""
    last_edit_date: str = ""


class Location(BaseModel):
    id: str = ""
    ciudad: str = ""
    region: str = ""
    pais: str = ""
    modalidad: str = ""
    creation_date: str = ""
    last_edit_date: str = ""


class Offer(BaseModel):
    id: str = ""
    fuente_id: str = ""
    empresa_id: str = ""
    ubicacion_id: str = ""
    source_identifier: str = ""
    url: str
    titulo: str
    descripcion_original: str
    fecha_publicacion: datetime | None = None
    discovery_date: datetime | None = None
    estado: OfferState = OfferState.DISCOVERED
    observaciones: str = ""
    creation_date: str = ""
    last_edit_date: str = ""
    run_id: str | None = None
    session_id: str | None = None
    set_indice: int | None = None
    id_externo_url: str | None = None


class GrupoCodigo(str, Enum):
    GRUPO_A = "grupo_a"
    GRUPO_B = "grupo_b"


class TipoEvento(str, Enum):
    ERROR = "error"
    SUCESO = "suceso"


class EstadoCorrida(str, Enum):
    EN_EJECUCION = "en_ejecucion"
    COMPLETADA = "completada"
    ERROR = "error"
    CONCURRENCIA = "concurrencia"


class Corrida(BaseModel):
    run_id: str
    timestamp_inicio: datetime | None = None
    estado: EstadoCorrida = EstadoCorrida.EN_EJECUCION


class EventoAlmacen(BaseModel):
    evento_id: str = ""
    run_id: str
    source_id: str = ""
    session_id: str | None = None
    set_indice: int | None = None
    timestamp: datetime | None = None
    tipo: TipoEvento
    codigo: str
    evidencia: str = ""
    offer_id: str | None = None


class AuditoriaSesion(BaseModel):
    session_id: str
    run_id: str
    source_id: str
    set_indice: int | None = None
    timestamp: datetime | None = None
    total_declarado: int | None = None
    conteo: int = 0
    estado: str = ""


class PoliticasCaptura(BaseModel):
    max_paginas: int = 5
    max_ofertas_por_corrida: int = 25
    pausa_entre_lotes_segundos: int = 10
    estrategia_anti_bloqueo: str = "pausa_aleatoria"


class FichaFuente(BaseModel):
    source_id: str
    nombre: str
    url: str = ""
    tipo_acceso: str = ""
    credenciales_referencia: list[str] = Field(default_factory=list)
    criterio_exito: str = ""
    timeout_segundos: int = 30


class SetFiltros(BaseModel):
    source_id: str
    indice: int
    filtros: list[dict[str, str | list[str]]] = Field(default_factory=list)


class EntryResult(BaseModel):
    estado: str = ""
    codigo_motivo: str = ""
    evidencia_acotada: str = ""
    numero_de_intentos: int = 0


class SearchResult(BaseModel):
    estado: str = ""
    codigo_motivo: str = ""
    evidencia_acotada: str = ""
    ofertas_primera_pagina: list[Offer] = Field(default_factory=list)
    estado_paginacion: str = ""
    total_declarado: int | None = None
    set_indice: int | None = None
    numero_de_intentos: int = 0


class CaptureBatch(BaseModel):
    ofertas: list[Offer] = Field(default_factory=list)
    run_id: str = ""
    source_id: str = ""
    session_id: str | None = None
    set_indice: int | None = None
    paginas_consumidas: int = 0


class EstadoCaptura(BaseModel):
    estado: str = ""
    codigo_motivo: str = ""
    paginas_consumidas: int = 0
    capturadas_acumuladas_fuente: int = 0
    limite_alcanzado: bool = False


class ProcessedOffer(BaseModel):
    id: str = ""
    offer_id: str = ""
    clean_title: str = ""
    clean_description: str = ""
    salario_min: float | None = None
    salario_max: float | None = None
    moneda: str = ""
    clean_location: str = ""
    modalidad: str = ""
    requisitos: list[str] = Field(default_factory=list)
    tecnologias: list[str] = Field(default_factory=list)
    idiomas: list[str] = Field(default_factory=list)
    experience_years: int | None = None
    processing_date: datetime | None = None
    creation_date: str = ""
    last_edit_date: str = ""


class Evaluation(BaseModel):
    id: str = ""
    processed_offer_id: str = ""
    resultado: EvaluationResult
    score: float
    approval_threshold: float = 50.0
    decision: DecisionEvaluation
    justification: str
    evaluated_criteria: str = ""
    evaluation_date: datetime | None = None
    version_modelo: str = "v1"
    creation_date: str = ""
    last_edit_date: str = ""


class EvaluacionDetallada(BaseModel):
    id: str = ""
    processed_offer_id: str = ""
    resultado_organizacional: str = ""
    problema_organizacional: str = ""
    perfil_profesional_requerido: str = ""
    coincidencias_perfil: str = ""
    logica_xyz: str = ""
    hipotesis_valor: str = ""
    informacion_descartada: str = ""
    ajuste_tecnico: float = 0.0
    justificacion_ajuste_tecnico: str = ""
    ajuste_funcional: float = 0.0
    justificacion_ajuste_funcional: str = ""
    ajuste_estrategico: float = 0.0
    justificacion_ajuste_estrategico: str = ""
    riesgo_sobrecalificacion: str = ""
    justificacion_riesgo: str = ""
    recomendacion_final: str = ""
    justificacion_recomendacion: str = ""
    insumos_carta_presentacion: str = ""
    evaluation_date: datetime | None = None
    version_metodologia: str = "v1"
    creation_date: str = ""
    last_edit_date: str = ""


class Profile(BaseModel):
    id: str = ""
    tecnologias: dict[str, int] = Field(default_factory=dict)
    experience_years: int = 0
    idiomas: dict[str, str] = Field(default_factory=dict)
    ubicaciones_preferidas: list[str] = Field(default_factory=list)
    modalidades_preferidas: list[str] = Field(default_factory=list)
    salario_minimo: float | None = None
    seniority: str = ""
    empresas_objetivo: list[str] = Field(default_factory=list)
    empresas_excluidas: list[str] = Field(default_factory=list)
    educacion_nivel: str = ""
