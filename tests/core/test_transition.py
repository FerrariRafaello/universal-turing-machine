"""Tests for Transition and TransitionFunction."""

# IMPORTS
import pytest

from utm.core.errors import InvalidTransitionError
from utm.core.symbols import Direction
from utm.core.transition import Transition, TransitionFunction


def test_transition_key_is_state_and_read_symbol() -> None:
    t = Transition("q0", "1", "q1", "0", Direction.RIGHT)
    assert t.key == ("q0", "1")


def test_transition_str() -> None:
    t = Transition("q0", "1", "q1", "0", Direction.RIGHT)
    assert str(t) == "d(q0, 1) = (q1, 0, R)"


def test_transition_is_immutable() -> None:
    t = Transition("q0", "1", "q1", "0", Direction.RIGHT)
    with pytest.raises(AttributeError):
        t.state = "q1"  # type: ignore[misc]


def test_function_looks_up_by_key() -> None:
    t = Transition("q0", "1", "q1", "0", Direction.RIGHT)
    delta = TransitionFunction([t])
    assert delta[("q0", "1")] is t
    assert delta.get(("q0", "0")) is None


def test_function_is_a_mapping() -> None:
    t1 = Transition("q0", "0", "q0", "0", Direction.RIGHT)
    t2 = Transition("q0", "1", "q1", "1", Direction.RIGHT)
    delta = TransitionFunction([t1, t2])
    assert len(delta) == 2
    assert ("q0", "0") in delta
    assert set(delta) == {("q0", "0"), ("q0", "1")}


def test_two_functions_with_same_rules_are_equal() -> None:
    t1 = Transition("q0", "0", "q0", "0", Direction.RIGHT)
    t2 = Transition("q0", "1", "q1", "1", Direction.RIGHT)
    assert TransitionFunction([t1, t2]) == TransitionFunction([t2, t1])


def test_duplicate_key_raises_invalid_transition_error() -> None:
    t1 = Transition("q0", "0", "q0", "0", Direction.RIGHT)
    t2 = Transition("q0", "0", "q1", "1", Direction.LEFT)
    with pytest.raises(InvalidTransitionError):
        TransitionFunction([t1, t2])
