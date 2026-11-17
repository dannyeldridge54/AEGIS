# New toolkits from what we learned (17 Nov 2026) — research summary + plan
Searched for prior art (web, 17 Nov):
- Warped-compactification KK spectra / stability: no general public package found — results are per-paper (e.g. 1911.01444, 2206.10628, hep-th/0512212);
  STRINGVACUA (0801.1508) is a Mathematica vacuum finder, not a spectrum/stability solver. → genuine gap.
- Inflation: MultiModeCode (1410.0685, Fortran, multi-field exact MS), PyTransport (1609.00381), CosmoBit/GAMBIT (2009.03286), InflationEasy (2506.11797,
  lattice C++), ASPIC (slow-roll library). Janus already beats ASPIC on accuracy (D1035, D1127: 188/188 points); its gap is multi-field exact MS.
Plan (one shared core, small focused packages, each validated before use):
1. KALUZA (new): KK masses + stability for 1D warped compactifications. Dual solvers (Prüfer shooting + finite differences, must agree), cutoff
   convergence with the derived order q = (D−2)/((D−1)(1+δ)) (D1038), sufficient-condition checks (BTR 2209.10553 Eq. 5.10, D1140), tensor + scalar
   master equations for general D. Validation targets: our S4c3 tower (D1036), BTR 10D critical scalar masses (Eq. 5.14), BMS 1811.11448 (D=10 coefficients).
2. JANUS-MF (Janus module, not a new toolkit): exact multi-field Mukhanov–Sasaki, validated against MultiModeCode/PyTransport the way Janus single-field
   was validated against ASPIC; keeps δN (twofield.py) as the fast path.
3. LOCKBENCH (method toolkit): the research workflow as code — lock + sha256 + push check (pcjob.py), resumable per-task-limited sweeps (sweep.py),
   PC/cloud runners, reference-precision ledger (every validation stores its reference's own spread), D-note/ladder hooks. Feeds CubeMind's mirror checks.
Not new toolkits: reheating/N* matching stays inside Janus (J7c2/J8 machinery); Janus-LT stays as is (BAO/SN/CMB/growth/σ8 validated, D1041–D1134).
Order: KALUZA first (biggest gap, pieces already validated), LOCKBENCH packaging alongside, JANUS-MF after MultiModeCode is installed on the PC.
