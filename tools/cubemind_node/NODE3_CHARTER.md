# Node 3 charter: the Mind (the field-native model)

Node 1 maps the field. Node 2 builds. **Node 3 turns the index into a mind.** It is built once the field is mapped and the Builder has a
working tool package.

> **Goal: a local, field-native model that holds every record by its geometry, so recall is a short step instead of a search —
> fast and cheap on Danny's own hardware, growing over time into the patterns, recall and "senses" of a mind.**

## What it builds, smallest piece up
1. **The encoder.** Turn each record's address (ring, anchor, shape, weight, side, layer, epoch, string position) and its links into one
   compact code — a fixed-length vector. This is the record's place in the mind. Built from the index that already exists; no training run needed to start.
2. **Recall by nearness.** Given any record or question, find its code and return the nearest codes — instant, because it is one geometric
   step, not a scan. (This reuses Node 1's step-out / reduce-in retrieval, made fast by the encoder.)
3. **Senses.** One intake channel per kind of data (text, numbers/datasets, code, math results). Each sense turns raw input into a code the
   same way, so anything new lands in the right place automatically.
4. **Association and attention.** Strengthen links that fire together (the synapses already in the neural web); spend most effort on the
   busiest, best-supported lanes — the mind's attention.
5. **Patterns and habits over time.** As records accumulate, record which recalls were useful; the model learns to answer common questions
   before reasoning — the trained-reflex feel of a mind.

## "Fast like a quantum computer" — the honest meaning
Every bit is addressed by the same geometry, so comparing and recalling is a geometric step, not a search. The encoder makes that cheap on
local hardware. Not literal qubits; the speed comes from the index doing the work.

## Fixed rules (same as every node)
- Built on the signed index; every code traces back to a hashed record.
- Runs on local models and local compute only; keep cost low.
- Code proposed, saved, syntax-checked; run only when a human says so.
- Comes on only when the switchboard signals the field is mapped and a Builder tool package exists.
