"""Execution context of a discovery run (nodo INICIO, DOC-04 Section 15).

RunContext is the single object passed between the thirteen nodes of the
official Discovery flow. It holds the validated configuration, the filtered
source list, the iterators (sources and filter sets), the run lock reference
and the result slots of each node. It is created by the INICIO node and does
not contain any node logic: nodes only read and update its fields.
"""

from datetime import datetime
from typing import Any

from shared.config import load
from shared.errors import ConfigurationError
from shared.models import (
    CaptureBatch,
    EntryResult,
    EstadoCaptura,
    FichaFuente,
    PoliticasCaptura,
    SearchResult,
    SetFiltros,
)
from shared.persistence import generate_id

_TIPOS_ACCESO = ("publico", "con_autenticacion")


def _ahora() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class RunContext:
    """Carries all the state a single discovery run needs across its nodes."""

    def __init__(
        self,
        config_fuentes: list[dict[str, Any]],
        config_captura: dict[str, Any] | None = None,
        run_id: str | None = None,
        permitir_vacio: bool = False,
    ) -> None:
        if not config_fuentes and not permitir_vacio:
            raise ConfigurationError(
                "12", "No sources defined in configuration.", source_module="run_context"
            )
        if config_captura is None:
            config_captura = load().get("captura", {})
        self.run_id = run_id or generate_id("corridas")
        self.timestamp_inicio: str = _ahora()
        self.fuentes_filtradas: list[FichaFuente] = []
        self._sets_validos: dict[str, list[SetFiltros]] = {}
        self._politicas_por_fuente: dict[str, PoliticasCaptura] = {}
        for conf in config_fuentes:
            ficha = self._construir_ficha(conf, config_captura)
            self.fuentes_filtradas.append(ficha)
        self.iterador_fuentes = -1
        self.iterador_sets: dict[str, int] = {
            f.source_id: -1 for f in self.fuentes_filtradas
        }
        self.bloqueo_adquirido = False
        self.session_id: str | None = None
        self.handle_sesion: Any | None = None
        self.entry_result: EntryResult | None = None
        self.search_result: SearchResult | None = None
        self.capture_batch: CaptureBatch | None = None
        self.estado_captura: EstadoCaptura | None = None
        self.paginas_consumidas = 0
        self.capturadas_acumuladas_fuente = 0
        self.limite_alcanzado = False

    def _construir_ficha(
        self, conf: dict[str, Any], config_captura: dict[str, Any]
    ) -> FichaFuente:
        if not isinstance(conf, dict):
            raise ConfigurationError(
                "12", "Malformed source entry (not a mapping).", source_module="run_context"
            )
        ficha_raw = conf.get("ficha_acceso")
        if not isinstance(ficha_raw, dict):
            raise ConfigurationError(
                "12",
                "Source without ficha_acceso (ERR-12, INICIO RN-08).",
                source_module="run_context",
            )
        try:
            ficha = FichaFuente(
                source_id=str(conf.get("source_id", "")),
                nombre=str(conf.get("nombre", "")),
                url=str(ficha_raw.get("url", "")),
                tipo_acceso=str(ficha_raw.get("tipo_acceso", "")),
                credenciales_referencia=[
                    str(c) for c in ficha_raw.get("credenciales_referencia", [])
                ],
                criterio_exito=str(ficha_raw.get("criterio_exito", "")),
                timeout_segundos=int(ficha_raw.get("timeout_segundos", 30)),
            )
        except (TypeError, ValueError) as exc:
            raise ConfigurationError(
                "12",
                f"Invalid access sheet fields ({exc}).",
                source_module="run_context",
            ) from exc
        if not ficha.source_id or not ficha.nombre or not ficha.url:
            raise ConfigurationError(
                "12",
                "Incomplete access sheet (ERR-12): "
                "source_id, nombre and url are mandatory.",
                source_module="run_context",
            )
        if not ficha.criterio_exito:
            raise ConfigurationError(
                "12",
                "Incomplete access sheet (ERR-12): criterio_exito is mandatory.",
                source_module="run_context",
            )
        if ficha.tipo_acceso not in _TIPOS_ACCESO:
            raise ConfigurationError(
                "12",
                f"Invalid tipo_acceso '{ficha.tipo_acceso}'",
                source_module="run_context",
            )
        if ficha.tipo_acceso == "con_autenticacion" and not ficha.credenciales_referencia:
            raise ConfigurationError(
                "12",
                "Authenticated source without credential references.",
                source_module="run_context",
            )
        sets = self._construir_sets(conf, ficha.source_id)
        self._sets_validos[ficha.source_id] = sets
        self._politicas_por_fuente[ficha.source_id] = self._construir_politicas(
            conf, config_captura
        )
        return ficha

    def _construir_sets(
        self, conf: dict[str, Any], source_id: str
    ) -> list[SetFiltros]:
        sets_raw = conf.get("sets_de_filtros")
        if not isinstance(sets_raw, list) or not sets_raw:
            return [SetFiltros(source_id=source_id, indice=0, filtros=[])]
        sets: list[SetFiltros] = []
        for item in sets_raw:
            if not isinstance(item, dict):
                continue
            indice = item.get("set_indice")
            filtros = item.get("filtros", [])
            if not isinstance(indice, int) or not isinstance(filtros, list):
                continue
            if any(f.source_id == source_id and f.indice == indice for f in sets):
                continue
            sets.append(
                SetFiltros(
                    source_id=source_id,
                    indice=indice,
                    filtros=[f for f in filtros if isinstance(f, dict)],
                )
            )
        sets.sort(key=lambda s: s.indice)
        return sets

    def _construir_politicas(
        self, conf: dict[str, Any], config_captura: dict[str, Any]
    ) -> PoliticasCaptura:
        politicas_raw = conf.get("politicas_de_captura")
        if not isinstance(politicas_raw, dict):
            return self._politicas_desde_global(config_captura)
        return PoliticasCaptura(
            max_paginas=int(
                politicas_raw.get(
                    "max_paginas", config_captura.get("max_paginas", 5)
                )
            ),
            max_ofertas_por_corrida=int(
                politicas_raw.get(
                    "max_ofertas_por_corrida",
                    config_captura.get("max_ofertas_por_corrida", 25),
                )
            ),
            pausa_entre_lotes_segundos=int(
                politicas_raw.get(
                    "pausa_entre_lotes_segundos",
                    config_captura.get("pausa_entre_lotes_segundos", 10),
                )
            ),
            estrategia_anti_bloqueo=str(
                politicas_raw.get(
                    "estrategia_anti_bloqueo",
                    config_captura.get("estrategia_anti_bloqueo", "pausa_aleatoria"),
                )
            ),
        )

    def _politicas_desde_global(
        self, config_captura: dict[str, Any]
    ) -> PoliticasCaptura:
        return PoliticasCaptura(
            max_paginas=int(config_captura.get("max_paginas", 5)),
            max_ofertas_por_corrida=int(
                config_captura.get("max_ofertas_por_corrida", 25)
            ),
            pausa_entre_lotes_segundos=int(
                config_captura.get("pausa_entre_lotes_segundos", 10)
            ),
            estrategia_anti_bloqueo=str(
                config_captura.get("estrategia_anti_bloqueo", "pausa_aleatoria")
            ),
        )

    def set_filtros(self, fuente: FichaFuente, indice: int = 0) -> SetFiltros | None:
        sets = self._sets_validos.get(fuente.source_id)
        if not sets:
            return None
        for s in sets:
            if s.indice == indice:
                return s
        return None

    def sets_validos(self, fuente: FichaFuente) -> list[SetFiltros]:
        return self._sets_validos.get(fuente.source_id, [])

    def politicas(self, fuente: FichaFuente) -> PoliticasCaptura:
        return self._politicas_por_fuente.get(
            fuente.source_id, PoliticasCaptura()
        )

    def reset_iteradores(self) -> None:
        self.iterador_fuentes = -1
        self.iterador_sets = {f.source_id: -1 for f in self.fuentes_filtradas}
        self.bloqueo_adquirido = False
        self.session_id = None
        self.handle_sesion = None
        self.entry_result = None
        self.search_result = None
        self.capture_batch = None
        self.estado_captura = None
        self.paginas_consumidas = 0
        self.capturadas_acumuladas_fuente = 0
        self.limite_alcanzado = False

    def seleccionar_siguiente_set(self, source_id: str) -> int:
        if source_id not in self.iterador_sets:
            raise ValueError(f"Unknown source in context: {source_id}")
        self.iterador_sets[source_id] += 1
        return self.iterador_sets[source_id]
