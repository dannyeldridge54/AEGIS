# PREREG_CERN1_ATLAS137 (D1723 planned) — re-anchor CERN+1's disappearing-track recast on ATLAS arXiv:2603.08315
Locked 19 Nov 2026 22:05 CT, before any number from the paper's tables is read into code.
Method: same benchmark-anchored scaling as SEARCHES['ATLAS_136'] (recast_dt.py), new entry 'ATLAS_137' with the paper's own
signal yield at one benchmark wino mass (n_bench, m_bench), luminosity 137 fb⁻¹, and its model-independent 95% CL visible-cross-section
limit for the signal region used for the electroweak interpretation (n95 = σ_vis,95 × L). Lifetime from lifetime.py (SM Δm), bg = 0.5 as before.
Inputs are taken from the paper text/tables only; if the paper does not quote n_bench or σ_vis,95 explicitly, STOP and record NULL (no tuning).
Pass rule: recast observed limit within ±20 GeV of the paper's 670 GeV (SM Δm interpretation). Report also the expected limit using
the paper's expected σ_vis (if quoted) vs 770 GeV (reported, not a pass condition).
On PASS: ATLAS_137 becomes the default search for limit/hl_lhc; ATLAS_136 and ATLAS_36 stay as validated references.
