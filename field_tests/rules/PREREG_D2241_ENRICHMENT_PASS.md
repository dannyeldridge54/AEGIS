# PREREG D2241 — Divertor enrichment pass (reactor paper 2, final test), locked 2026-11-23

Question: D2240 brought divertor argon under the 5% cap with a long-leg divertor, but the core then holds
SOL/3 argon and stops burning. If the divertor keeps argon better (enrichment eta = c_div/c_core > 3),
does a design meet every limit?

Engine: theory/tests/d2240_exhaust.py main configuration (leg 1-5, nu 0.4-0.6), unchanged except the core
argon floor c/3 becomes c/eta with an added knob eta ladder [3, 5, 10].
Literature: enrichment ~3 measured for nitrogen on ASDEX Upgrade with "considerable uncertainty"; no
measured argon value; DIII-D puff-and-pump reports strong compression without a number (Kallenbach et al.).
Labels fixed now: eta = 3 LITERATURE; eta = 5 and 10 UNVERIFIED (optimistic, not measured for argon).

Control: eta = 3 only must reproduce D2240 main endpoints (all infeasible).
Verdicts (fixed now):
- OPEN AT LITERATURE: a feasible endpoint with eta = 3.
- CONDITIONAL OPEN: feasible endpoints only at eta >= 5; report the smallest eta that works per start.
- CLOSED: none feasible.
TRIANGULATED if >= 2 of 3 starts per coil class end within one ladder step on every knob.
Run once; fixes only via _DEVIATIONS.md written before any rerun.
