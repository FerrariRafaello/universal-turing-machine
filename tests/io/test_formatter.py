"""Tests for the output formatter."""

# IMPORTS
from utm.core.machine import TuringMachine
from utm.execution.simulator import run
from utm.io.formatter import format_result, format_step, format_trace


def test_format_step() -> None:
    result = run(TuringMachine.create(
        states={"q0", "qa", "qr"},
        input_alphabet=set(),
        tape_alphabet={"_"},
        transitions=[],
        start_state="q0",
        accept_state="qa",
        reject_state="qr",
    ), "")
    assert format_step(0, result.trace[0]) == "step 0: q0: "


def test_format_trace_has_one_line_per_step(even_ones_machine: TuringMachine) -> None:
    result = run(even_ones_machine, "0110")
    lines = format_trace(result.trace).splitlines()
    assert len(lines) == len(result.trace)
    assert lines[0].startswith("step 0:")


def test_format_result_reports_outcome(even_ones_machine: TuringMachine) -> None:
    result = run(even_ones_machine, "0110")
    text = format_result(result)
    assert "accepted after 5 steps" in text
    assert "final tape: '0110'" in text
