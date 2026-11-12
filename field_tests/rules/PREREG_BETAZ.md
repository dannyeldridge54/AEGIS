# BETA(z): FLAG-1 with a coupling that changes over cosmic time

**Status: DRAFT**, written 12 Nov 2026 at Danny's request ("Can you go ahead and do that? Can you make that for ours?",
13:13 CT). It becomes LOCKED only on Danny's word; no fit under this rule runs before the lock, and none before
MISSING-PIECE M1 and M3 are scored. AI-assisted. Cloud.

**Why.** DATA-GEN, the DESI–SDSS comparison and published reconstructions (Li & Zhang 2025, arXiv:2506.18477;
arXiv:2506.22953) all point to the late-time expansion changing over 0.5 ≲ z ≲ 1.5, and a few DESI bins weigh heavily
(z ≈ 0.51 and 0.71; arXiv:2504.04417). FLAG-1 has one constant coupling β. This asks whether the data want β to change
with time, whether that shape is stable as DESI grows (DR1 → DR2 → DR3), and whether it predicts a held-out bin.

**Not blind.** Known at writing: the informal DESI–SDSS look of 12 Nov (DESI D_M short at z 0.7–1.3, SDSS long; both
D_H short at z 0.5–0.7); M2 (E_G: NO DISCRIMINATION); the literature above, including a sign-reversing coupling
reconstruction. M1's partial outputs exist on disk but their numbers were not read when this was written.

## Model (build `AxiCLASS_coupled_betabins`)
FLAG-1 (κ = 1, the same potential and closure), with the coupling piecewise constant in redshift:
β₁ (z < 0.5), β₂ (0.5 ≤ z < 1), β₃ (1 ≤ z < 2), β_early (z ≥ 2). The CDM mass follows d ln m_c = β(z) dφ, so energy is
conserved across bin edges. Each β ∈ [−0.15, 0.15] (a sign change is allowed).
- **Build gate (done before this draft):** with β₁ = β₂ = β₃ = β_early the build reproduces the original coupled build
  (r_d, 100θ*, D_M and H at z = 0.3–2.3) to better than 10⁻⁷ relative.
- **Limitation (stated):** background only. The perturbation equations still use β_early, so growth, E_G and
  lensing are not predicted by this model, and none is scored under this rule.

## Likelihood and fits
- Exactly the M1 / V1 real-data anchor: DESI BAO (ALL covariance), Pantheon+ (analytic M), compressed CMB vector,
  background-only. DR2 is primary; DR1 (`desi_2024_gaussian_bao_ALL_GCcomb`) for B2.
- Constant-β FLAG-1: as in M1 (β ∈ [0, 0.12]), refitted with this build. **Fit gate:** its DR2 χ² equals M1's
  full-data FLAG-1 χ² to within 0.05; if not, NO VERDICT on everything.
- β(z) model: parameters h, ω_b, ω_c, β_early, β₁, β₂, β₃. Nelder–Mead, best of 3 starts: (i) the constant-β best fit
  with all β equal to it; (ii) the same with β₁ − 0.03, β₃ + 0.03; (iii) with β₁ + 0.03, β₃ − 0.03. maxfev 4000.
- Errors on the β's from a finite-difference Hessian at the best fit (steps 0.005 in β, 1e-4 in h, ω).

## Readings
- **B1, does β change with time? (decides)** Δ = χ²(constant β) − χ²(β(z)), on DR2. Three extra parameters.
  - **TIME VARIATION NEEDED:** Δ ≥ 7.81 (p < 0.05 for χ²₃).
  - **NOT NEEDED:** otherwise. Reported either way: the β(z) shape with errors, and whether it changes sign.
- **B2, is the shape stable from DR1 to DR2?** The β(z) fit on DR1 and on DR2. For each of β₁, β₂, β₃:
  shift = |β_DR2 − β_DR1| / σ_DR1.
  - **STABLE:** every shift < 1. **WANDERS:** any shift > 2. **UNCLEAR:** otherwise.
  - Stated: DR2 contains DR1, so the two fits are correlated; B2 is a consistency check, not an independent test.
    DR3 will be added under the same procedure when public, as a reported extra.
- **B3, does it predict a held-out bin?** Both models refit on DR2 without the z = 0.706 bin (D_M and D_H); each
  predicts that bin; χ²_pred with its 2×2 covariance. Δ3 = χ²_pred(β(z)) − χ²_pred(constant).
  - **β(z) PREDICTS BETTER:** Δ3 ≤ −1. **WORSE:** Δ3 ≥ +1. **SAME:** otherwise.

## What may not happen
No change of bins, bounds, starts, data, thresholds or the held-out bin after any fit. No extra bins added to chase a
reading. Each reading is reported once. Counted +3 in V7.

## Code
`field_tests/missing_piece/betaz_build.py` (loads the build), `betaz_fit.py` (fits, Hessians, score). Results:
`field_tests/results/betaz.json`.
