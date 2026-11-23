# CubeMind fusion playbook — how the fusion engine was built, and how you (CubeMind) carry it on
Written 23 Nov 2026 for CubeMind by the cloud session, at Danny's request ("tell it exactly how you've gotten to this point and have it run it").

## The goal
The top goalpost is **net electricity from D-T fusion**. Under it sit seven sections (a fractal network: any section can open into its own
sub-engines; links may run up, down or sideways): S1 reactions, S2 ignition, S3 tokamak operating point with dials, S4 inertial fusion
(OU's IFE-STARFIRE hub), S5 fuel cycle (linked to Chronos for tritium decay), S6 neutrons and materials, S7 stars (the Gamow peak).
Code: aegis_tools/aegis_bundle/tools/fusion (fusion.py, fusion_fast.py, net.py, sim.py, adas.py, nuclide_pulse.py, fusion_cm.py).

## The method (the Prometheus loop) — every cycle, in this order
1. **Breathe in:** gather hints (aim for 20) from published sources about the worst open failure. Write each with its source.
2. **Lock:** write the plan and goalposts in a PREREG file and fingerprint it BEFORE computing. Include at least one held-out check that is
   never used to tune, and show the held-out check can actually move when the change is switched off (otherwise it proves nothing).
3. **Breathe out:** build and compute once.
4. **Referee:** an adversarial reviewer attacks the result. Every finding goes into a DEVIATIONS file BEFORE any fix. Exactly one rerun.
5. **Balance:** keep the change only if it moves closer to published values without breaking any other section. A new knob must pay for
   itself (BIC-style charge).
6. **Record:** a D-note, a ledger line, commit, push; every number goes into memory with its source and label.
**A stop is not the end:** when a cycle finds nothing (NULL), apply the fixes and widen to the next part of the goal (the big loom).
**Honest labels:** LIVE (computed), INPUT, LIT (from literature), DATA, PREDICTION, post-hoc. Failures stay on the record.

## What has been established (numbers you can check with the fusion_* tools)
- D-T reactivity matches the Bosch-Hale tables to 4 figures (1.136e-16 cm^3/s at 10 keV). Q(D-T) = 17.589 MeV; neutron 14.028 MeV
  (relativistic, reactants at rest — the common "14.07" is the 4/5 shortcut).
- Ignition: minimum n T tau_E = 2.91e21 keV s m^-3 at 14.2 keV; ideal ignition 4.29 keV.
- ITER (0-D, pedestal profiles, Lux radiation correction, self-consistent helium ash): 400 MW case reproduced (390 MW, tau_E 3.41 s, Q 9.7);
  500 MW case: P_fus 532 MW, tau_E 2.88 s (15% low; the loss-power definition is the open question).
- Net electricity on an ITER-sized machine with a DEMO-style plant and ITER's ~100 MW house loads: about +21 MW at best, about -89 MW with
  today's heating efficiency (25%). An ITER-sized Q ~ 10 machine is marginal for net power.
- NIF August 2021 shot: inferred hot-spot pressure 545 Gbar (published 569 +- 61; same 0-D method, so a consistency check). Ignition criteria met.
- Tritium: 56.08 kg burned per GW-full-power-year; breeding ratio 1.051 doubles 10 kg in 5 years at 1 GW; 1.010 just holds it.
- Impurity radiation from OPEN-ADAS (line + recombination, minus the bremsstrahlung already counted): 19.1 MW for ITER's argon and
  beryllium vs the table's 27 MW (-29%). Not yet adopted (it pushes the held-out 400 MW check just outside tolerance).
- Simulations: the burn is thermally stable, resettles in ~25 s after a heating step; helium ash builds on ~12 s.
- Data pulses: 24 elements (ADAS cooling curves) and 5,823 nuclides (NUBASE2020) catalogued; Chronos half-lives agree with NUBASE2020 within 0.4%.

## Mistakes that were caught (learn from them)
- Goalposts copied from shortcuts (14.07 MeV, 55.8 kg, a 15 MK value used at 15.7 MK) — always derive the benchmark from the same recipe.
- A fit that "matched" ITER by cancelling errors (missing radiation vs too much dilution) — check each term against the source table.
- A test that could not fail (comparing a change against itself) — show the test moves when the change is off.
- A plasma used above its own density limit — every reported point must pass the same limits the dials enforce.
- Leaving out recombination radiation — at 5-15 keV it exceeds argon's line radiation.

## Your job now (what you run)
- The calc queue (weave_data/calc_queue.jsonl) holds 46 fusion tasks: derive each number yourself, step by step, BEFORE the tool runs;
  the fusion_* tool then grades you. Your derivations are stored as checked or failed.
- When you propose something new, give the tool, the args, your predicted value and a tolerance; it is stored as a HYPOTHESIS until the
  tool confirms it. You never change the engine yourself: changes go through a lock, a referee and Danny.
