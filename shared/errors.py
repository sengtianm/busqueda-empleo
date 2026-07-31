from datetime import datetime, timezone
from enum import IntEnum
from typing import Any


class Severity(IntEnum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    INFORMATIVE = 5


class BaseError(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        severity: Severity = Severity.MEDIUM,
        source_module: str = "",
        offer_id: str | None = None,
    ) -> None:
        self.code = code
        self.severity = severity
        self.source_module = source_module
        self.offer_id = offer_id
        self.timestamp = datetime.now(timezone.utc)
        super().__init__(message)

    def __str__(self) -> str:
        base = f"[{self.code}] SV-{self.severity.value} | {super().__str__()}"
        if self.source_module:
            base += f" | module: {self.source_module}"
        if self.offer_id:
            base += f" | offer: {self.offer_id}"
        return base

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "message": super().__str__(),
            "severity": self.severity.name,
            "source_module": self.source_module,
            "offer_id": self.offer_id,
            "timestamp": self.timestamp.isoformat(),
        }


class NetworkError(BaseError):
    def __init__(self, code: str, message: str, **kwargs: Any) -> None:
        super().__init__(f"ER-RED-{code}", message, **kwargs)


class BrowserError(BaseError):
    def __init__(self, code: str, message: str, **kwargs: Any) -> None:
        super().__init__(f"ER-NAV-{code}", message, **kwargs)


class ExtractionError(BaseError):
    def __init__(self, code: str, message: str, **kwargs: Any) -> None:
        super().__init__(f"ER-EXT-{code}", message, **kwargs)


class ValidationError(BaseError):
    def __init__(self, code: str, message: str, **kwargs: Any) -> None:
        super().__init__(f"ER-VAL-{code}", message, **kwargs)


class LLMError(BaseError):
    def __init__(self, code: str, message: str, **kwargs: Any) -> None:
        super().__init__(f"ER-LLM-{code}", message, **kwargs)


class DataError(BaseError):
    def __init__(self, code: str, message: str, **kwargs: Any) -> None:
        super().__init__(f"ER-DAT-{code}", message, **kwargs)


class PersistenceError(BaseError):
    def __init__(self, code: str, message: str, **kwargs: Any) -> None:
        super().__init__(f"ER-DB-{code}", message, **kwargs)


class ConfigurationError(BaseError):
    def __init__(self, code: str, message: str, **kwargs: Any) -> None:
        super().__init__(f"ER-CFG-{code}", message, **kwargs)


class InternalError(BaseError):
    def __init__(self, code: str, message: str, **kwargs: Any) -> None:
        super().__init__(f"ER-INT-{code}", message, **kwargs)


class ExternalError(BaseError):
    def __init__(self, code: str, message: str, **kwargs: Any) -> None:
        super().__init__(f"ER-EXTS-{code}", message, **kwargs)
