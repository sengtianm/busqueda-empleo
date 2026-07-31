import pytest

from shared.errors import InternalError
from shared.models import OfferState
from shared.state_machine import possible_transitions, transition


def test_transition_discovered_to_prepared() -> None:
    result = transition(OfferState.DISCOVERED, OfferState.PREPARED)
    assert result == OfferState.PREPARED


def test_transition_prepared_to_evaluated() -> None:
    result = transition(OfferState.PREPARED, OfferState.EVALUATED)
    assert result == OfferState.EVALUATED


def test_transition_evaluated_to_accepted() -> None:
    result = transition(OfferState.EVALUATED, OfferState.ACCEPTED)
    assert result == OfferState.ACCEPTED


def test_transition_evaluated_to_discarded() -> None:
    result = transition(OfferState.EVALUATED, OfferState.DISCARDED)
    assert result == OfferState.DISCARDED


def test_transition_accepted_to_processed() -> None:
    result = transition(OfferState.ACCEPTED, OfferState.PROCESSED)
    assert result == OfferState.PROCESSED


def test_transition_discarded_to_finalized() -> None:
    result = transition(OfferState.DISCARDED, OfferState.FINALIZED)
    assert result == OfferState.FINALIZED


def test_transition_processed_to_finalized() -> None:
    result = transition(OfferState.PROCESSED, OfferState.FINALIZED)
    assert result == OfferState.FINALIZED


def test_invalid_transition() -> None:
    with pytest.raises(InternalError, match="ER-INT-010"):
        transition(OfferState.DISCOVERED, OfferState.FINALIZED)


def test_possible_transitions_from_evaluated() -> None:
    destinations = possible_transitions(OfferState.EVALUATED)
    assert OfferState.ACCEPTED in destinations
    assert OfferState.DISCARDED in destinations


def test_possible_transitions_from_finalized() -> None:
    destinations = possible_transitions(OfferState.FINALIZED)
    assert destinations == []
