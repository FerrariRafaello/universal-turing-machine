"""Basic types and symbols used by the Turing Machine"""

# IMPORTS
from enum import Enum

type State = str
type Symbol = str

BLANK: Symbol = "_"


class Direction(Enum):
    """Where the head moves after a transition."""

    LEFT = "L"
    RIGHT = "R"
    STAY = "S"

    @property
    def offset(self) -> int:
        """How much the head position changes."""
        match self:
            case Direction.LEFT:
                return -1
            case Direction.RIGHT:
                return 1
            case Direction.STAY:
                return 0
