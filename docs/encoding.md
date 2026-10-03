# Encoding scheme

A Turing machine M is encoded as a string `<M>`. An instance (M, w) is
encoded as `<M>#w`, which is what the universal machine actually reads.

This is not the classic binary encoding from textbooks (Sipser uses binary
numbers for states/symbols). Here machines are encoded as plain text fields
separated by reserved characters instead. It's still just a string, and the
UTM still only works with tape symbols, never rebuilding a `TuringMachine`
object to run a step. Text fields are just way easier to read and debug
than binary.

## Reserved characters

From `encoding/scheme.py`:

| name             | char | what it separates                      |
|------------------|------|------------------------------------------|
| `FIELD_SEP`      | `,`  | items inside one section                |
| `TRANSITION_SEP` | `;`  | transitions from each other             |
| `SECTION_SEP`    | `#`  | sections of `<M>`, and `<M>` from `w`   |

A state/symbol name can't use any of these 3 chars, and can't be empty.

## Structure of `<M>`

7 sections, separated by `#`, always in this order:

states # input_alphabet # tape_alphabet # transitions # start # accept # reject



- `states`, `input_alphabet`, `tape_alphabet`: names separated by `,`
- `transitions`: separated by `;`, each one is 5 fields separated by `,`:
  `state,read,next_state,write,direction` (direction is `L`, `R` or `S`)
- `start`, `accept`, `reject`: just one state name each

## Structure of `<M>#w`

Just `<M>`, then `#`, then w. Since `<M>` always has 7 sections, splitting
on `#` and getting 8 parts (not 7) is how we know a `w` is there.

## Example

Machine that accepts binary strings with an even number of 1s:

even,odd,qa,qr#0,1#0,1,#even,0,even,0,R;even,1,odd,1,R;even,,qa,,S;odd,0,odd,0,R;odd,1,even,1,R;odd,,qr,_,S#even#qa#qr



With input `00`, just add `#00` at the end.

## Encoder / decoder

- `encoder.py`: turns a machine into `<M>` or `<M>#w`. Sorts everything
  first so the same machine always gives the same string.
- `decoder.py`: does the opposite. Raises `DecodingError` if the string is
  malformed (wrong number of sections, bad transition, etc). If the string
  is well-formed but describes a machine that doesn't make sense (like a
  start state that's not in the states), `TuringMachine.create` raises
  `MachineDefinitionError` instead.

`decode_machine(encode_machine(M)) == M` for any machine M. Tested in
`test_roundtrip.py`, including a hypothesis test with random machines.