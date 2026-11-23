# The Prometheus loop (working name; Danny may rename) — one loop for nuclear fusion, everything we learned folded in
Goal at the top: net electricity from D-T fusion. Engine: tools/fusion (fractal network: net.py; sections S1-S7 in fusion.py).
Each cycle breathes:
1. INHALE: gather 20 hints from published sources aimed at the worst open failure; log each with its source (hints/cycleN.json).
2. LOCK: PREREG_PROMN.md names which hints are acted on, the change, the goalposts, and at least one HELD-OUT check never used to tune.
3. EXHALE: build and compute once (Core-style: in-process, memoised; every number traceable).
4. REFEREE: an adversarial referee attacks the build (ping-pong); findings go to DEVIATIONS first; one rerun.
5. BALANCE: the change is kept only if it moves the engine closer to the published values without breaking any other section
   (the dials: bounded knobs against named limits; any new knob is charged).
6. RECORD: D-note, ledger line, commit and push; CubeMind memory gets every engine call through the Core.
NULL: a cycle whose 20 hints yield no accepted change ends the loop. Honest labels throughout: LIVE / INPUT / LIT / DATA / post-hoc.
Cycle log: 1 (PROM-1) pedestal + radiation correction + He ash: held-out ITER 400 MW PASS; 500 MW misses tau_E by 15%.
