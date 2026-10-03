"""Command-line interface for the utm package."""

# IMPORTS
import argparse
import sys
from pathlib import Path

from utm.core.errors import UTMError
from utm.encoding.encoder import encode_instance, encode_machine
from utm.execution.simulator import run as simulate
from utm.io.formatter import format_result
from utm.io.loader import load_machine
from utm.universal.universal_machine import run_universal

DEFAULT_MAX_STEPS = 100_000


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="utm", description="A Universal Turing Machine toolkit.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Simulate a machine directly on an input.")
    run_parser.add_argument("machine", type=Path, help="Path to a machine JSON file.")
    run_parser.add_argument("input", nargs="?", default="", help="Input string (default: empty).")
    run_parser.add_argument("--max-steps", type=int, default=DEFAULT_MAX_STEPS)

    encode_parser = subparsers.add_parser("encode", help="Print <M> or <M>#w for a machine.")
    encode_parser.add_argument("machine", type=Path)
    encode_parser.add_argument("input", nargs="?", default=None)

    universal_parser = subparsers.add_parser(
        "universal", help="Simulate a machine through the UTM."
    )
    universal_parser.add_argument("machine", type=Path)
    universal_parser.add_argument("input", nargs="?", default="")
    universal_parser.add_argument("--max-steps", type=int, default=DEFAULT_MAX_STEPS)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "run":
            machine = load_machine(args.machine)
            result = simulate(machine, args.input, max_steps=args.max_steps)
            print(format_result(result))
        elif args.command == "encode":
            machine = load_machine(args.machine)
            if args.input is None:
                print(encode_machine(machine))
            else:
                print(encode_instance(machine, args.input))
        elif args.command == "universal":
            machine = load_machine(args.machine)
            encoded = encode_instance(machine, args.input)
            result = run_universal(encoded, max_steps=args.max_steps)
            print(format_result(result))
    except UTMError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    return 0
