"""Tests for the universal machine, including the central equivalence property:

For every machine M and input w, running the UTM on <M>#w must match
running the direct simulator on (M, w): same halt reason, same step
count, same final tape content.
"""

# IMPORTS
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from utm.core.machine import TuringMachine
from utm.encoding.encoder import encode_instance
from utm.execution.result import ExecutionResult
from utm.execution.simulator import run as simulate
from utm.universal.universal_machine import run_universal


def _assert_equivalent(direct: ExecutionResult, universal: ExecutionResult) -> None:
    assert direct.reason == universal.reason
    assert direct.steps == universal.steps
    direct_content = direct.final_configuration.tape.contents()
    universal_content = universal.final_configuration.tape.contents()
    assert direct_content == universal_content


def test_utm_matches_simulator_on_acceptance(even_ones_machine: TuringMachine) -> None:
    w = "0110"
    direct = simulate(even_ones_machine, w)
    universal = run_universal(encode_instance(even_ones_machine, w))
    _assert_equivalent(direct, universal)


def test_utm_matches_simulator_on_rejection(even_ones_machine: TuringMachine) -> None:
    w = "010"
    direct = simulate(even_ones_machine, w)
    universal = run_universal(encode_instance(even_ones_machine, w))
    _assert_equivalent(direct, universal)


def test_utm_matches_simulator_on_empty_input(even_ones_machine: TuringMachine) -> None:
    w = ""
    direct = simulate(even_ones_machine, w)
    universal = run_universal(encode_instance(even_ones_machine, w))
    _assert_equivalent(direct, universal)


def test_utm_matches_simulator_when_stuck(stuck_machine: TuringMachine) -> None:
    w = "0"
    direct = simulate(stuck_machine, w)
    universal = run_universal(encode_instance(stuck_machine, w))
    _assert_equivalent(direct, universal)


def test_utm_matches_simulator_on_step_limit(infinite_loop_machine: TuringMachine) -> None:
    w = "0"
    direct = simulate(infinite_loop_machine, w, max_steps=30)
    universal = run_universal(encode_instance(infinite_loop_machine, w), max_steps=30)
    _assert_equivalent(direct, universal)


@given(w=st.text(alphabet="01", max_size=8))
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_utm_matches_simulator_for_any_binary_input(
    even_ones_machine: TuringMachine, w: str
) -> None:
    direct = simulate(even_ones_machine, w)
    universal = run_universal(encode_instance(even_ones_machine, w))
    _assert_equivalent(direct, universal)
