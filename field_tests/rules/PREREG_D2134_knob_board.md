# PREREG D2134: the "knob board". The builder turns the knobs, the referee watches every dial (Danny 18:47). One locked scan of the ONE folding change: a thread–dark-matter coupling b. Locked before computing.

**Knobs:**
- **b** (the coupling), on the grid {−0.15, −0.10, −0.075, −0.05, −0.025, 0, +0.025, +0.05, +0.10};
- **u_i** (the thread amplitude), profiled on [0.005, 0.21] (below the u_i ≈ 0.22 collapse edge, D2133).

**Physics** (units 8πG = 1; the standard coupled quintessence of Amendola 2000):
- ρ̇_c = −3Hρ_c + b φ̇ ρ_c and φ̈ + 3Hφ̇ + V′ = −b ρ_c.
- V = V_L(1 − A e^{−βφ}), with A = 16ζ(2)/(3ζ(3)) and β = 2√2. The field is frozen at a = 1e-6 (coupling on throughout), with A e^{−βφ_i} = u_i. V_L comes from flatness.
- Baryons, photons and ν are standard, with N_eff = 3.044 and Σm_ν = 0.0587 eV treated as matter at late times (background).
- r_s(z*) and r_d are computed in the same code from the sound speed, with z* from Hu–Sugiyama and z_d from Eisenstein–Hu.

**Gate G0:** at b = 0 and u_i = 0.13, R, ℓ_A, r_d and the DESI distances must agree with CAMB (D2130 engine) within 0.15%. If G0 fails, nothing is used.

**Data:**
- the CHW compressed CMB (4-parameter), with n_s fixed at 0.9706;
- DESI DR2 (shipped mean and covariance);
- SN, one set per fit, each with analytic M marginalisation: **DES-Dovekie** (shipped inverse covariance), Pantheon+ (zHD > 0.01, STAT+SYS covariance) and Union3 (22 bins, shipped covariance).

ω_b, ω_c (the early value) and H0 are fitted (Nelder–Mead) at each knob point.

**Dials, reported for every b:**
- χ² by block, and Δχ² vs ΛCDM on the same data;
- H0, today's Ω_m, and the DM mass change since z*;
- the apparent w_eff(z) seen by an uncoupled-DM observer, ρ_DE,eff = ρ_φ + ρ_c − ρ_c0 a⁻³; whether it crosses −1 for 0.3 < z < 2; and its CPL (w0, wa) over z < 2;
- an **S₈ proxy**: linear growth with the coupling (G_eff = G(1 + 2b²) for DM, plus the drag term), normalised to ΛCDM at z = 50, ×0.811·√(Ω_m/0.3). This is an ESTIMATE.

**Scored items untouched by construction:** the coupling acts only between DM and DE. n_s, r, ΔN_eff, BBN, Σm_ν, the proton, the α-drift and the leptons are therefore unchanged. The referee verifies this.

**Verdict:**
- The **one change is ADOPTED** only if a single b, the same for all three SN sets within ±0.025, improves χ² over b = 0 by ≥ 2 on at least 2 of the 3 SN sets, does not worsen any set by > 1, and keeps the S₈ proxy ≤ 0.83.
- Otherwise it is **REJECTED**, and the Weave stays at b = 0.
