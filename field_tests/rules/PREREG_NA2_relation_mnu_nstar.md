# PREREG NA2 — node audit phase 2: janus, mnu, nstar_e (arithmetic re-derivation)
Locked before any computation. Data: NA1's 12 PC scan rows (field_tests/results/na1_pc_scan_n001.json), already on disk.
## A. janus (Janus relation) — reproduce D689's stated offset
D689: for SERAPIS-E's E(τ,2) tilt the leading-order relation with (p, κ) = (2√2, 1) (tools/serapis_calc/pipeline.py) UNDERESTIMATES exact α_s by 13–16%.
Test: at all 12 NA1 rows, deficit = 1 − α_rel/α_exact. PASS if every deficit lies in [12%, 17%]. Also reported (no verdict): the κ = ½ value (D669 wording "SERAPIS is (2√2, 1/2)").
## B. mnu — Σm_ν = 0.0587 eV from oscillation data
Fetch NuFIT 6.0 (nu-fit.org) normal-ordering best fits Δm²21, Δm²3l. With m1 = 0: Σ = √Δm²21 + √Δm²31.
PASS if |Σ − 0.0587| ≤ 0.0005 eV. Also recompute the D-note margin vs DESI DR2+CMB 0.0642 (stated 5.5 meV) and vs 0.053 (stated 5.7 meV), tolerance 0.3 meV.
## C. nstar_e — N* = 49.7–50.5 at T_R = 3e8–3e9 GeV (D725)
Self-consistent N* with tools/serapis_calc/nstar.py (g = 106.75, k = 0.05), exact background (Janus core, C = 1.15e-6), exact ε_H = 1 end
(V*/V_end from the background), r from spectra3 at that N*; iterate to |ΔN| < 1e-3. T_R = 3e8, 3e9.
PASS if both lie within 0.05 of 49.7 and 50.5. If FAIL, report the corrected window (no change to frozen predictions: post-hoc rule).
Information only (no verdict): same at T_R = 1e5, 1e6 GeV (D781's T₂ window, mentioned in D-notes as the later reheating chain).
## Rules
No reruns to chase results; any fix via PREREG_NA2_DEVIATIONS.md written first. Results: field_tests/results/na2_relation_mnu_nstar.txt.
