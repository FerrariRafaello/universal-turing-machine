""" The Universal Turing Machine: runs <M>#w step by step."""

# IMPORTS
from utm.core.tape import Tape
from utm.encoding.decoder import decode_instance
from utm.execution.configuration import Configuration
from utm.execution.result import ExecutionResult, HaltReason
from utm.execution.simulator import DEFAULT_MAX_STEPS
from utm.universal.multitape import MultiTape


def run_universal(encoded_instance: str, max_steps: int = DEFAULT_MAX_STEPS) -> ExecutionResult:
    """Runs <M>#w on the Universal machine."""
    machine, input_string = decode_instance(encoded_instance)
    tapes = MultiTape(
        description=encoded_instance,
        state=machine.start_state,
        work=input_string,
        blank=machine.blank,
    )

    state = machine.start_state
    trace = [Configuration(state, tapes.work.copy())]

    steps = 0
    while not machine.is_halting(state) and steps < max_steps:
        symbol = tapes.work.read()
        transition = machine.transitions.get((state, symbol))
        if transition is None:
            return _result(HaltReason.REJECTED, steps, state, tapes.work, trace)

        tapes.work.write(transition.write)
        tapes.work.move(transition.move)
        state = transition.next_state
        tapes.state = Tape(state, blank=machine.blank)

        steps += 1
        trace.append(Configuration(state, tapes.work.copy()))

    if machine.is_halting(state):
        reason = HaltReason.ACCEPTED if state == machine.accept_state else HaltReason.REJECTED
        return _result(reason, steps, state, tapes.work, trace)

    return _result(HaltReason.STEP_LIMIT, steps, state, tapes.work, trace)


def _result(
    reason: HaltReason,
    steps: int,
    state: str,
    work: Tape,
    trace: list[Configuration],
) -> ExecutionResult:
    return ExecutionResult(
        reason=reason,
        steps=steps,
        final_configuration=Configuration(state, work),
        trace=tuple(trace),
    )
