from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class EstadoOferta(str, Enum):
    DESCUBIERTA = "descubierta"
    PREPARADA = "preparada"
    EVALUADA = "evaluada"
    ACEPTADA = "aceptada"
    DESCARTA = "descartada"
    PROCESADA = "procesada"
    FINALIZADA = "finalizada"


class ResultadoEvaluacion(str, Enum):
    ALTA = "alta"
    MEDIA = "media"
    BAJA = "baja"


class DecisionEvaluacion(str, Enum):
    CONTINUAR = "continuar"
    DESCARTAR = "descartar"


class Fuente(BaseModel):
    id: str = ""
    nombre: str
    tipo: str = ""
    url_base: str = ""
    fecha_creacion: str = ""
    fecha_ultima_edicion: str = ""


class Empresa(BaseModel):
    id: str = ""
    nombre: str
    nombre_normalizado: str = ""
    sitio_web: str = ""
    linkedin: str = ""
    sector: str = ""
    tamano: str = ""
    descripcion: str = ""
    fecha_creacion: str = ""
    fecha_ultima_edicion: str = ""


class Ubicacion(BaseModel):
    id: str = ""
    ciudad: str = ""
    region: str = ""
    pais: str = ""
    modalidad: str = ""
    fecha_creacion: str = ""
    fecha_ultima_edicion: str = ""


class Oferta(BaseModel):
    id: str = ""
    fuente_id: str = ""
    empresa_id: str = ""
    ubicacion_id: str = ""
    identificador_fuente: str = ""
    url: str
    titulo: str
    descripcion_original: str
    fecha_publicacion: datetime | None = None
    fecha_descubrimiento: datetime | None = None
    estado: EstadoOferta = EstadoOferta.DESCUBIERTA
    observaciones: str = ""
    fecha_creacion: str = ""
    fecha_ultima_edicion: str = ""


class OfertaProcesada(BaseModel):
    id: str = ""
    oferta_id: str = ""
    titulo_limpio: str = ""
    descripcion_limpia: str = ""
    salario_min: float | None = None
    salario_max: float | None = None
    moneda: str = ""
    ubicacion_limpia: str = ""
    modalidad: str = ""
    requisitos: list[str] = Field(default_factory=list)
    tecnologias: list[str] = Field(default_factory=list)
    idiomas: list[str] = Field(default_factory=list)
    experiencia_anios: int | None = None
    fecha_procesamiento: datetime | None = None
    fecha_creacion: str = ""
    fecha_ultima_edicion: str = ""


class Evaluacion(BaseModel):
    id: str = ""
    oferta_procesada_id: str = ""
    resultado: ResultadoEvaluacion
    puntaje: float
    umbral_aprobacion: float = 50.0
    decision: DecisionEvaluacion
    justificacion: str
    criterios_evaluados: str = ""
    fecha_evaluacion: datetime | None = None
    version_modelo: str = "v1"
    fecha_creacion: str = ""
    fecha_ultima_edicion: str = ""


class ResultadoProcesamiento(BaseModel):
    id: str = ""
    oferta_procesada_id: str = ""
    diagnostico: str = ""
    extraccion_estrategica: str = ""
    diseno_candidatura: str = ""
    borrador_carta: str = ""
    preparacion_entrevista: str = ""
    fecha_procesamiento: datetime | None = None
    fecha_creacion: str = ""
    fecha_ultima_edicion: str = ""


class Perfil(BaseModel):
    id: str = ""
    tecnologias: dict[str, int] = Field(default_factory=dict)
    experiencia_anios: int = 0
    idiomas: dict[str, str] = Field(default_factory=dict)
    ubicaciones_preferidas: list[str] = Field(default_factory=list)
    modalidades_preferidas: list[str] = Field(default_factory=list)
    salario_minimo: float | None = None
    seniority: str = ""
    empresas_objetivo: list[str] = Field(default_factory=list)
    empresas_excluidas: list[str] = Field(default_factory=list)
    educacion_nivel: str = ""
