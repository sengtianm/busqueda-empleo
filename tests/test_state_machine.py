import pytest

from shared.errors import ErrorInterno
from shared.models import EstadoOferta
from shared.state_machine import transicionar, transiciones_posibles


def test_transicion_descubierta_a_preparada() -> None:
    resultado = transicionar(EstadoOferta.DESCUBIERTA, EstadoOferta.PREPARADA)
    assert resultado == EstadoOferta.PREPARADA


def test_transicion_preparada_a_evaluada() -> None:
    resultado = transicionar(EstadoOferta.PREPARADA, EstadoOferta.EVALUADA)
    assert resultado == EstadoOferta.EVALUADA


def test_transicion_evaluada_a_aceptada() -> None:
    resultado = transicionar(EstadoOferta.EVALUADA, EstadoOferta.ACEPTADA)
    assert resultado == EstadoOferta.ACEPTADA


def test_transicion_evaluada_a_descarta() -> None:
    resultado = transicionar(EstadoOferta.EVALUADA, EstadoOferta.DESCARTA)
    assert resultado == EstadoOferta.DESCARTA


def test_transicion_aceptada_a_procesada() -> None:
    resultado = transicionar(EstadoOferta.ACEPTADA, EstadoOferta.PROCESADA)
    assert resultado == EstadoOferta.PROCESADA


def test_transicion_descarta_a_finalizada() -> None:
    resultado = transicionar(EstadoOferta.DESCARTA, EstadoOferta.FINALIZADA)
    assert resultado == EstadoOferta.FINALIZADA


def test_transicion_procesada_a_finalizada() -> None:
    resultado = transicionar(EstadoOferta.PROCESADA, EstadoOferta.FINALIZADA)
    assert resultado == EstadoOferta.FINALIZADA


def test_transicion_invalida() -> None:
    with pytest.raises(ErrorInterno, match="ER-INT-010"):
        transicionar(EstadoOferta.DESCUBIERTA, EstadoOferta.FINALIZADA)


def test_transiciones_posibles_desde_evaluada() -> None:
    destinos = transiciones_posibles(EstadoOferta.EVALUADA)
    assert EstadoOferta.ACEPTADA in destinos
    assert EstadoOferta.DESCARTA in destinos


def test_transiciones_posibles_desde_finalizada() -> None:
    destinos = transiciones_posibles(EstadoOferta.FINALIZADA)
    assert destinos == []
