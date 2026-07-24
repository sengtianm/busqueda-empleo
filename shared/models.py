from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

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
    id: UUID = Field(default_factory=uuid4)
    nombre: str
    tipo: str = ""
    url_base: str = ""
    activa: bool = True


class Empresa(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    nombre: str
    nombre_normalizado: str = ""
    sitio_web: str = ""
    linkedin: str = ""
    sector: str = ""
    tamano: str = ""
    descripcion: str = ""


class Ubicacion(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    ciudad: str = ""
    region: str = ""
    pais: str = ""
    modalidad: str = ""


class Oferta(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    fuente_id: UUID
    empresa_id: UUID
    ubicacion_id: UUID | None = None
    identificador_fuente: str = ""
    url: str
    titulo: str
    descripcion_original: str
    fecha_publicacion: datetime | None = None
    fecha_descubrimiento: datetime = Field(default_factory=datetime.now)
    estado: EstadoOferta = EstadoOferta.DESCUBIERTA
    activa: bool = True
    observaciones: str = ""
    fecha_creacion: datetime = Field(default_factory=datetime.now)
    fecha_actualizacion: datetime = Field(default_factory=datetime.now)


class OfertaProcesada(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    oferta_id: UUID
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
    fecha_procesamiento: datetime = Field(default_factory=datetime.now)


class Evaluacion(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    oferta_procesada_id: UUID
    resultado: ResultadoEvaluacion
    puntaje: float
    umbral_aprobacion: float = 50.0
    decision: DecisionEvaluacion
    justificacion: str
    criterios_evaluados: str = ""
    fecha_evaluacion: datetime = Field(default_factory=datetime.now)
    version_modelo: str = "v1"


class ResultadoProcesamiento(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    oferta_procesada_id: UUID
    diagnostico: str = ""
    extraccion_estrategica: str = ""
    diseno_candidatura: str = ""
    borrador_carta: str = ""
    preparacion_entrevista: str = ""
    fecha_procesamiento: datetime = Field(default_factory=datetime.now)


class Perfil(BaseModel):
    id: UUID = Field(default_factory=uuid4)
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
