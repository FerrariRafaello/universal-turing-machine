"""Shared fixtures: small Turing machines used across the test suite."""

# IMPORTS
import pytest

from utm.core.machine import TuringMachine
from utm.core.symbols import Direction
from utm.core.transition import Transition


@pytest.fixture
def even_ones_machine() -> TuringMachine:
    """Accepts binary strings with an even number of 1s."""
    return TuringMachine.create(
        states={"even", "odd", "qa", "qr"},
        input_alphabet={"0", "1"},
        tape_alphabet={"0", "1", "_"},
        transitions=[
            Transition("even", "0", "even", "0", Direction.RIGHT),
            Transition("even", "1", "odd", "1", Direction.RIGHT),
            Transition("even", "_", "qa", "_", Direction.STAY),
            Transition("odd", "0", "odd", "0", Direction.RIGHT),
            Transition("odd", "1", "even", "1", Direction.RIGHT),
            Transition("odd", "_", "qr", "_", Direction.STAY),
        ],
        start_state="even",
        accept_state="qa",
        reject_state="qr",
    )


@pytest.fixture
def stuck_machine() -> TuringMachine:
    """Has no transitions at all: rejects everything by getting stuck."""
    return TuringMachine.create(
        states={"q0", "qa", "qr"},
        input_alphabet={"0"},
        tape_alphabet={"0", "_"},
        transitions=[],
        start_state="q0",
        accept_state="qa",
        reject_state="qr",
    )


@pytest.fixture
def infinite_loop_machine() -> TuringMachine:
    """Never halts: stays on the same cell and state forever."""
    return TuringMachine.create(
        states={"q0", "qa", "qr"},
        input_alphabet={"0"},
        tape_alphabet={"0", "_"},
        transitions=[Transition("q0", "0", "q0", "0", Direction.STAY)],
        start_state="q0",
        accept_state="qa",
        reject_state="qr",
    )
