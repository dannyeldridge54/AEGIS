# PREREG D1989: the complete field (Danny 19:19). Locked at this commit, before any of it is built or run.
Everything carries over from D1986/D1987 (goalposts, engine v3 detectors, bars A1–A5, the held-out discipline), except the changes below. **Earlier verdicts stand**, including D1987's FAIL on A5.

## P1 Tooling fixes (owed items)
1. **Scorer.** A live PRED whose value depends on a knob in fits_spent is labelled **PASS (FIT)**, never PASS. The dependence map:
   | goalpost | knobs |
   |---|---|
   | as | m32, split |
   | M2 | m32 |
   | Y | TR, MN |
   | Om | TR, m32 |
   | ns | TR |
   | u, rung | u |
   | MN | MN |
2. **Controller.** A 1 s window counts as quiet only if it lies **entirely** inside a quiet window.
3. **STUCK rule.** A layer whose balancing step is clipped to zero by a bound on every needed knob, for 1 s continuously, becomes **STUCK**. It stops balancing, is reported, and is not RESONANT. Bounds no longer let a balancer hug them.
4. **Physical bounds** replace the arbitrary ±ln 3:
   - T_R ∈ [T_BBN = 5e-3 GeV, m_φ];
   - M_N inside the L2 window [4.5e10, 2.5e12];
   - u inside the quark window (and held by L1);
   - m₃/₂ and split keep ±ln 3, labelled *naturalness bounds*.

   Every knob more than 1 % off its derived value is still a FIT.
5. **KNOBS_OF correction** in resonance.py: L4 → [] (true response 0); L8 → ['TR', 'MN', 'm32'].
6. **Kink-aware R2** in lensing: probes ±1e-3. A layer whose linear fit has R² < 0.99 is flagged KINK, and R1 decides it.
7. **Determinism:** two consecutive loomd pulses on unchanged inputs must give an identical state, and the second must be NULL. Run for real.
8. **PASS-label check (C8):** no goalpost in a scored result may read "PASS" when its kind is FIT or when it depends on a spent fit. Automated, and run in every pulse.

## P2 Real-data replay (instead of synthetic events)
A 70 s run where the data streams step through the **actual published history** at fixed times. Noise is at each release's σ, and the order is fixed.
- **n_s:**
  - WMAP9 0.9608 ± 0.0080;
  - Planck 2013 0.9603 ± 0.0073;
  - Planck 2015 0.9655 ± 0.0062;
  - Planck 2018 0.9649 ± 0.0042;
  - P-ACT 2025 0.9743 ± 0.0034;
  - CMB-SPA 0.9684 ± 0.0030;
  - SPA + DESI 0.9728 ± 0.0027.
- **α_s (PDG editions):** 2012 0.1184 ± 0.0007; 2014 0.1185 ± 0.0006; 2016 0.1181 ± 0.0011; 2018 0.1181 ± 0.0011; 2020 0.1179 ± 0.0010; 2022 0.1179 ± 0.0009; 2024 0.1180 ± 0.0009.
- **Wino disappearing-track limit:** ATLAS 2017 460 GeV; ATLAS 2022 660 GeV; ATLAS + CMS 2025 700 GeV (σ 20 for the stream).
- **Y_B:** WMAP9 0.88e-10; Planck 0.87e-10.
- Each n_s and α_s release lasts 10 s (7 releases = 70 s). The wino releases fall at 0, 25 and 50 s; Y_B at 0 and 30 s.

These values are recalled from the PDG and collaboration papers, not re-fetched in this session; that is stated.

**Locked expectation:** a release is **detectable** if |Δ central| / σ_new ≥ 1. Score: detected-when-detectable (recall) and no detection when |Δ|/σ_new < 0.25 (specificity).
- The goalpost status timeline is reported per release.
- The wino must flip to FAIL at the 700 GeV release unless m₃/₂ has been fitted. If it has, the label is PASS (FIT).

## P3 Derivation tests (no new fit)
**C1 The cube axis.** The hypothesis H_Imτ: a sector's rung step = e^{−9π/8} × (Im τ_knot / Im i).
- **POST-HOC.** It was noticed before this lock: the leptons at ρ give 0.0292 × √3/2 = 0.02527 against the lepton slip 0.0253.
- The numerology guard (check.py C4) is applied to that in-sample match. The lepton slip's natural range is 0.0066–0.0435 (D1877), so the in-sample match carries **no evidential weight by itself**.
- **Out-of-sample test (the only one that counts): the quarks.**
  - The prediction for τ_q ∈ {ρ, i} is 0.02527 or 0.02918 against the one-spurion window [0.02588, 0.02740].
  - **PASS** if either lies inside the window. **FAIL** if neither does.
- If PASS, the cube's consistency check becomes rung/Im τ, and L4 is re-scored. If FAIL, L4 stays NO LOCK / OPAQUE, and H_Imτ is recorded as an unsupported coincidence.

**C2 The baryogenesis feasibility scan.** Within the physical bounds, with M_N held by L2 (inside-out) and no new knob: find the set of T_R where Y_B ≥ 0.87e-10 **and** Ω_wino h² ≤ 0.12 **and** n_s within 2σ.
- Report T_R_min and the fit factor T_R / T_R(derived).
- That T_R is a FIT unless derived.
- The verdict is FEASIBLE-BY-FIT or INFEASIBLE.

## P4 Self-driving (loomd auto)
`python3 tools/loom/loomd.py auto [--pulses N] [--field-seconds S]`. Each pulse runs unattended:
1. the core (self-test, still point, resonance, lensing, compass, review, centre brief);
2. a woven-field scored run of S seconds (default 20) with seed = 2026 + round;
3. the battery without mutation;
4. the PASS-label check;
5. online FDR over the band-goalpost tension p-values;
6. the planner;
7. a human-readable report, field_tests/loom/reports/round_NNN.md.

It stops at the endpoint, or at a **STALL** of 7 null pulses. A STALL is reported, never treated as the endpoint.

**Acceptance:** 3 unattended pulses run without error and each writes a round file and a report; the determinism test (P1.7) passes; and a STALL is declared correctly in a test mode with a forced null streak.

## P5 The final sequence
1. Run the woven-field scored run under the new bounds on **seed 2027**, which has never been used. Bars A1–A5 as locked.
2. Run the real-data replay (P2).
3. Run the derivation tests (P3).
4. Then the Loom pattern: `loomd auto` pulses, triangulating each pulse, until a 7-null STALL or the endpoint.

**Expected (stated now):**
- A5 PASSes under physical bounds. The balancer moves T_R to about 1.5e9 (a FIT, about ×4) for leptogenesis.
- C1 FAILs out-of-sample: neither 0.02527 nor 0.02918 is in [0.02588, 0.02740].
- The pulses stall without reaching the endpoint.
