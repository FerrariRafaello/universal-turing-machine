"""Tests for TuringMachine: the validated 7-tuple."""

# IMPORTS
import pytest

from utm.core.errors import InvalidTransitionError, MachineDefinitionError
from utm.core.machine import TuringMachine
from utm.core.symbols import Direction
from utm.core.transition import Transition


def test_valid_machine_can_be_created(even_ones_machine: TuringMachine) -> None:
    assert even_ones_machine.start_state == "even"
    assert even_ones_machine.is_halting("qa")
    assert even_ones_machine.is_halting("qr")
    assert not even_ones_machine.is_halting("even")


def test_start_state_must_be_in_states() -> None:
    with pytest.raises(MachineDefinitionError):
        TuringMachine.create(
            states={"q0", "qa", "qr"},
            input_alphabet={"0"},
            tape_alphabet={"0", "_"},
            transitions=[],
            start_state="missing",
            accept_state="qa",
            reject_state="qr",
        )


def test_accept_and_reject_must_differ() -> None:
    with pytest.raises(MachineDefinitionError):
        TuringMachine.create(
            states={"q0", "qa"},
            input_alphabet={"0"},
            tape_alphabet={"0", "_"},
            transitions=[],
            start_state="q0",
            accept_state="qa",
            reject_state="qa",
        )


def test_blank_must_be_in_tape_alphabet() -> None:
    with pytest.raises(MachineDefinitionError):
        TuringMachine.create(
            states={"q0", "qa", "qr"},
            input_alphabet={"0"},
            tape_alphabet={"0"},
            transitions=[],
            start_state="q0",
            accept_state="qa",
            reject_state="qr",
            blank="_",
        )


def test_blank_cannot_be_in_input_alphabet() -> None:
    with pytest.raises(MachineDefinitionError):
        TuringMachine.create(
            states={"q0", "qa", "qr"},
            input_alphabet={"0", "_"},
            tape_alphabet={"0", "_"},
            transitions=[],
            start_state="q0",
            accept_state="qa",
            reject_state="qr",
        )


def test_input_alphabet_must_be_subset_of_tape_alphabet() -> None:
    with pytest.raises(MachineDefinitionError):
        TuringMachine.create(
            states={"q0", "qa", "qr"},
            input_alphabet={"0", "1"},
            tape_alphabet={"0", "_"},
            transitions=[],
            start_state="q0",
            accept_state="qa",
            reject_state="qr",
        )


def test_transition_cannot_reference_unknown_state() -> None:
    with pytest.raises(InvalidTransitionError):
        TuringMachine.create(
            states={"q0", "qa", "qr"},
            input_alphabet={"0"},
            tape_alphabet={"0", "_"},
            transitions=[Transition("q0", "0", "ghost", "0", Direction.RIGHT)],
            start_state="q0",
            accept_state="qa",
            reject_state="qr",
        )


def test_transition_cannot_reference_unknown_symbol() -> None:
    with pytest.raises(InvalidTransitionError):
        TuringMachine.create(
            states={"q0", "qa", "qr"},
            input_alphabet={"0"},
            tape_alphabet={"0", "_"},
            transitions=[Transition("q0", "9", "q0", "0", Direction.RIGHT)],
            start_state="q0",
            accept_state="qa",
            reject_state="qr",
        )


def test_halting_state_cannot_have_transitions() -> None:
    with pytest.raises(InvalidTransitionError):
        TuringMachine.create(
            states={"q0", "qa", "qr"},
            input_alphabet={"0"},
            tape_alphabet={"0", "_"},
            transitions=[Transition("qa", "0", "q0", "0", Direction.RIGHT)],
            start_state="q0",
            accept_state="qa",
            reject_state="qr",
        )


def test_two_machines_with_same_definition_are_equal(even_ones_machine: TuringMachine) -> None:
    same = TuringMachine.create(
        states=even_ones_machine.states,
        input_alphabet=even_ones_machine.input_alphabet,
        tape_alphabet=even_ones_machine.tape_alphabet,
        transitions=even_ones_machine.transitions.values(),
        start_state=even_ones_machine.start_state,
        accept_state=even_ones_machine.accept_state,
        reject_state=even_ones_machine.reject_state,
    )
    assert same == even_ones_machine
