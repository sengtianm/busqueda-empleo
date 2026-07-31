import pytest

from shared.errors import ErrorInterno
from shared.models import OfferState
from shared.state_machine import possible_transitions, transition


def test_transicion_descubierta_a_preparada() -> None:
    resultado = transition(OfferState.DISCOVERED, OfferState.PREPARED)
    assert resultado == OfferState.PREPARED


def test_transicion_preparada_a_evaluada() -> None:
    resultado = transition(OfferState.PREPARED, OfferState.EVALUATED)
    assert resultado == OfferState.EVALUATED


def test_transicion_evaluada_a_aceptada() -> None:
    resultado = transition(OfferState.EVALUATED, OfferState.ACCEPTED)
    assert resultado == OfferState.ACCEPTED


def test_transicion_evaluada_a_descarta() -> None:
    resultado = transition(OfferState.EVALUATED, OfferState.DISCARDED)
    assert resultado == OfferState.DISCARDED


def test_transicion_aceptada_a_procesada() -> None:
    resultado = transition(OfferState.ACCEPTED, OfferState.PROCESSED)
    assert resultado == OfferState.PROCESSED


def test_transicion_descarta_a_finalizada() -> None:
    resultado = transition(OfferState.DISCARDED, OfferState.FINALIZED)
    assert resultado == OfferState.FINALIZED


def test_transicion_procesada_a_finalizada() -> None:
    resultado = transition(OfferState.PROCESSED, OfferState.FINALIZED)
    assert resultado == OfferState.FINALIZED


def test_transicion_invalida() -> None:
    with pytest.raises(ErrorInterno, match="ER-INT-010"):
        transition(OfferState.DISCOVERED, OfferState.FINALIZED)


def test_transiciones_posibles_desde_evaluada() -> None:
    destinos = possible_transitions(OfferState.EVALUATED)
    assert OfferState.ACCEPTED in destinos
    assert OfferState.DISCARDED in destinos


def test_transiciones_posibles_desde_finalizada() -> None:
    destinos = possible_transitions(OfferState.FINALIZED)
    assert destinos == []
