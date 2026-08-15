"""Nodes for recording events and errors in the discovery flow.
(RN-01: Generic node for any 'No' branch of a decision)
"""

from dataclasses import dataclass

from loguru import logger

from modules.discovery.run_context import RunContext
from shared.models import EntryResult, SearchResult, TipoEvento
from shared.persistence import escribir_evento_seguro
from shared.utilidades import ahora


@dataclass
class ResultadoRegistro:
    estado: str  # "ok"
    contexto: RunContext | None
    codigo: str = ""
    descripcion: str = ""


def registrar_evento(contexto: RunContext) -> ResultadoRegistro:
    """
    Determines which result to read (search or entry), typifies it,
    and writes it to the events table.
    """
    resultado: SearchResult | EntryResult | None = None
    indice_set: int | None = None

    # 1. Determine result to read, scoped to the current source (RN-09):
    #    a search_result only belongs to the run segment of its own source.
    set_actual = contexto.set_corriente
    fuente = contexto.fuente_corriente
    search_de_fuente = (
        contexto.search_result is not None
        and set_actual is not None
        and fuente is not None
        and set_actual.fuente_id == fuente.fuente_id
    )
    if search_de_fuente:
        search_resultado = contexto.search_result
        assert search_resultado is not None
        resultado = search_resultado
        indice_set = search_resultado.indice_set
    elif contexto.entry_result is not None:
        resultado = contexto.entry_result
    if resultado is None or isinstance(resultado, SearchResult) and indice_set is None:
        logger.warning(f"[{contexto.id_corrida}] Result without context data to register.")
        return ResultadoRegistro(estado="ok", contexto=contexto)

    # 2. Typify with the official enum (DOC-05 CNP-014)
    tipo = TipoEvento.ERROR if resultado.estado == "fallo" else TipoEvento.SUCESO

    # 3. Write to events table (non-aborting: RN-04 continue on failure)
    evidencia = (
        f"{resultado.evidencia_acotada} | "
        f"intentos: {resultado.numero_de_intentos}"
    )
    escribir_evento_seguro(
        {
            "id_corrida": contexto.id_corrida,
            "fuente_id": (
                contexto.fuente_corriente.fuente_id
                if contexto.fuente_corriente
                else ""
            ),
            "id_sesion": contexto.id_sesion,
            "indice_set": indice_set,
            "marca_temporal": ahora(),
            "tipo": tipo.value,
            "codigo": resultado.codigo_motivo,
            "evidencia": evidencia,
        },
        contexto_log=contexto.id_corrida,
    )

    return ResultadoRegistro(estado="ok", contexto=contexto)
