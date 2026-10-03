"""Transitions and the transition function (delta)."""

# IMPORTS
from collections.abc import Iterable, Iterator, Mapping
from dataclasses import dataclass

from utm.core.errors import InvalidTransitionError
from utm.core.symbols import Direction, State, Symbol

type TransitionKey = tuple[State, Symbol]


@dataclass(frozen=True, slots=True)
class Transition:
    """One rule of delta: (state, read) -> (next_state, write, move)."""

    state: State
    read: Symbol
    next_state: State
    write: Symbol
    move: Direction

    @property
    def key(self) -> TransitionKey:
        return (self.state, self.read)

    def __str__(self) -> str:
        return (
            f"d({self.state}, {self.read}) = "
            f"({self.next_state}, {self.write}, {self.move.value})"
        )


class TransitionFunction(Mapping[TransitionKey, Transition]):
    """Transition function delta."""

    def __init__(self, transitions: Iterable[Transition]) -> None:
        table: dict[TransitionKey, Transition] = {}
        for t in transitions:
            if t.key in table:
                raise InvalidTransitionError(f"more than one transition for {t.key}")
            table[t.key] = t
        self._table = table

    def __getitem__(self, key: TransitionKey) -> Transition:
        return self._table[key]

    def __iter__(self) -> Iterator[TransitionKey]:
        return iter(self._table)

    def __len__(self) -> int:
        return len(self._table)

    def __repr__(self) -> str:
        return f"TransitionFunction({list(self._table.values())!r})"
