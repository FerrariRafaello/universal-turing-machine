"""Tests for save_machine and load_machine."""

# IMPORTS
from pathlib import Path

import pytest

from utm.core.errors import MachineLoadError
from utm.core.machine import TuringMachine
from utm.io.loader import load_machine, save_machine


def test_roundtrip(even_ones_machine: TuringMachine, tmp_path: Path) -> None:
    path = tmp_path / "machine.json"
    save_machine(even_ones_machine, path)
    assert load_machine(path) == even_ones_machine


def test_missing_file_raises_machine_load_error(tmp_path: Path) -> None:
    with pytest.raises(MachineLoadError):
        load_machine(tmp_path / "does_not_exist.json")


def test_invalid_json_raises_machine_load_error(tmp_path: Path) -> None:
    path = tmp_path / "broken.json"
    path.write_text("{not valid json")
    with pytest.raises(MachineLoadError):
        load_machine(path)


def test_missing_field_raises_machine_load_error(tmp_path: Path) -> None:
    path = tmp_path / "incomplete.json"
    path.write_text('{"states": ["q0"]}')
    with pytest.raises(MachineLoadError):
        load_machine(path)


def test_invalid_machine_definition_raises_machine_load_error(tmp_path: Path) -> None:
    path = tmp_path / "inconsistent.json"
    path.write_text(
        """
        {
            "states": ["q0", "qa", "qr"],
            "input_alphabet": ["0"],
            "tape_alphabet": ["0", "_"],
            "blank": "_",
            "start_state": "missing",
            "accept_state": "qa",
            "reject_state": "qr",
            "transitions": []
        }
        """
    )
    with pytest.raises(MachineLoadError):
        load_machine(path)


def test_unknown_direction_raises_machine_load_error(tmp_path: Path) -> None:
    path = tmp_path / "bad_direction.json"
    path.write_text(
        """
        {
            "states": ["q0", "qa", "qr"],
            "input_alphabet": ["0"],
            "tape_alphabet": ["0", "_"],
            "blank": "_",
            "start_state": "q0",
            "accept_state": "qa",
            "reject_state": "qr",
            "transitions": [
                {"state": "q0", "read": "0", "next_state": "qa", "write": "0", "move": "X"}
            ]
        }
        """
    )
    with pytest.raises(MachineLoadError):
        load_machine(path)
