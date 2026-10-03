"""Tape of the Turing Machine, infinite in both directions."""

# IMPORTS
from collections.abc import Iterable

from utm.core.errors import TapeError
from utm.core.symbols import BLANK, Direction, Symbol


class Tape:
    """Infinite tape with one head."""

    def __init__(self, content: Iterable[Symbol] = (), blank: Symbol = BLANK) -> None:
        self._check(blank)
        self._blank = blank
        self._cells: dict[int, Symbol] = {}
        self._head = 0
        for i, symbol in enumerate(content):
            self._check(symbol)
            if symbol != blank:
                self._cells[i] = symbol

    @property
    def head(self) -> int:
        return self._head

    @property
    def blank(self) -> Symbol:
        return self._blank

    def read(self) -> Symbol:
        return self._cells.get(self._head, self._blank)

    def write(self, symbol: Symbol) -> None:
        self._check(symbol)
        if symbol == self._blank:
            self._cells.pop(self._head, None)
        else:
            self._cells[self._head] = symbol

    def move(self, direction: Direction) -> None:
        self._head += direction.offset

    def contents(self) -> str:
        """Tape content from the first to the last non-blank cell."""
        if not self._cells:
            return ""
        first, last = min(self._cells), max(self._cells)
        return "".join(self._cells.get(i, self._blank) for i in range(first, last + 1))

    def copy(self) -> "Tape":
        other = Tape(blank=self._blank)
        other._cells = dict(self._cells)
        other._head = self._head
        return other

    def __str__(self) -> str:
        """Shows the tape with the head between brackets, e.g. 1 0 [1] 1"""
        positions = [*self._cells, self._head]
        cells = []
        for i in range(min(positions), max(positions) + 1):
            symbol = self._cells.get(i, self._blank)
            cells.append(f"[{symbol}]" if i == self._head else symbol)
        return " ".join(cells)

    @staticmethod
    def _check(symbol: Symbol) -> None:
        if len(symbol) != 1:
            raise TapeError(f"tape symbols must be a single character, got {symbol!r}")
