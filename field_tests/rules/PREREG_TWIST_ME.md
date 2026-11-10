# TWIST-ME: the flagship plus a heavier (or lighter) electron before recombination

**Status: LOCKED** on Danny's word ("Go ahead and test", 10 Nov 2026, 08:17 CT), right after the literature review
below was reported to him. AI-assisted. No TWIST-ME fit exists at lock.

**Not blind, stated plainly.** Known at writing:
- The literature: with Planck + ACT DR6 + DESI DR2 + SN, a constant m_e/m_e0 before recombination is mildly preferred.
  Seto et al., arXiv 2508.09025: 1.0078 ± 0.0047, Δχ² −7.3, H0 69.4 ± 0.7 under ΛCDM. arXiv 2508.19081: H0 69.6–70.5.
- Our results: FLAG-1 beats ΛCDM+S8 by 4.71 / 6.01 / 7.69 with H0 ≈ 67.0–67.4. The two-field test (early n = 3 field)
  was NOT WORTH IT and H0 did not rise.
- Cloud check before lock (only the engine runs, no fit): with m_e = 1.01 at the FLAG-1 point and no refit, H0 = 69.2.

**Why the Twist.** A dilaton that couples to matter is the textbook way for "constants" such as m_e or α to differ in the
early universe. Here m_e is a free number before z = 50 and the standard value after. That step is a phenomenological
stand-in. It is not derived from the flagship's dilaton, which barely moves before recombination. Any derivation would
also have to face the tight late-time limits on varying constants (quasars, clocks, equivalence-principle tests). Both
points are stated in the write-up.

## Question
Does letting the early electron mass float raise H0 while keeping, or improving, the flagship's fit to CMB + BAO + SN + S8?
Does it pay for its one extra parameter?

## Model and engine (fixed)
- **FLAG-1 exactly** (`PREREG_FLAGSHIP.md`: S8-J setup, κ = 1, β_eff free, DES Y6 S8 term, CMB + DESI DR2 + one SN set,
  same priors, best of 4), on the same build (`AxiCLASS_coupled_nlfix`, CLASS v3.3).
- **Plus `varying_me` ∈ [0.9, 1.1]**: CLASS's built-in `varying_fundamental_constants = instantaneous`. m_e/m_e0 =
  varying_me for z > 50 and 1 after. α is fixed to 1; the transition redshift is fixed at 50 (CLASS default, as in the
  literature). Start: 1.0, ref width 0.005; the other parameters start at the FLAG-1 best fit.
- Runs `ME`, `ME_dovekie`, `ME_union3` (3 fits, PC). Code: `cmb-fit/axiclass/varme/me_fit.py`.

## Gate
- **G-ME-PC (before any fit):** with varying_me = 1 (switch on), at each FLAG-1 best fit, total χ² must equal the stored
  FLAG-1 χ² within **0.05**. Cloud check: switch on with m_e = 1 is identical to switch off on every term the cloud can
  run. If the gate fails: no fits.

## Readings (per SN set; 2 of 3 decides)
- **vs FLAG-1:** Δ_F = χ²(ME) − χ²(FLAG-1 recomputed at its stored point, the G-ME-PC value).
  - **ELECTRON MASS EARNS ITS PLACE** if Δ_F ≤ −4.
  - **NOT WORTH IT** if Δ_F > −2.
  - Otherwise **WEAK**.
- **vs ΛCDM+S8** (stored `ax_spa_lcdm_halofit{...}_s8y6`, the lower of the two restarts, as for FLAG-1): Δ ≤ −4 is
  **SURVIVES**.
- **H0** (reported, not a verdict): "H0 RISES" only if it is ≥ 1.0 km/s/Mpc above FLAG-1's stored H0 on 2 of 3 sets.
  H0 is also reported next to CCHP/JWST (≈ 70.0 ± 1.5) and SH0ES (≈ 73).
- **Reported, not verdicts:** m_e/m_e0 with its distance from 1, β_eff, and S8.
- **Lensing cost:** afterwards the locked DES Y3 and KiDS-Legacy full-shear tests (LATE-BASE method, same ΛCDM partners)
  are rerun at the ME best fits and reported.

## What may not happen
No change of priors, data, ranges or thresholds after any result. Failed fits are NO VERDICT for that set. No rerun to
chase a reading. No α-plus-m_e follow-up under this rule (that would need a new rule). Counted +1 in V7.

## PC time
Each step takes about as long as FLAG-1 (same build, one more parameter): 3 fits × best of 4 ≈ 4–12 h.
