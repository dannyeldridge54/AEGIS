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

## DEVIATION (written before any code was run)
r_s(z*) and r_d are taken from CAMB, as a function of the early-universe parameters (ω_b, early ω_c, N_eff, Σm_ν), instead of a home-made sound-horizon integral. The reason: CAMB's exact recombination differs by ~1–2% from Eisenstein–Hu fitting formulas, which would fail G0.

The coupling's effect before recombination is negligible, because ρ_c ∝ e^{bΔφ} with Δφ ≈ 0 before z*. **That assumption is itself reported** as a dial: Δφ(z*).

The late universe (H(z), D_M) comes from the coupled solver. H0 is derived: the knobs are ω_b, ω_c, V̂_L and u_i, with V̂_L fitted in place of H0, so no shooting is needed. The ΛCDM reference is b = 0, u_i = 1e-4, with the same fixed n_s (an M5-type control).

## ADDENDUM (referee K-1…K-6 and the tandem pass), written before any output was read. The gate crashed on a bracket error with no numbers.

1. **Sign convention.** The thread rolls to smaller φ (φ̇ < 0). So b > 0 means DM loses mass (energy flows DM → DE), and b < 0 means DM gains mass.
2. **Adoption window: |b| ≤ 0.05.** Larger |b| gives matter-era early dark energy (Ω_φ ≈ 2b²/3), where the compressed priors are invalid and full CMB bounds apply. Those points are reported only, as "full-CMB required; not adoptable".
3. **G0 tightened.**
   - ℓ_A ≤ 0.01% and R ≤ 0.1%, both via D_M(z*) against CAMB at b = 0;
   - DESI distances and H(z) ≤ 0.15%.
4. **Adoption threshold:** Δχ² ≤ −4 relative to b = 0, on at least 2 of the 3 SN sets, with no set worse by more than +1 and the S₈ proxy ≤ 0.83.
5. **New dials:**
   - early Ω_φ at z*;
   - the total field excursion Δφ (a = 1e-6 → today);
   - the α leak Δα/α = ζ_α·|Δφ| with ζ_α = 3.8e-10 (D1887), against a conservative 1e-6;
   - the DM mass change since a = 1e-6 (freeze-out for 12.8 GeV is earlier, but the coupling only acts in the matter era);
   - ω_c(z*).

   **Birefringence** comes from the photon-axion on its own cycle (D1793), not from the thread, so it does not move. This is stated as a model fact, which the referee may contest.
6. **Apparent crossing:** two definitions, with DM anchored today and anchored at z*. Both are reported and **not** used for adoption.
7. **Code DEVIATION (pre-output):** the bounds on ln V̂_L were wrong, (0, 1.5) where the true value is ≈ −1. They are corrected to (−3, 0.5), and the start values are set to −1.0.
