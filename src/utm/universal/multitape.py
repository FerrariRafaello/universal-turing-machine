"""The 3 tapes used by the universal machine to simulate M."""

# IMPORTS
from utm.core.symbols import BLANK, Symbol
from utm.core.tape import Tape


class MultiTape:
    """Groups the 3 tapes the UTM needs: description, state and work."""

    def __init__(self, description: str, state: str, work: str, blank: Symbol = BLANK) -> None:
        self.description = Tape(description, blank=blank)
        self.state = Tape(state, blank=blank)
        self.work = Tape(work, blank=blank)

    def __str__(self) -> str:
        return f"description: {self.description}\nstate: {self.state}\nwork: {self.work}"

