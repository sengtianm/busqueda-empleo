from shared.errors import ErrorInterno
from shared.models import EstadoOferta

TRANSICIONES_VALIDAS: dict[EstadoOferta, list[EstadoOferta]] = {
    EstadoOferta.DESCUBIERTA: [EstadoOferta.PREPARADA],
    EstadoOferta.PREPARADA: [EstadoOferta.EVALUADA],
    EstadoOferta.EVALUADA: [EstadoOferta.ACEPTADA, EstadoOferta.DESCARTA],
    EstadoOferta.ACEPTADA: [EstadoOferta.PROCESADA],
    EstadoOferta.DESCARTA: [EstadoOferta.FINALIZADA],
    EstadoOferta.PROCESADA: [EstadoOferta.FINALIZADA],
}


def transicionar(
    estado_actual: EstadoOferta,
    estado_destino: EstadoOferta,
) -> EstadoOferta:
    if (
        estado_actual in TRANSICIONES_VALIDAS
        and estado_destino in TRANSICIONES_VALIDAS[estado_actual]
    ):
        return estado_destino
    raise ErrorInterno(
        "010",
        f"Transicion invalida: {estado_actual.value} → {estado_destino.value}",
        modulo_origen="state_machine",
    )


def transiciones_posibles(estado: EstadoOferta) -> list[EstadoOferta]:
    return TRANSICIONES_VALIDAS.get(estado, [])
