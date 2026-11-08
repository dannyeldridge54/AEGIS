# DRAFT pre-registration UB-2: the unified BI axion–dilaton against data

**Status: DRAFT, not locked, no hash.** Written 7 Nov 2026 with AI assistance at Danny's request. It is locked only if
**UB-1 passes** (`PREREG_UNIFY_BG.md`), and only after the code passes the gates below. No UB-2 number exists yet.
If UB-1 fails, this draft is marked WITHDRAWN and kept.

## Question
Can **one** BI axion–dilaton (fixed λ = −2√(2/3), F = F_P/|φ|, F_P = 1.559, n = 3, no cosmological constant) fit the
data as well as the two separate pieces we have now (the Locked Twist early, the Spiral late) and better than ΛCDM?

## Model (fixed when locked)
- Exactly the UB-1 model, in the variant(s) that passed: B (exponential, κ free; UB-1 D1) and, if UB-1b passes, C
  (derived potential with W = W0 e^{bΦ}, b free).
- Free beyond the standard six (A is set by flatness, replacing Λ): ln L, θ_i, |φ|_i, plus κ for variant B.
  **3 extra parameters (A) or 4 (B)**, against 2 for w0–wa.
- Prior box: the UB-1 box, cut to the region where UB-1 found R2–R5 met (UB-1 used no data, so this is allowed).

## Engine (fixed when locked) — code ready: `cmb-fit/ub2_fit.py` + `cmb-fit/ub2_camb/`
- CAMB 2.0.5 rebuilt with a **two-field dark-energy module** (`ub2_camb/DarkEnergyUBField.f90`, built by
  `ub2_camb/build_ub2_camb.sh`) + Cobaya 3.6.2. For each parameter point CAMB's own background gives every non-field
  density; the two-field background (`theory/unify_hyperbolic_bg_ub1b.py` equations, DOP853, = UB-1 D1 + variant C) is
  solved on it with A fixed by flatness, and passed to the module, which evolves **both fields' perturbations** in
  synchronous gauge (no fluid or PPF approximation). H0 is sampled directly.
- Tested 7 Nov before any gate or fit: with λ = 0 the module reproduces CAMB's own EarlyQuintessence at the Locked
  Twist best fit to 2×10⁻⁵ in TT/EE (ℓ 2–2500) and 2×10⁻¹¹ in H(z) (`ub2_camb/validate_single_field.py`); with the full
  two-field background H(z) matches the stand-alone solver to ≤ 10⁻⁶. The earlier fluid route (low-ℓ TT ×50) and PPF
  route (2.5% TT) are dropped.
- Building it on the PC needs gfortran (WSL micromamba env: `micromamba install -c conda-forge gfortran`).

## Gates (code checks, must pass before any UB-2 fit; no UB-2 data fit is involved)
- **G1 early:** the module in its λ = 0 limit, at the stored Locked Twist best fit (`cmp_edelockP.json`), reproduces
  the full EarlyQuintessence χ² within 1.0.
- **G2 ΛCDM limit:** with L → 0 and a flat potential, the χ² is within 1.0 of the stored ΛCDM fit on the same data.
- **G3 background:** CAMB's H(z) with the UB fluid matches the stand-alone solver to 10⁻³ (z = 0–3000).
- Run: `python ub2_fit.py gates` → `results/ub2_gates.json`. The fit command refuses to run until this rule is locked.

## Data (fixed when locked)
Planck 2018 (low-ℓ TT/EE, plik-lite TTTEEE, lensing) + DESI DR2 BAO + one supernova set: Pantheon+, DES-Dovekie, Union3
(DES Y5 excluded). This is the CAMB data set of the stored `lcdmP`, `edelockP` (+ `_dovekie`, `_union3`) fits, so the
ΛCDM and Locked Twist references need no new runs and the engine is the same. New references: `w0waP` on each set
(3 CAMB fits). Best of 4 restarts.

## Verdicts (per supernova set; same thresholds as SF)
- **Against ΛCDM:** BEATS if Δχ² ≤ −4 on at least 2 of 3; TIE if none ≤ −4 and none ≥ +2; otherwise MIXED.
- **Against w0–wa:** BEATS if Δχ² ≤ −2 on at least 2 of 3; COMPETITIVE if ≤ +2 on at least 2 of 3; otherwise NOT
  COMPETITIVE. Reported with the parameter counts (3 or 4 vs 2) and ΔAIC beside it.
- **Unification check (the point of the test):** compare Δχ² vs ΛCDM (same engine and data) with the stored pieces:
  the Locked Twist (`edelockP*`, same engine) and the Spiral (SF, AxiCLASS, its own ΛCDM reference). **UNIFIES** if the single field is within +2 of the better stored piece on at least 2 of 3 sets
  while using fewer free parameters than the two pieces together; otherwise **DOES NOT UNIFY**.
- **Also reported, not verdicts:** S8 (DES Y6 penalty as in S8-WL Part 1), f_peak, z_peak, w0, |φ| today.
- **Failures:** a failed or non-finite fit is NO VERDICT for that set; any setting change is logged first.

## Choices for Danny before locking
1. Data: the Planck 2018 + DESI + SN set above (recommended: same engine as the stored references), or also the
   ACT/SPT combined CMB (needs new CAMB references, ~6 more fits).
2. Accept the fluid approximation if G1–G3 pass, or wait for a full two-field Boltzmann module (much more work).
3. Keep the SF thresholds (recommended, so the verdicts compare directly).
4. Fit variant(s): only those UB-1 passed (the D1 run counts; see `UB1_DEVIATIONS.md`).
