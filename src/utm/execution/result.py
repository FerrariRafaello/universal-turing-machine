"""Result of running a Turing machine."""

# IMPORTS
from dataclasses import dataclass
from enum import Enum

from utm.execution.configuration import Configuration


class HaltReason(Enum):
    """Why an execution stopped."""
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    STEP_LIMIT = "step_limit"


@dataclass(frozen=True, slots=True)
class ExecutionResult:
    """Outcome of simulating a machine on some input."""
    reason: HaltReason
    steps: int
    final_configuration: Configuration
    trace: tuple[Configuration, ...]

    @property
    def accepted(self) -> bool:
        return self.reason is HaltReason.ACCEPTED

    def __str__(self) -> str:
        return f"{self.reason.value} after {self.steps} steps: {self.final_configuration}"
