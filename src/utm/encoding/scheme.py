"""Specification of the string encoding used for a Turing machine.

Instead of the classic binary encoding (Sipser), this project encodes a
machine as fields separated by reserved characters. It is still just a
string over a fixed alphabet, and the UTM still only manipulates tape
symbols, never rebuilding a TuringMachine object. This is simpler to
implement and debug, without losing conceptual correctness.
"""

FIELD_SEP = ","
TRANSITION_SEP = ";"
SECTION_SEP = "#"

RESERVED_CHARS = frozenset({FIELD_SEP, TRANSITION_SEP, SECTION_SEP})

SECTION_COUNT = 7


def is_valid_name(name: str) -> bool:
    """A state or symbol name can't be empty or contain a reserved char."""
    return len(name) > 0 and not any(c in RESERVED_CHARS for c in name)
