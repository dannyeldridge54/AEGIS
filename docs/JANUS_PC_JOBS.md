# Janus PC jobs — exact Mukhanov–Sasaki checks the cloud sandbox is too slow for

Written by the Janus derivation loop (D1426, 19 Nov 2026). Nothing here has been run. Each job needs its own PREREG
(+ .sha256) committed and pushed BEFORE it runs (templates below), then a D-note with the result, pass or fail.
Engine: `apps/aegis_studio/engine/tools/serapis_calc/ms.py` — `Background(V, dV, phi0)` then **`spectra(bg, Nstar, ic='ds')`**
(per-mode start + exact de Sitter initial state). Do **not** take α_s from `spectra_fast` (D1420/D1422: common-start
artefact). Cloud cost ≈ 40 s per spectra_fast call, more per-mode; the PC is faster.

## J1 — exact α_s at the band_e / audited-box corners (tests the A1-anchored ρ meter where it was never run exactly)
- Points: SERAPIS-E full model (pipeline.predict path, as A1/D1262) at C ∈ {1.0, 1.3}e-6 × T_R ∈ {5.46e8, 1.65e10} GeV, MSSM g*.
- Compare: α_s(exact) vs 1.0352 × (−p²r/4) at each corner's own (n_s, r).
- Rule: PASS if all four agree within 0.5 % (D1423 found ≤ 0.25 % at the box ends using D1262's values).
- PREREG template: `PREREG_D###_rho_meter_corners.md` — model path, the four points, `ic='ds'`, the 0.5 % rule.

## J2 — D1415's asymptotic offset model, exact MS, solved to A1's (n_s, r)
- Model: V = (1 − 1/E₁)(1 + C(E₁ − 1)), E₁ = 2ζ(4)y² − 4.7833 + πζ(3)/y, y = e^{√2φ} (no tuning of B or D).
- Solve (C, φ*) by Newton (≤ 6 iterations) to n_s 0.974393, r 4.82095e-4; start C 1.255e-6, y* 14.818, φ0 = φ* + 0.3 (D1418 D1).
- Rule: PASS if α_s within 1 % of A1's exact −9.9814e-4 (the D1415 rule); also run B = D = 0 as control.
- Meaning: decides whether the ρ offset model is right (and D1415's +1.33 % was first-order slow-roll error) or not.

## J3 — spectra vs spectra_fast α_s at A1 (settles D1420/D1422)
- Same background as A1; three evaluations: spectra(ic='bd'), spectra(ic='ds'), spectra_fast.
- Report α_s from each; D1422's prediction: spectra_fast differs, the two per-mode results agree to < 1 %.
- Rule: "spectra_fast α_s unreliable" if it differs from per-mode ic='ds' by > 5 %; otherwise retire the D1422 rule.

## J4 — rerun the 12 reference rows with the D1417 α_s estimator (tightens D1444 / D1448; added by D1450)
- Why: the derived second-order models now match the exact references to ≤ 0.14 % (ρ, 7 rows) and ≤ 0.031 % (τ = i, 5 rows),
  but every reference predates D1417's estimator fix (A1 −9.9814e-4 vs new −9.964e-4, 0.17 %) — the comparison is now
  limited by the references, not the models.
- ρ rows (7): `field_tests/scripts/a1.py` path (pipeline.predict_fast → ms.spectra, per-mode, ic='bd') at the MSSM rows of
  `field_tests/results/a1_mssm_gstar.txt` (A1 + C ∈ {1.0, 1.15, 1.3}e-6 × T_R ∈ {5.455e8, 1.653e10}). Rerun with the current
  ms.spectra default (11-pt LSQ cubic, D1417) **and** ic='ds'; keep N* self-consistent as in a1.py.
- τ = i rows (5): `field_tests/scripts/na12/band_i_na12.py` (running_d632.py MS code; its own 5-pt finite-difference α_s).
  Rerun with the 11-pt LSQ-cubic estimator applied to the same PR(k) samples (dlnk −0.25…+0.25, step 0.05), ε 1.30–1.50e-4.
- Compare: D1442/D1443/D1444 ρ model and D1448 τ = i model predictions (scripts already in field_tests/scripts) at the new (n_s, r).
- Rule (lock in PREREG first): PASS if max |model/exact − 1| ≤ 0.1 % (ρ) and ≤ 0.05 % (τ = i); report shifts of the references.
- Cost estimate: 12 backgrounds + ~11 per-mode evaluations each; ~15–30 min on the PC (cloud: ~40 s/evaluation ⇒ too slow).
- Output: `field_tests/results/D###_J4_references.json` (old vs new n_s, r, α_s per row) → the loop writes the D-note.

## How to queue (for the C / PC-jobs track, when Danny says so)
Each job: copy the PREREG template, fill numbers, commit + push, then drop a `.job` in `AEGIS_PCJOBS\queue` the usual way
(`<name>|<timeout>|cmd …`). Results go to `field_tests/results/D###_*.json`; the loop writes the D-note.
