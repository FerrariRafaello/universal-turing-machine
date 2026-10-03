"""Tests for the command-line interface."""

# IMPORTS
from pathlib import Path

import pytest

from utm.cli import main
from utm.core.machine import TuringMachine
from utm.io.loader import save_machine


@pytest.fixture
def machine_path(even_ones_machine: TuringMachine, tmp_path: Path) -> Path:
    path = tmp_path / "even_ones.json"
    save_machine(even_ones_machine, path)
    return path


def test_run_accepts(machine_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = main(["run", str(machine_path), "0110"])
    out = capsys.readouterr().out
    assert exit_code == 0
    assert "accepted after 5 steps" in out


def test_run_rejects(machine_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = main(["run", str(machine_path), "010"])
    out = capsys.readouterr().out
    assert exit_code == 0
    assert "rejected" in out


def test_encode_without_input_prints_just_machine(
    machine_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    main(["encode", str(machine_path)])
    out = capsys.readouterr().out.strip()
    assert "#" in out
    assert not out.endswith("#00")


def test_encode_with_input_appends_it(
    machine_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    main(["encode", str(machine_path), "00"])
    out = capsys.readouterr().out.strip()
    assert out.endswith("#00")


def test_universal_matches_run(
    machine_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    main(["run", str(machine_path), "0110"])
    run_out = capsys.readouterr().out
    main(["universal", str(machine_path), "0110"])
    universal_out = capsys.readouterr().out
    assert run_out == universal_out


def test_missing_machine_file_returns_error_code(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    exit_code = main(["run", str(tmp_path / "missing.json"), "0"])
    err = capsys.readouterr().err
    assert exit_code == 1
    assert "error:" in err


def test_no_command_exits_with_usage_error() -> None:
    with pytest.raises(SystemExit):
        main([])
