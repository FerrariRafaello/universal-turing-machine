# Theory

## The 7-tuple

A Turing machine here is the formal 7-tuple:

    M = (Q, Sigma, Gamma, delta, q0, q_accept, q_reject)

- `Q`: set of states (`TuringMachine.states`)
- `Sigma`: input alphabet, symbols allowed in w
- `Gamma`: tape alphabet, with `Sigma ⊆ Gamma` plus a blank symbol `_`
- `delta`: transition function, `Q x Gamma -> Q x Gamma x {L, R, S}`.
  It's partial: no rule for (state, symbol) means the machine halts and rejects.
- `q0`: start state
- `q_accept`, `q_reject`: the two halting states, must be different

`S` (stay) was added just for convenience. Any machine using `S` can be
rewritten with only `L`/`R`, so it doesn't add computational power.

`TuringMachine.__post_init__` checks all of this when a machine is created,
so an invalid machine can never exist as an object.

## Configurations

A configuration is a snapshot of the machine while running: current state +
tape + head position (`Configuration` class). Running the machine is just a
sequence of configurations, one after another, each one following from
applying delta once. That sequence is the trace.

## Halting

A machine halts when it reaches `q_accept` or `q_reject`. In this project
a run can stop 3 ways:

- reaches a halting state (accept/reject)
- gets stuck: no rule for (state, symbol) -> counts as reject
- hits `max_steps` without halting

The halting problem is undecidable: no algorithm can tell, for every M and
w, if M will ever halt. So this project doesn't try to detect infinite
loops. It just caps the number of steps and reports `STEP_LIMIT` if it runs
out. Hitting the limit doesn't mean the machine loops forever, it just
means we gave up waiting.

## Universal machine

A Universal Turing Machine (UTM) is one fixed machine that can simulate any
other machine M on any input w, as long as it's given a description of M.
This is the result that makes "general-purpose computers" possible.

The UTM here takes a string `<M>#w` and produces the same result M would
on w. It's built with 3 tapes:

1. description tape: holds `<M>`, never changes
2. state tape: holds M's current state
3. work tape: holds M's simulated tape

Each step, it looks up (current state, symbol under the head of the work
tape) in M's transition table, then updates the work tape and the state.

Important: `run_universal` never calls the direct simulator on M. It reads
`<M>` once to get the transition table, but the simulation loop itself is
separate code. That's what makes the equivalence test mean something: it's
checking two different implementations agree, not one implementation
agreeing with itself.
