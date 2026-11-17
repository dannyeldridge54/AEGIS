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
