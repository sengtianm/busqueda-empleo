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


class ProcessingResult(BaseModel):
    id: str = ""
    processed_offer_id: str = ""
    diagnostic: str = ""
    strategic_extraction: str = ""
    application_design: str = ""
    cover_letter_draft: str = ""
    interview_preparation: str = ""
    processing_date: datetime | None = None
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
