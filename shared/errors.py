from datetime import datetime, timezone
from enum import IntEnum
from typing import Any


class Severidad(IntEnum):
    CRITICO = 1
    ALTO = 2
    MEDIO = 3
    BAJO = 4
    INFORMATIVO = 5


class BaseError(Exception):
    def __init__(
        self,
        codigo: str,
        mensaje: str,
        severidad: Severidad = Severidad.MEDIO,
        modulo_origen: str = "",
        oferta_id: str | None = None,
    ) -> None:
        self.codigo = codigo
        self.severidad = severidad
        self.modulo_origen = modulo_origen
        self.oferta_id = oferta_id
        self.timestamp = datetime.now(timezone.utc)
        super().__init__(mensaje)

    def __str__(self) -> str:
        base = f"[{self.codigo}] SV-{self.severidad.value} | {super().__str__()}"
        if self.modulo_origen:
            base += f" | módulo: {self.modulo_origen}"
        if self.oferta_id:
            base += f" | oferta: {self.oferta_id}"
        return base

    def to_dict(self) -> dict[str, Any]:
        return {
            "codigo": self.codigo,
            "mensaje": super().__str__(),
            "severidad": self.severidad.name,
            "modulo_origen": self.modulo_origen,
            "oferta_id": self.oferta_id,
            "timestamp": self.timestamp.isoformat(),
        }


class ErrorRed(BaseError):
    def __init__(self, codigo: str, mensaje: str, **kwargs: Any) -> None:
        super().__init__(f"ER-RED-{codigo}", mensaje, **kwargs)


class ErrorNavegador(BaseError):
    def __init__(self, codigo: str, mensaje: str, **kwargs: Any) -> None:
        super().__init__(f"ER-NAV-{codigo}", mensaje, **kwargs)


class ErrorExtraccion(BaseError):
    def __init__(self, codigo: str, mensaje: str, **kwargs: Any) -> None:
        super().__init__(f"ER-EXT-{codigo}", mensaje, **kwargs)


class ErrorValidacion(BaseError):
    def __init__(self, codigo: str, mensaje: str, **kwargs: Any) -> None:
        super().__init__(f"ER-VAL-{codigo}", mensaje, **kwargs)


class ErrorLLM(BaseError):
    def __init__(self, codigo: str, mensaje: str, **kwargs: Any) -> None:
        super().__init__(f"ER-LLM-{codigo}", mensaje, **kwargs)


class ErrorDatos(BaseError):
    def __init__(self, codigo: str, mensaje: str, **kwargs: Any) -> None:
        super().__init__(f"ER-DAT-{codigo}", mensaje, **kwargs)


class ErrorPersistencia(BaseError):
    def __init__(self, codigo: str, mensaje: str, **kwargs: Any) -> None:
        super().__init__(f"ER-DB-{codigo}", mensaje, **kwargs)


class ErrorConfiguracion(BaseError):
    def __init__(self, codigo: str, mensaje: str, **kwargs: Any) -> None:
        super().__init__(f"ER-CFG-{codigo}", mensaje, **kwargs)


class ErrorInterno(BaseError):
    def __init__(self, codigo: str, mensaje: str, **kwargs: Any) -> None:
        super().__init__(f"ER-INT-{codigo}", mensaje, **kwargs)


class ErrorExterno(BaseError):
    def __init__(self, codigo: str, mensaje: str, **kwargs: Any) -> None:
        super().__init__(f"ER-EXTS-{codigo}", mensaje, **kwargs)
