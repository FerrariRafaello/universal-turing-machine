"""Instantaneous configuration of a Turing Machine during execution."""

# IMPORTS
from dataclasses import dataclass

from utm.core.symbols import State
from utm.core.tape import Tape


@dataclass(frozen=True, slots=True)
class Configuration:
    """A snapshot of the machine at one point in the execution."""
    state: State
    tape: Tape

    def __str__(self) -> str:
        """Shows as 'state: tape content with head marked'."""
        return f"{self.state}: {self.tape}"
