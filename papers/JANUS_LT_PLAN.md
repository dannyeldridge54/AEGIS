# Janus-LT: the late-universe twin of the Janus calculator (plan, 16 Nov 2026)
Goal: instant, validated late-universe cosmology for ANY expansion history — ΛCDM, w0–wa, early dark energy, SERAPIS's late branches, modified growth — with an exact Boltzmann code as the referee. Audience: everyone fitting SN, BAO, CMB-distance and growth data (far larger than the inflation community).
Pattern (same as Janus): fast physics-aware route + exact referee; every stage locked, two routes, D-note, Zenodo version.
## Fast route (what Janus-LT computes)
- Background: H(z) from any input — parameters (Ω_m, w0, wa, …), a function F(a) multiplying ΛCDM, or a user formula (sympy, like Janus J1); radiation + massive neutrinos included.
- Distances: D_M, D_H, D_A, D_L, D_V; SN distance modulus μ(z); BAO ratios D_M/r_d, D_H/r_d, D_V/r_d.
- Sound horizon r_d: exact integral of c_s/H up to the drag epoch (with the drag redshift from a fitting formula as route 1, the integral as route 2).
- CMB compressed: shift parameter R, acoustic scale l_A, ω_b (Planck/ACT-compressed likelihood).
- Growth: linear growth ODE → D(z), f(z), fσ8(z), σ8 (scale-independent for smooth DE; μ(a), Σ(a) hooks for modified gravity).
- Likelihoods: DESI DR2 BAO, Pantheon+/Union3/DES-Y5 SN, compressed CMB, RSD fσ8; χ² and fast fits.
## Exact referee
CAMB (pip wheel; CLASS as second referee if it builds): H(z), distances, r_d, σ8, fσ8 for the same cosmologies.
## Stages (track L)
L0 Background + distances + r_d for ΛCDM, w0–wa; locked validation vs CAMB on ≥ 50 cosmologies (targets: distances ≤ 1e-4, r_d ≤ 2e-4, R/l_A ≤ 1e-4 relative).
L1 Any expansion history: formula input, F(a) multipliers, EDE-like bumps; validation where CAMB can represent them (w(a) tables), self-consistency elsewhere.
L2 Growth: D, f, fσ8, σ8 vs CAMB (≤ 1e-3).
L3 Data: DESI DR2 / SN / CMB-compressed likelihoods; reproduce published ΛCDM and w0–wa best fits (locked comparison with the papers' numbers).
L4 Error bars per result (fast–exact gap, integration tolerance).
L5 Fits in seconds: full Bayesian sampling (emcee) of SERAPIS late branches (current model) on all data.
L6 SERAPIS late-universe predictions (current model, from the model map) applied: CMB distances, σ8, BAO, joint χ².
L7 Jaw-drop benchmark: speed and accuracy vs CAMB/CLASS across a standard grid, plus the expansion histories they cannot take directly (arbitrary F(a), formulas).
Release: Zenodo v1.0 after L0–L2 (GitHub repo janus-lt-calculator), versions per stage. Runs: heavy CAMB grids on the PC queue (COURSE.md rule 1).


Note (Danny, 17 Nov 00:30 CT): TorsionΛ is an old model — do not use it as a Janus-LT target or test case. D1025/D1028 TorsionΛ numbers are archival only.
- L6 DONE (D1041): Pantheon+ SN likelihood, Ω_m 0.3315 ± 0.018 (published 0.334 ± 0.018). Next: joint SN+BAO+CMB w0wa.
- L7 DONE (D1042): joint BAO+CMB+SN w0wa consistent with DESI Table V (0.3σ, 0.5σ). Next: full CMB distance prior or growth+SN.
- L9 prep (17 Nov, fetched arXiv html 2411.12021v5, DESI 2024 V Table 9 + App. A): ShapeFit fσ_s8/(fσ_s8)_fid per bin: BGS 0.80±0.20 (z 0.295), LRG1 1.09+0.12−0.14 (0.510),
  LRG2 1.05±0.12 (0.706), LRG3 0.96+0.11−0.10 (0.919), ELG2 0.95+0.11−0.08 (1.317), QSO 1.16±0.12 (1.491); raw means 0.3772, 0.5136, 0.4836, 0.4222, 0.3767, 0.4349
  (errors from App. A covariances, not yet fetched). Design issue before locking: Janus-LT has growth D(z), f(z) but NO transfer function/σ8 normalisation,
  so ratios vs the DESI fiducial need either (a) σ8 shape-independence assumption (state it), or (b) adding an Eisenstein–Hu transfer function (fetched) to get σ8.
  Do (b) first as its own locked validation (σ8 vs CAMB), then L9.
