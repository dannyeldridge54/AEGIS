# PREREG D2189: "Chronos", a nuclear decay / isotope planning toolkit for Oklahoma's nuclear people
Locked 2026-11-23 ~08:40 CT, before code is written or run. Chronos: the Greek figure of time (Weave time-god naming).

## For whom (one engine, several schools)
- Nuclear pharmacy (OU College of Pharmacy, Dr. V. Awasthi): tracer activity planning (F-18, Ga-68, Tc-99m, Cu-64,
  Zr-89, Lu-177, Ac-225...), generator ingrowth/elution (Mo-99/Tc-99m, Ge-68/Ga-68, Sr-82/Rb-82).
- Radiation physics (OSU, Dr. E. Benton): same engine; dose module deferred to v2 (stated).
- Environmental radio-monitoring (OU, Dr. F. Xu, Fukushima radiocesium): Cs-134/Cs-137 (and I-131/Cs-137) "release
  clocks": time since release from a measured activity ratio.
- Nuclear energy / waste (Oklahoma's Nuclear Lifecycle Innovation Campus bid; Oklo, Deep Isolation): long-lived chains,
  e.g. Pu-241 -> Am-241 ingrowth, Sr-90/Y-90, Cs-137/Ba-137m.

## Method
Decay of a chain with branching solved two independent ways: (a) the matrix exponential of the decay matrix
(scipy.linalg.expm), (b) the analytic Bateman solution for linear chains with branching ratios. Half-lives and branching
from NNDC/NuDat (ENSDF) / DDEP; entered by hand and listed with each value in the output; referee to spot-check.

## Locked tests
T1: (a) and (b) agree to relative 1e-9 on every built-in chain at 20 log-spaced times from 1e-3 to 10 half-lives of the
    longest member (where activities exceed 1e-12 of the initial).
T2: Mo-99 -> Tc-99m (branching 0.876): time of maximum Tc-99m activity from pure Mo-99 within 22.5-23.5 h (textbook ~23 h);
    transient-equilibrium ratio A_Tc/A_Mo within 0.95-0.97.
T3: Pu-241 -> Am-241: time of maximum Am-241 activity within 65-75 y (textbook ~70 y).
T4: Release clock: generate a ratio at t = 0.5, 3, 10 y from an initial Cs-134/Cs-137 = 1.0 and invert; recover t to 1e-9.
## Honesty rules
v1 = decay arithmetic only; no production cross sections, no dose, no shielding (stated). Not a clinical or regulatory tool
(stated in the tool). Referee ping-pong until NULL before anything is sent. Nothing is emailed without Danny's "send".
