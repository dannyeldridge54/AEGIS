# PREREG A2l — 1 TeV wino vs H.E.S.S. IGS for the cored (Burkert) Gaia DR3 haloes of Singh & Desai — locked 2026-11-17, before any code or run
Source: arXiv:2605.16994v1, Table A1 (median values), Burkert ρ0 [1e7 M☉ kpc⁻³] and r_c [kpc], baryon model B0, datasets D1–D4:
- (28.96, 3.37), (22.05, 3.79), (44.08, 2.91), (42.59, 2.87).
- Also B1 / D2 (15.24, 4.13) as the most diffuse variant.
Profile: Burkert, ρ = ρ0 r_c³/((r + r_c)(r² + r_c²)) (jfactor.burkert shape), normalised by its own value at R0 = 8.178 kpc. Units via astropy (as in A2j).
- Einasto is NOT used: the paper's ρ0/r_c/α convention is unverified (labelled).
- NFW rows are not used: the extraction flagged them as partly garbled.
Method: identical to theory/wiring/a2j_gaia_halo.py.
- J in the IGS annuli 0.5–3.0° / J_bench.
- 1 TeV line σv, LO and NLO, NLL band factors (0.794, 0.658), limit 2.3e-28.
- f_max = sqrt(limit/(σv·R·J/J_bench)).
Prediction (single source, serapis_inputs.wino_fraction(1.0)): thermal f bracket [0.124, 0.205] (D1152/D1153). The stale f = 0.26 of A2j is NOT used.
Verdict per halo:
- PASS if f_max(lower band edge) ≥ 0.205;
- FAIL if f_max(upper band edge) < 0.124;
- otherwise BAND-DEPENDENT.
Also reported: ρ☉ of each halo. Script field_tests/scripts/a2l_burkert_J.py (written after this lock).
