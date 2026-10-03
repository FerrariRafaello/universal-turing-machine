"""Encodes a TuringMachine as the string <M> described in scheme.py."""

# IMPORTS
from utm.core.errors import EncodingError
from utm.core.machine import TuringMachine
from utm.core.transition import Transition
from utm.encoding.scheme import FIELD_SEP, SECTION_SEP, TRANSITION_SEP, is_valid_name


def encode_machine(machine: TuringMachine) -> str:
    """Turns a TuringMachine into its string encoding <M>."""
    _check_names(machine)
    transitions = sorted(machine.transitions.values(), key=lambda t: t.key)
    sections = [
        FIELD_SEP.join(sorted(machine.states)),
        FIELD_SEP.join(sorted(machine.input_alphabet)),
        FIELD_SEP.join(sorted(machine.tape_alphabet)),
        TRANSITION_SEP.join(_encode_transition(t) for t in transitions),
        machine.start_state,
        machine.accept_state,
        machine.reject_state,
    ]
    return SECTION_SEP.join(sections)


def encode_instance(machine: TuringMachine, input_string: str) -> str:
    """Turns (M, w) into <M>#w, the string the UTM actually reads."""
    return f"{encode_machine(machine)}{SECTION_SEP}{input_string}"


def _encode_transition(t: Transition) -> str:
    """Turns one transition into 'state,read,next_state,write,direction'."""
    return FIELD_SEP.join([t.state, t.read, t.next_state, t.write, t.move.value])


def _check_names(machine: TuringMachine) -> None:
    names = {*machine.states, *machine.tape_alphabet}
    for name in names:
        if not is_valid_name(name):
            raise EncodingError(f"name {name!r} can't be encoded (uses a reserved character)")
