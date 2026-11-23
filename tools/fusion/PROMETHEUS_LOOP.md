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
Cycle log: 1 (PROM-1) pedestal + radiation correction + He ash: held-out ITER 400 MW PASS; 500 MW tau_E -15%. 2 (PROM-2) NULL after R85 -> loop stopped (D2194a).

## Guard rails added 23 Nov 2026 (Danny 13:48 "have the referee go through the code and everything to limit this")
- Before EVERY locked compute: `python3 tools/fusion/preflight.py` must print OK (compiles all code, checks lock fingerprints,
  flags corrected goalposts reappearing: 0.7997, 14.07, 5.9 keV at 15.7 MK, 55.8 kg, the 3.0-4.4 s window, 336 eV, 4.468e9 y, the KM branch).
  New stale values found by a referee get added to STALE in preflight.py the same day.
- Goalposts are copied from the CURRENT deviations file, never from an older lock; each goalpost carries its source in the lock.
- No inline comments inside expressions in test scripts (they broke three runs); comments go on their own line.
- Back-end audits: two read-only referees (neutron side, plasma/plant side) go through every module, not just each result.
