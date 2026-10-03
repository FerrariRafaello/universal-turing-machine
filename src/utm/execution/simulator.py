"""Direct simulator: runs a Turing Machine step by step."""

# IMPORTS
from utm.core.machine import TuringMachine
from utm.core.symbols import Symbol
from utm.core.tape import Tape
from utm.execution.configuration import Configuration
from utm.execution.result import ExecutionResult, HaltReason

DEFAULT_MAX_STEPS = 100_000


def run(
    machine: TuringMachine,
    input_string: str,
    max_steps: int = DEFAULT_MAX_STEPS,
) -> ExecutionResult:
    """Runs the machine on input_string until it halts or max_steps is hit."""
    tape = Tape(input_string, blank=machine.blank)
    state = machine.start_state
    trace = [Configuration(state, tape.copy())]

    steps = 0
    while not machine.is_halting(state) and steps < max_steps:
        transition = machine.transitions.get((state, tape.read()))
        if transition is None:
            return _result(HaltReason.REJECTED, steps, state, tape, trace)

        tape.write(transition.write)
        tape.move(transition.move)
        state = transition.next_state
        steps += 1
        trace.append(Configuration(state, tape.copy()))

    if machine.is_halting(state):
        reason = HaltReason.ACCEPTED if state == machine.accept_state else HaltReason.REJECTED
        return _result(reason, steps, state, tape, trace)

    return _result(HaltReason.STEP_LIMIT, steps, state, tape, trace)


def _result(
    reason: HaltReason,
    steps: int,
    state: Symbol,
    tape: Tape,
    trace: list[Configuration],
) -> ExecutionResult:
    return ExecutionResult(
        reason=reason,
        steps=steps,
        final_configuration=Configuration(state, tape),
        trace=tuple(trace),
    )
