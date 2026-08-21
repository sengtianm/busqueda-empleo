"""¿Quedan ofertas en 'descubierta'? node of the Preparation flow (ficha M2
v1.0).

The module's only decision with I/O (RN-05): it queries the database because
each loop pass must observe the real remaining state. Condition (VAL-03):
`pendientes > 0 y pasadas_actuales < max_pasadas` where `pasadas_actuales =
contexto.pasadas + 1` counts the pass that just finished.

Branches: Sí → control back to Preparación with `pasadas` incremented (the
upcoming pass). No → the `revision_pendientes` event (pasadas, pendientes)
is ALWAYS written before handing control to "Finalizar Proceso" (VAL-04) —
both for the no-loop close (`pasadas=1, pendientes=0`) and for the exhausted
`max_pasadas` close (RN-03: leftovers stay `descubierta` for the next run).

Approved interpretation note P2 (sub-phase 5.4): when INICIO loads zero
candidates the flow short-circuits to Finalizar Proceso with the
`sin_pendientes` motive and this node never executes — so this node writes
`revision_pendientes` only when it actually runs.
"""

from dataclasses import dataclass

from loguru import logger

from modules.preparation.nodes.preparacion import FalloPreparacion
from modules.preparation.nodes.verificacion import registrar_evento
from modules.preparation.run_context import RunContext
from shared.persistence import contar_filas
from shared.retry import ejecutar_con_reintento


@dataclass
class ResultadoDecisionBucle:
    """Outcome handed to the flow: `continuar` (another pass) or `finalizar`;
    `abortada` on ERR-01."""

    estado: str
    contexto: RunContext | None = None
    codigo: str = ""
    descripcion: str = ""
    pendientes: int = 0
    pasadas: int = 0


def _contar_descubierta(contexto: RunContext) -> int:
    """ERR-01: the count retries via the shared helper; exhaustion raises."""

    def _contar() -> int:
        try:
            return contar_filas("ofertas_descubiertas", {"estado": "descubierta"})
        except Exception as exc:
            # Generic SQLite failures become flow-code failures so the shared
            # helper actually retries them (ERR-01).
            raise FalloPreparacion("error_bd", str(exc)) from exc

    def _fallo(exc: BaseException, intentos: int) -> int:
        raise FalloPreparacion("error_bd", f"{exc} tras {intentos} intentos") from exc

    reintentos = contexto.config_preparacion["retries"]
    resultado, _ = ejecutar_con_reintento(
        _contar,
        al_fallo_final=_fallo,
        max_attempts=int(reintentos["max_attempts"]),
        base_wait=float(reintentos["base_wait_seconds"]),
        multiplier=float(reintentos["multiplier"]),
        max_wait=float(reintentos["max_wait_seconds"]),
        contexto_log=contexto.id_corrida,
    )
    return resultado


def _validar_contexto(contexto: RunContext) -> str | None:
    """VAL-01: coherent `max_pasadas` (positive integer) in configuration.
    None → valid."""
    valor = contexto.config_preparacion.get("max_pasadas")
    if isinstance(valor, bool) or not isinstance(valor, int) or valor < 1:
        return "max_pasadas ausente o invalido"
    if contexto.pasadas < 0 or contexto.pasadas > valor:
        return f"contador de pasadas incoherente: {contexto.pasadas}"
    return None


def _abortar(
    contexto: RunContext, codigo: str, descripcion: str
) -> ResultadoDecisionBucle:
    registrar_evento(contexto.id_corrida, "error", codigo, descripcion, "N/A")
    logger.error(f"{codigo} | {contexto.id_corrida} | {descripcion}")
    return ResultadoDecisionBucle(
        estado="abortada", contexto=contexto, codigo=codigo, descripcion=descripcion
    )


def ejecutar_decision_bucle(contexto: RunContext | None) -> ResultadoDecisionBucle:
    """Run the ¿Quedan ofertas en 'descubierta'? decision (sheet pasos 1-4)."""
    if contexto is None or not isinstance(contexto, RunContext):
        logger.error(
            "ERR-01 | sin id_corrida | contexto ausente o corrupto: "
            "no se puede evaluar el bucle"
        )
        return ResultadoDecisionBucle(
            estado="abortada",
            codigo="ERR-01",
            descripcion="contexto ausente o corrupto",
        )
    id_corrida = contexto.id_corrida

    problema = _validar_contexto(contexto)
    if problema is not None:
        return _abortar(contexto, "ERR-01", f"contexto invalido: {problema}")

    # Paso 1 — query the pending count (ERR-01 retries; abort on exhaust).
    try:
        pendientes = _contar_descubierta(contexto)
    except FalloPreparacion as error:
        return _abortar(contexto, "ERR-01", f"fallo de bd en conteo: {error.detalle}")
    if pendientes < 0:
        return _abortar(contexto, "ERR-01", f"conteo negativo: {pendientes}")

    max_pasadas = int(contexto.config_preparacion["max_pasadas"])
    pasadas_actuales = contexto.pasadas + 1

    # Pasos 2-3 — rama Sí: another pass; hand control with pasadas incremented.
    if pendientes > 0 and pasadas_actuales < max_pasadas:
        contexto.pasadas = pasadas_actuales
        logger.info(
            f"BUCLE CONTINUA | run={id_corrida} | pasadas={pasadas_actuales} "
            f"pendientes={pendientes}"
        )
        return ResultadoDecisionBucle(
            estado="continuar",
            contexto=contexto,
            pendientes=pendientes,
            pasadas=pasadas_actuales,
        )

    # Paso 4 — rama No: write revision_pendientes BEFORE handing control
    # (VAL-04), covering both the no-loop close and the max_pasadas close.
    texto_evento = (
        f"pasadas={pasadas_actuales} pendientes={pendientes} para la próxima corrida"
        if pendientes
        else f"pasadas={pasadas_actuales} pendientes=0"
    )
    registrar_evento(id_corrida, "suceso", "revision_pendientes", texto_evento, "N/A")
    logger.info(
        f"BUCLE CERRADO | run={id_corrida} | pasadas={pasadas_actuales} "
        f"pendientes={pendientes}"
    )
    return ResultadoDecisionBucle(
        estado="finalizar",
        contexto=contexto,
        pendientes=pendientes,
        pasadas=pasadas_actuales,
    )
