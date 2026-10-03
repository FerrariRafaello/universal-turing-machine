"""Loads and saves TuringMachine definitions as JSON files."""

# IMPORTS
import json
from pathlib import Path

from utm.core.errors import MachineDefinitionError, MachineLoadError
from utm.core.machine import TuringMachine
from utm.core.symbols import Direction
from utm.core.transition import Transition


def load_machine(path: str | Path) -> TuringMachine:
    """Reads a TuringMachine from a JSON file."""
    try:
        data = json.loads(Path(path).read_text())
    except (OSError, json.JSONDecodeError) as error:
        raise MachineLoadError(f"can't read {path}: {error}") from error

    try:
        transitions = [
            Transition(
                state=t["state"],
                read=t["read"],
                next_state=t["next_state"],
                write=t["write"],
                move=Direction(t["move"]),
            )
            for t in data["transitions"]
        ]
        return TuringMachine.create(
            states=data["states"],
            input_alphabet=data["input_alphabet"],
            tape_alphabet=data["tape_alphabet"],
            transitions=transitions,
            start_state=data["start_state"],
            accept_state=data["accept_state"],
            reject_state=data["reject_state"],
            blank=data.get("blank", "_"),
        )
    except (KeyError, ValueError, TypeError, MachineDefinitionError) as error:
        raise MachineLoadError(f"invalid machine definition in {path}: {error}") from error


def save_machine(machine: TuringMachine, path: str | Path) -> None:
    """Writes a TuringMachine to a JSON file."""
    data = {
        "states": sorted(machine.states),
        "input_alphabet": sorted(machine.input_alphabet),
        "tape_alphabet": sorted(machine.tape_alphabet),
        "blank": machine.blank,
        "start_state": machine.start_state,
        "accept_state": machine.accept_state,
        "reject_state": machine.reject_state,
        "transitions": [
            {
                "state": t.state,
                "read": t.read,
                "next_state": t.next_state,
                "write": t.write,
                "move": t.move.value,
            }
            for t in sorted(machine.transitions.values(), key=lambda t: t.key)
        ],
    }
    Path(path).write_text(json.dumps(data, indent=2) + "\n")
