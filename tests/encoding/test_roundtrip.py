"""Tests for encoding and decoding <M> and <M>#w."""

# IMPORTS
import pytest
from hypothesis import given
from hypothesis import strategies as st

from utm.core.errors import DecodingError
from utm.core.machine import TuringMachine
from utm.core.symbols import Direction
from utm.core.transition import Transition
from utm.encoding.decoder import decode_instance, decode_machine
from utm.encoding.encoder import encode_instance, encode_machine


def test_roundtrip_even_ones(even_ones_machine: TuringMachine) -> None:
    assert decode_machine(encode_machine(even_ones_machine)) == even_ones_machine


def test_roundtrip_stuck_machine(stuck_machine: TuringMachine) -> None:
    assert decode_machine(encode_machine(stuck_machine)) == stuck_machine


def test_roundtrip_instance_recovers_input(even_ones_machine: TuringMachine) -> None:
    machine, w = decode_instance(encode_instance(even_ones_machine, "0110"))
    assert machine == even_ones_machine
    assert w == "0110"


def test_wrong_section_count_raises_decoding_error() -> None:
    with pytest.raises(DecodingError):
        decode_machine("too#few#sections")


def test_malformed_transition_raises_decoding_error() -> None:
    with pytest.raises(DecodingError):
        decode_machine("q0,qa,qr#0#0,_#q0,0,qa#q0#qa#qr")


def test_unknown_direction_raises_decoding_error() -> None:
    with pytest.raises(DecodingError):
        decode_machine("q0,qa,qr#0#0,_#q0,0,qa,0,X#q0#qa#qr")


def test_name_with_reserved_char_cannot_be_encoded() -> None:
    machine = TuringMachine.create(
        states={"q#0", "qa", "qr"},
        input_alphabet=set(),
        tape_alphabet={"_"},
        transitions=[],
        start_state="q#0",
        accept_state="qa",
        reject_state="qr",
    )
    with pytest.raises(Exception, match="reserved character"):
        encode_machine(machine)


# Property-based: for any valid machine built this way, decode(encode(M)) == M.
@st.composite
def _machines(draw: st.DrawFn) -> TuringMachine:
    symbols = frozenset({"0", "1", "_"})
    non_halting = [f"s{i}" for i in range(draw(st.integers(min_value=1, max_value=3)))]
    states = frozenset({*non_halting, "acc", "rej"})

    transitions = []
    for state in non_halting:
        for symbol in symbols:
            if draw(st.booleans()):
                transitions.append(
                    Transition(
                        state=state,
                        read=symbol,
                        next_state=draw(st.sampled_from(sorted(states))),
                        write=draw(st.sampled_from(sorted(symbols))),
                        move=draw(st.sampled_from(list(Direction))),
                    )
                )

    return TuringMachine.create(
        states=states,
        input_alphabet={"0", "1"},
        tape_alphabet=symbols,
        transitions=transitions,
        start_state=non_halting[0],
        accept_state="acc",
        reject_state="rej",
    )


@given(_machines())
def test_roundtrip_property(machine: TuringMachine) -> None:
    assert decode_machine(encode_machine(machine)) == machine
