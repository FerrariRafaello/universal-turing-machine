"""Tests for the direct simulator."""

# IMPORTS
from utm.core.machine import TuringMachine
from utm.execution.result import HaltReason
from utm.execution.simulator import run


def test_accepts_even_number_of_ones(even_ones_machine: TuringMachine) -> None:
    result = run(even_ones_machine, "0110")
    assert result.reason is HaltReason.ACCEPTED
    assert result.accepted


def test_rejects_odd_number_of_ones(even_ones_machine: TuringMachine) -> None:
    result = run(even_ones_machine, "010")
    assert result.reason is HaltReason.REJECTED
    assert not result.accepted


def test_accepts_empty_string(even_ones_machine: TuringMachine) -> None:
    result = run(even_ones_machine, "")
    assert result.accepted


def test_stuck_machine_rejects(stuck_machine: TuringMachine) -> None:
    result = run(stuck_machine, "0")
    assert result.reason is HaltReason.REJECTED
    assert result.steps == 0


def test_infinite_loop_hits_step_limit(infinite_loop_machine: TuringMachine) -> None:
    result = run(infinite_loop_machine, "0", max_steps=50)
    assert result.reason is HaltReason.STEP_LIMIT
    assert result.steps == 50


def test_trace_has_one_more_entry_than_steps(even_ones_machine: TuringMachine) -> None:
    result = run(even_ones_machine, "0110")
    assert len(result.trace) == result.steps + 1


def test_final_configuration_matches_tape_content(even_ones_machine: TuringMachine) -> None:
    result = run(even_ones_machine, "0110")
    assert result.final_configuration.tape.contents() == "0110"


def test_trace_entries_are_independent_snapshots(even_ones_machine: TuringMachine) -> None:
    result = run(even_ones_machine, "0110")
    first_tape = result.trace[0].tape
    last_tape = result.trace[-1].tape
    assert first_tape.head != last_tape.head
