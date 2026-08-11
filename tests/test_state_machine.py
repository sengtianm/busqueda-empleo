import pytest

from shared.errors import InternalError
from shared.models import OfferState
from shared.state_machine import possible_transitions, transition


def test_transition_discovered_to_prepared() -> None:
    result = transition(OfferState.DESCUBIERTA, OfferState.PREPARADA)
    assert result == OfferState.PREPARADA


def test_transition_prepared_to_evaluated() -> None:
    result = transition(OfferState.PREPARADA, OfferState.EVALUADA)
    assert result == OfferState.EVALUADA


def test_transition_evaluated_to_accepted() -> None:
    result = transition(OfferState.EVALUADA, OfferState.ACEPTADA)
    assert result == OfferState.ACEPTADA


def test_transition_evaluated_to_discarded() -> None:
    result = transition(OfferState.EVALUADA, OfferState.DESCARTADA)
    assert result == OfferState.DESCARTADA


def test_transition_accepted_to_processed() -> None:
    result = transition(OfferState.ACEPTADA, OfferState.PROCESADA)
    assert result == OfferState.PROCESADA


def test_transition_discarded_to_finalized() -> None:
    result = transition(OfferState.DESCARTADA, OfferState.FINALIZADA)
    assert result == OfferState.FINALIZADA


def test_transition_processed_to_finalized() -> None:
    result = transition(OfferState.PROCESADA, OfferState.FINALIZADA)
    assert result == OfferState.FINALIZADA


def test_invalid_transition() -> None:
    with pytest.raises(InternalError, match="ER-INT-010"):
        transition(OfferState.DESCUBIERTA, OfferState.FINALIZADA)


def test_possible_transitions_from_evaluated() -> None:
    destinations = possible_transitions(OfferState.EVALUADA)
    assert OfferState.ACEPTADA in destinations
    assert OfferState.DESCARTADA in destinations


def test_possible_transitions_from_finalized() -> None:
    destinations = possible_transitions(OfferState.FINALIZADA)
    assert destinations == []
