"""Turing Machine definition: the 7-tuple (Q, Sigma, Gamma, delta, q0, q_accept, q_reject)."""

# IMPORTS
from collections.abc import Iterable
from dataclasses import dataclass

from utm.core.errors import InvalidTransitionError, MachineDefinitionError
from utm.core.symbols import BLANK, State, Symbol
from utm.core.transition import Transition, TransitionFunction


@dataclass(frozen=True)
class TuringMachine:
    """A deterministic single-tape turing machine."""

    states: frozenset[State]
    input_alphabet: frozenset[Symbol]
    tape_alphabet: frozenset[Symbol]
    transitions: TransitionFunction
    start_state: State
    accept_state: State
    reject_state: State
    blank: Symbol = BLANK

    def __post_init__(self) -> None:
        self._validate_states()
        self._validate_alphabets()
        self._validate_transitions()

    @classmethod
    def create(  # noqa: PLR0913
        cls,
        *,
        states: Iterable[State],
        input_alphabet: Iterable[Symbol],
        tape_alphabet: Iterable[Symbol],
        transitions: Iterable[Transition],
        start_state: State,
        accept_state: State,
        reject_state: State,
        blank: Symbol = BLANK,
    ) -> "TuringMachine":
        """Builds a machine from plain lists or sets."""
        return cls(
            states=frozenset(states),
            input_alphabet=frozenset(input_alphabet),
            tape_alphabet=frozenset(tape_alphabet),
            transitions=TransitionFunction(transitions),
            start_state=start_state,
            accept_state=accept_state,
            reject_state=reject_state,
            blank=blank,
        )

    def is_halting(self, state: State) -> bool:
        return state in (self.accept_state, self.reject_state)

    def _validate_states(self) -> None:
        for name, state in (
            ("start", self.start_state),
            ("accept", self.accept_state),
            ("reject", self.reject_state),
        ):
            if state not in self.states:
                raise MachineDefinitionError(f"{name} state {state!r} is not in the set of states")
        if self.accept_state == self.reject_state:
            raise MachineDefinitionError("accept and reject states must be different")

    def _validate_alphabets(self) -> None:
        for symbol in self.tape_alphabet:
            if len(symbol) != 1:
                raise MachineDefinitionError(f"symbol {symbol!r} must be a single character")
        if self.blank not in self.tape_alphabet:
            raise MachineDefinitionError("blank symbol must be in the tape alphabet")
        if self.blank in self.input_alphabet:
            raise MachineDefinitionError("blank symbol can't be in the input alphabet")
        if not self.input_alphabet <= self.tape_alphabet:
            raise MachineDefinitionError("input alphabet must be a subset of the tape alphabet")

    def _validate_transitions(self) -> None:
        for t in self.transitions.values():
            if self.is_halting(t.state):
                raise InvalidTransitionError(f"halting state {t.state!r} can't have transitions")
            for state in (t.state, t.next_state):
                if state not in self.states:
                    raise InvalidTransitionError(f"unknown state {state!r} in {t}")
            for symbol in (t.read, t.write):
                if symbol not in self.tape_alphabet:
                    raise InvalidTransitionError(f"unknown symbol {symbol!r} in {t}")
