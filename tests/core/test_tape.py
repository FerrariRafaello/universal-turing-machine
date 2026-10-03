"""Tests for the Tape class."""

# IMPORTS
import pytest

from utm.core.errors import TapeError
from utm.core.symbols import Direction
from utm.core.tape import Tape


def test_new_tape_is_blank() -> None:
    tape = Tape()
    assert tape.read() == "_"
    assert tape.head == 0
    assert tape.contents() == ""


def test_tape_starts_with_given_content() -> None:
    tape = Tape("101")
    assert tape.read() == "1"
    assert tape.contents() == "101"


def test_write_then_read() -> None:
    tape = Tape()
    tape.write("1")
    assert tape.read() == "1"


def test_move_right_and_left() -> None:
    tape = Tape("101")
    tape.move(Direction.RIGHT)
    assert tape.head == 1
    assert tape.read() == "0"
    tape.move(Direction.LEFT)
    tape.move(Direction.LEFT)
    assert tape.head == -1
    assert tape.read() == "_"


def test_move_stay_does_not_change_head() -> None:
    tape = Tape("1")
    tape.move(Direction.STAY)
    assert tape.head == 0


def test_writing_blank_clears_the_cell() -> None:
    tape = Tape("1")
    tape.write("_")
    assert tape.contents() == ""


def test_contents_spans_from_first_to_last_non_blank_cell() -> None:
    tape = Tape()
    tape.write("1")
    tape.move(Direction.RIGHT)
    tape.move(Direction.RIGHT)
    tape.write("1")
    assert tape.contents() == "1_1"


def test_copy_is_independent_from_original() -> None:
    original = Tape("1")
    clone = original.copy()
    clone.write("0")
    assert original.read() == "1"
    assert clone.read() == "0"


def test_str_marks_the_head() -> None:
    tape = Tape("101")
    assert str(tape) == "[1] 0 1"


def test_invalid_symbol_raises_tape_error() -> None:
    tape = Tape()
    with pytest.raises(TapeError):
        tape.write("ab")


def test_invalid_blank_raises_tape_error() -> None:
    with pytest.raises(TapeError):
        Tape(blank="ab")
