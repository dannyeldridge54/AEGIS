# DRAFT pre-registration UB-2: the unified BI axion–dilaton against data

**Status: DRAFT, not locked, no hash.** Written 7 Nov 2026 with AI assistance at Danny's request. It is locked only if
**UB-1 passes** (`PREREG_UNIFY_BG.md`), and only after the code passes the gates below. No UB-2 number exists yet.
If UB-1 fails, this draft is marked WITHDRAWN and kept.

## Question
Can **one** BI axion–dilaton (fixed λ = −2√(2/3), F = F_P/|φ|, F_P = 1.559, n = 3, no cosmological constant) fit the
data as well as the two separate pieces we have now (the Locked Twist early, the Spiral late) and better than ΛCDM?

## Model (fixed when locked)
- Exactly the UB-1 model, in the variant(s) UB-1 passed (A: derived GKY potential; B: exponential, κ free).
- Free beyond the standard six (A is set by flatness, replacing Λ): ln L, θ_i, |φ|_i, plus κ for variant B.
  **3 extra parameters (A) or 4 (B)**, against 2 for w0–wa.
- Prior box: the UB-1 box, cut to the region where UB-1 found R2–R5 met (UB-1 used no data, so this is allowed).

## Engine (fixed when locked)
- CAMB 2.0.5 + Cobaya 3.6.2 on the PC (venv312), as for the Locked Twist fits. For each parameter point the two-field
  background is solved (`theory/unify_hyperbolic_bg.py` equations, with the sampled Ω_m, ω_r and H0), and the field's
  w(a) is passed to CAMB as one dark-energy fluid (`DarkEnergyFluid`, w(a) table, rest-frame sound speed 1).
- This is an **approximation**: it ignores the oscillating angle's scale-dependent sound speed and the two-field
  entropy mode. The gates below decide whether it is good enough. If not, UB-2 waits for a full two-field module.

## Gates (code checks, must pass before any UB-2 fit; no UB-2 data fit is involved)
- **G1 early:** the fluid route applied to the stored Locked Twist best fit (`cmp_edelockP.json`) reproduces the full
  EarlyQuintessence χ² within 1.0.
- **G2 ΛCDM limit:** with L → 0 and a flat potential, the χ² is within 1.0 of the stored ΛCDM fit on the same data.
- **G3 background:** CAMB's H(z) for a UB-1 passing point matches the stand-alone solver to 10⁻⁴.

## Data (fixed when locked)
The SF data, so results line up with the Spiral: CMB (Planck low-ℓ, ACT DR6 + Planck cut, ACT lensing, SPT-3G D1) +
DESI DR2 BAO + one supernova set: Pantheon+, DES-Dovekie, Union3 (DES Y5 excluded, as in SF). Best of 4 restarts.

## Verdicts (per supernova set; same thresholds as SF)
- **Against ΛCDM:** BEATS if Δχ² ≤ −4 on at least 2 of 3; TIE if none ≤ −4 and none ≥ +2; otherwise MIXED.
- **Against w0–wa:** BEATS if Δχ² ≤ −2 on at least 2 of 3; COMPETITIVE if ≤ +2 on at least 2 of 3; otherwise NOT
  COMPETITIVE. Reported with the parameter counts (3 or 4 vs 2) and ΔAIC beside it.
- **Unification check (the point of the test):** compare with the two-piece result (Locked Twist early + Spiral late,
  stored fits). **UNIFIES** if the single field is within +2 of the better stored piece on at least 2 of 3 sets
  while using fewer free parameters than the two pieces together; otherwise **DOES NOT UNIFY**.
- **Also reported, not verdicts:** S8 (DES Y6 penalty as in S8-WL Part 1), f_peak, z_peak, w0, |φ| today.
- **Failures:** a failed or non-finite fit is NO VERDICT for that set; any setting change is logged first.

## Choices for Danny before locking
1. Data: the SF set above (recommended), or add the fair Planck + DESI + Pantheon+ set used for the Locked Twist.
2. Accept the fluid approximation if G1–G3 pass, or wait for a full two-field Boltzmann module (much more work).
3. Keep the SF thresholds (recommended, so the verdicts compare directly).
