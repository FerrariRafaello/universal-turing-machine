# Universal Turing Machine

Student: Rafaello Ferrari<br>
Student ID: 2026200940<br>
University: Unicarioca<br>
Course: Formal Languages<br>
Professor: Julio Tadeu

## About

This is a project for the Formal Languages course. The goal is to build a
Universal Turing Machine (UTM) in Python: a single machine that can
simulate any other Turing machine M running on an input w, given a
description of M.

The project has 4 main layers:

- `core`: the formal model (states, tape, transitions, the 7-tuple)
- `execution`: a direct simulator, runs a machine step by step
- `encoding`: turns a machine into a string `<M>` and back
- `universal`: the UTM itself, runs `<M>#w` without calling the direct
  simulator on M

The central idea tested in this project: running the UTM on `<M>#w` should
give the exact same result as running the direct simulator on `(M, w)`.
That's checked with automated tests, including property-based tests with
`hypothesis`.

More details on the theory and the encoding scheme are in `docs/`.

## Requirements

- Python 3.12+

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Run a machine directly:

```bash
python -m utm run machines/binary_increment.json 101
```

Encode a machine as `<M>` (or `<M>#w` if you pass an input):

```bash
python -m utm encode machines/binary_increment.json
python -m utm encode machines/binary_increment.json 101
```

Run a machine through the universal machine:

```bash
python -m utm universal machines/binary_increment.json 101
```

## Tests

```bash
pytest
```

With coverage:

```bash
pytest --cov
```

## Project structure

```
src/utm/
  core/        formal model: states, tape, transitions, machine
  execution/   direct simulator and execution result
  encoding/    <M> and <M>#w: encode/decode
  universal/   the universal machine (3 tapes)
  io/          load/save machines as JSON, format output
  cli.py       command-line interface

machines/      example machine definitions (JSON)
tests/         tests for every layer above
docs/          theory and encoding scheme
```
