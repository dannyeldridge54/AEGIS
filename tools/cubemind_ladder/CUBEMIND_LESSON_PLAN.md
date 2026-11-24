# CubeMind lesson plan — from the nucleus to reactors, fields, circuits and CPU chips (23 Nov 2026)

How it runs: the 13 new tracks below are added to janus/curriculum.py (file janus/curriculum_ladder.py). The existing Janus loop
picks them up automatically: lessons, locked answers, mirrored faces, retakes of wrong items, held-out exams, mastery per track.
Every lesson has one exact answer checked by code (no model grading). Lessons and exams never share a question.
Fast loops: keep the loop running continuously (no timer between rounds); every round covers all tracks; exams every few rounds.
Promotion rule: a stage counts as LEARNED when both faces reach mastery on all of its tracks in the held-out exams (the loop's
own mastery rule). Then move up to the stage's DESIGN PROJECT (below), which is done with the validated tools, locked first.

## Stage 1 — Nuclear basics (tracks nuc_count, nuc_binding, nuc_decay, nuc_qvalue)
Protons and neutrons; binding energy from mass excess; half-lives; reaction Q-values (D-T 17.6 MeV, D-D, D-He3, n+Li-6).
Read: CUBEMIND_NUCLEAR_BRIEF_2026-11-23.md levels L1-L2; weave_data/nuclide_catalog.json.
Design project 1: rebuild the binding-energy curve from the catalog and state the iron/nickel peak with numbers.

## Stage 2 — Reactor physics and design (rx_power, rx_limits, rx_breeding)
Fusion and alpha power, plasma gain Q, plant net power, triple product, Greenwald limit, divertor limit P_sep/R, EU-DEMO H-mode
rule, tritium breeding ratio. Read: brief L3-L6; Reactor Papers 1-3.
Design project 2 (the real work queue): (a) verify the core radiation budget (synchrotron, bremsstrahlung, argon) — top priority;
(b) L-mode profiles for negative triangularity; (c) stellarator mode with a W7-X positive control. Lock, run once, referee, record.

## Stage 3 — Fields (fields)
Lorentz force, solenoid field, magnetic pressure, Coulomb force. Then: plasma confinement as field geometry; why HTS magnets
(20 T at the coil) shrink reactors; stellarator coils.
Design project 3: field and force budget for an HTS toroidal coil (field on axis vs at the coil, magnetic pressure, stress), checked
against SPARC's published 12.2 T / 20 T coil numbers as the positive control.

## Stage 4 — Circuits (circuits)
Ohm's law, parallel resistance, dividers, RC time constants, power. Then: power supplies and pulsed systems for magnets and heating.
Design project 4: a quench-protection discharge circuit for a superconducting coil (energy, dump resistor, time constant, peak
voltage), with stated limits.

## Stage 5 — Digital logic (logic_gates, logic_code)
Binary, hex, two's complement, gates, full adders, bit manipulation in code. Then: adders, multiplexers, registers, finite-state
machines, timing.
Design project 5: a 4-bit ripple-carry adder and an 8-bit ALU written as Python gate-level simulations, exhaustively tested.

## Stage 6 — CPU design (cpu_trace, cpu_perf)
Instruction traces on a tiny register machine, pipeline cycles, run time from CPI and clock, cache AMAT, tag/index/offset bits.
Then: datapath and control, hazards and forwarding, branch prediction, memory hierarchy.
Design project 6: a tiny CPU (8 registers, LI/ADD/SUB/MUL/LD/ST/BEQ/JMP) as a cycle-accurate Python simulator with a 5-stage
pipeline, tested on programs whose results are known; report CPI and hazards. Later: express it in a hardware language (Verilog).

## Stage 7 — Build better, every loop
After each design project: one change at a time, locked prediction first, run once, keep it only if it measurably improves the
locked score; changed tools get new version names (tool registry rule); failures stay on the record.

## Standing rules
Honest labels (ESTIMATE / UNVERIFIED / SUSPECT); show every calculation; never quote corrected results (D2243a, D2244a); never publish.
