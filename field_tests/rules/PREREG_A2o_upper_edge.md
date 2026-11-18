# PREREG A2o — the upper edge of the post-hoc wino window: H.E.S.S. IGS line test at M = 1.25 and 1.5 TeV — locked 2026-11-18, before code or run
Goal: replace the estimated upper edge "~1–1.5 TeV" (D1153) with a computed one.
Method: the same as A2l/A2n, except for these mass-dependent pieces:
- **Line σv:** sommerfeld_nlo.wino_s_nlo(M, v = 1e-3, LO and NLO, off √2) with the same γγ + ½γZ factor and CONV as a2j.
- **NLL Sudakov:** the central R(M) from a2d_line_nll's Sig(M), formula unchanged. The band is the 1 TeV band ratios (0.794/0.709, 0.658/0.709) applied to R(M) (labelled assumption).
- **IGS limit at M:** log–log interpolation between the quoted 2.3e-28 at 1 TeV and 6.5e-28 at 2.9 TeV (2608.07234, D1124/D1126), labelled. This gives ≈ 2.3e-28·M^0.976.
- **f_pred(M):** serapis_inputs.wino_fraction(M).
- **Haloes:**
  - the H.E.S.S. benchmark Einasto (J/J_bench = 1);
  - the Gaia NFW central (A2j geometry: M200 0.55e12, c 13.9);
  - the 10 Singh–Desai shapes at ρ☉ = 0.40 (A2n).
Verdicts per halo and mass: PASS / BAND-DEP / FAIL as before.
Reported: the window's upper edge = the largest tested mass at which the Gaia/Singh–Desai haloes all PASS, and whether the benchmark passes.
Scored check (S1): at M = 1.0 the code must reproduce A2n's B0/D1 LO f_max lower edge 0.286 within 1%. Otherwise STOP.
