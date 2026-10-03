"""Formats execution results for display in a terminal."""

# IMPORTS
from utm.execution.configuration import Configuration
from utm.execution.result import ExecutionResult


def format_step(index: int, config: Configuration) -> str:
    """One line of the trace: 'step N: state: tape'."""
    return f"step {index}: {config}"


def format_trace(trace: tuple[Configuration, ...]) -> str:
    """The whole trace, one step per line."""
    return "\n".join(format_step(i, c) for i, c in enumerate(trace))


def format_result(result: ExecutionResult) -> str:
    """The full trace followed by a short summary of the outcome."""
    lines = [
        format_trace(result.trace),
        "",
        f"result: {result.reason.value} after {result.steps} steps",
        f"final tape: {result.final_configuration.tape.contents()!r}",
    ]
    return "\n".join(lines)
