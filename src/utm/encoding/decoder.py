"""Decodes the string <M> (and <M>#w) back into a TuringMachine."""

# IMPORTS
from utm.core.errors import DecodingError
from utm.core.machine import TuringMachine
from utm.core.symbols import Direction
from utm.core.transition import Transition
from utm.encoding.scheme import FIELD_SEP, SECTION_COUNT, SECTION_SEP, TRANSITION_SEP

TRANSITION_FIELD_COUNT = 5


def decode_machine(encoded: str) -> TuringMachine:
    """Turns <M> back into a TuringMachine.

    Raises DecodingError if the string is not well-formed. If the fields
    are well-formed but don't form a valid machine (e.g. start state not
    in the set of states), TuringMachine.create raises MachineDefinitionError.
    """
    sections = encoded.split(SECTION_SEP)
    if len(sections) != SECTION_COUNT:
        raise DecodingError(f"expected {SECTION_COUNT} sections, got {len(sections)}")

    states_s, input_s, tape_s, transitions_s, start, accept, reject = sections
    transitions = [
        _decode_transition(raw, index)
        for index, raw in enumerate(_split(transitions_s, TRANSITION_SEP))
    ]
    return TuringMachine.create(
        states=_split(states_s, FIELD_SEP),
        input_alphabet=_split(input_s, FIELD_SEP),
        tape_alphabet=_split(tape_s, FIELD_SEP),
        transitions=transitions,
        start_state=start,
        accept_state=accept,
        reject_state=reject,
    )


def decode_instance(encoded: str) -> tuple[TuringMachine, str]:
    """Splits <M>#w into (M, w)."""
    sections = encoded.split(SECTION_SEP)
    if len(sections) != SECTION_COUNT + 1:
        raise DecodingError(f"expected <M>#w, got {len(sections)} sections")
    machine_part = SECTION_SEP.join(sections[:SECTION_COUNT])
    input_string = sections[SECTION_COUNT]
    return decode_machine(machine_part), input_string


def _split(section: str, sep: str) -> list[str]:
    return section.split(sep) if section else []


def _decode_transition(raw: str, index: int) -> Transition:
    fields = raw.split(FIELD_SEP)
    if len(fields) != TRANSITION_FIELD_COUNT:
        raise DecodingError(f"transition must have {TRANSITION_FIELD_COUNT} fields", position=index)

    state, read, next_state, write, move = fields
    try:
        direction = Direction(move)
    except ValueError:
        raise DecodingError(f"unknown direction {move!r}", position=index) from None

    return Transition(state, read, next_state, write, direction)
