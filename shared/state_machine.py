from shared.errors import ErrorInterno
from shared.models import OfferState

VALID_TRANSITIONS: dict[OfferState, list[OfferState]] = {
    OfferState.DISCOVERED: [OfferState.PREPARED],
    OfferState.PREPARED: [OfferState.EVALUATED],
    OfferState.EVALUATED: [OfferState.ACCEPTED, OfferState.DISCARDED],
    OfferState.ACCEPTED: [OfferState.PROCESSED],
    OfferState.DISCARDED: [OfferState.FINALIZED],
    OfferState.PROCESSED: [OfferState.FINALIZED],
}


def transition(
    current_state: OfferState,
    target_state: OfferState,
) -> OfferState:
    if (
        current_state in VALID_TRANSITIONS
        and target_state in VALID_TRANSITIONS[current_state]
    ):
        return target_state
    raise ErrorInterno(
        "010",
        f"Invalid transition: {current_state.value} -> {target_state.value}",
        source_module="state_machine",
    )


def possible_transitions(estado: OfferState) -> list[OfferState]:
    return VALID_TRANSITIONS.get(estado, [])
