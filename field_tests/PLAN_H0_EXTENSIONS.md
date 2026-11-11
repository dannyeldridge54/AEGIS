# Plan: extending the Twist's equation toward the H0 gap (10 Nov 2026)

AI-assisted. Every fit-based step runs under its own locked rule (lock on Danny's word); each rule fixes its bars before
any run. Cheap feasibility checks come first, so a dead idea costs minutes, not PC days.

**Where we start.** FLAG-1 beats ΛCDM+S8 by 4.7 / 6.0 / 7.7, with H0 ≈ 67.1. Two add-ons did not pay: TWOFIELD (early
field) and TWIST-ME (early electron mass). Across the literature, every surviving idea tops out at H0 ≈ 69–70.5 without
the SH0ES calibration. The JWST/CCHP local value is 70 ± 2; Cepheids alone give 71.1 ± 1.4. **The realistic target is
H0 ≈ 69–70, not 73.**

**Current equation.** gravity (GR) + dilaton φ with potential V(φ) + CDM coupled to φ (β) + baryons/photons uncoupled.

## Phase 0 — feasibility, cloud (done / minutes)
| # | Add-on | Check | Result |
|---|---|---|---|
| 0a | Universal coupling g: m_e ∝ e^{gφ} (axiodilaton-style, arXiv 2512.13544) | Flagship φ(z) through the constants check (`field_tests/dilaton_me/phi_history.json`) | **Ruled out for our field.** φ moves 0.121 between recombination and today but 0.208 since z = 0.89. Any g that shifts m_e enough at recombination breaks quasars by about 10⁵ and clocks by about 10⁴. A quadratic (least-coupling) form fails the same way. The axiodilaton paper's tracker history is different, and its authors also need screening. The Twist keeps its CDM-only coupling, and the write-up says why |
| 0b | ΔN_eff (dark radiation) + running α_s | Engine runs with the flagship (cloud) | **Works.** At the FLAG-1 point with ΔN_eff = 0.3, before refit: H0 70.2, σ8 0.794, r_d 145.95 |
| 0c | Decaying CDM fraction → dark radiation (arXiv 2605.26050) | Engine runs with the flagship | **Engineering needed.** CLASS's dcdm shooting clashes with the dilaton's closure shooting (shooting failed). About half a day to make both close; only worth it if Phase 1 shows promise |
| 0d | Dilaton coupled to gravity, F(φ)R (scalar-tensor; arXiv 2511.04610) | Is a modified-gravity engine available? | Not in our build. Needs hi_class merged with the coupled dilaton: 2–4 days. First a background + growth feasibility study against lunar-ranging and Cassini bounds (a "gravity check", like the constants check) |

## Phase 1 — TWIST-DR (PC fits about 1 day; rule `PREREG_TWIST_DR.md`, drafted)
FLAG-1 + free ΔN_eff (free-streaming dark radiation) + running α_s. Gate, then 3 fits; full-shear rerun reported.
Literature ceiling: H0 ≈ 70 (with interacting DR and running). ACT's own analysis disfavours ΔN_eff > 0.

## Phase 2 — TWIST-DCDM (only if Phase 1 reads WEAK or better, or Danny asks)
Fix the dcdm + dilaton closure (0c), then FLAG-1 + decaying CDM fraction + its rate.

## Phase 3 — TWIST-G (only after a positive feasibility study)
Scalar-tensor dilaton: G_eff bump near z ≈ 2 that returns to GR today. Gravity check against Ġ/G (lunar ranging,
≲ 1e-13/yr) and Cassini (|γ − 1| < 2.3e-5). Then the hi_class build and a pre-registered rule.

## Phase 4 — write-up
Flagship wins: fit, DESI apparent phantom crossing, 1.4σ from JWST H0. Clean "no" results: early field, early electron
mass, local void, universal coupling. Open: weak lensing, gap to SH0ES. Positioning against the axiodilaton paper:
same physics family, but the CDM-only coupling keeps the Twist on the side that passes laboratory tests.

## Already in the toolkit
Constants check, inverse distance ladder (SH0ES and JWST), local-void shells, DESI (w0, wa) mapping.

## Status update (10 Nov 2026, evening)
- **Phase 1 TWIST-DR:** NOT WORTH IT (2 of 3; the Pantheon+ fit died = NO VERDICT). ΔN_eff → 0, H0 unchanged.
- **Phase 3 feasibility, TWIST-G** (`field_tests/twist_g/toy_geff.py`, background-only toy, EXPLORATORY). The coupling is
  G_eff = 1 + A (φ − φ0)², a quadratic coupling about today's field, so G_eff = G0 today and Cassini and lunar ranging are
  met at first order. With the flagship's own φ(z) this gives a bump peaking near z ≈ 2, the same shape arXiv 2511.04610
  reconstructs.
  - DESI DR2 BAO + Pantheon+ (uncalibrated) + Planck distance priors: best A = 0.047 (δG/G 0.3% at z = 2), Δχ² −0.08,
    ΔH0 −0.01. That holds from three different starting points.
  - Forcing the paper-sized 8% bump (A = 1.5) costs Δχ² +71 and lowers H0 to 66.5. The opposite sign (A = −1.5) costs
    +97 for H0 67.3.
  - **Not worth the hi_class build:** the background alone already rejects it, and perturbations cannot rescue H0.
    The paper's H0 gain needs a free-form G(z) and the SH0ES-calibrated SNe.
- **Phase 2 TWIST-DCDM:** not pursued (Phase 1 was negative, and the literature evidence ties with ΛCDM).

## Data gaps list (10 Nov 2026, 21:10 CT): status
1. **Full shear at the FLAG-1 fits:** DES Y3 running in the cloud; KiDS-Legacy next (pairs added to both pipelines).
2. **Error bars:** FLAG-1 MCMC, 4 chains on the PC via the runner (started 21:06 CT; R−1 < 0.02 or 40k samples).
3. **Growth fσ8:** done, exploratory (`field_tests/growth_fs8/`). χ² 6.4–6.7 for 6 points vs ΛCDM 6.2: no distinction.
4. **Planck high-ℓ:** already in the fits. The CMB set is P-ACT (Planck PR3 lite, cut at ℓ < 1000 TT / 600 TE-EE, as
   ACT DR6 recommends) + ACT DR6 + SPT-3G. A Planck-only robustness refit is possible but low value; not run.
5. **DESI-MOCK with the full CMB:** deferred. It needs mock ACT/SPT/Planck spectra fed through their likelihoods (new
   code, about a day). It is worth doing only for the paper's final version.
6. **Null predictions:** locked (`PREREG_NULLS.md`). **V6 Laplace:** dropped as superseded. It computed ln B for the
   pre-flagship models (old Spiral, ΛCDM, S8-L), and the job died on the PC on 9 Nov; it is not restarted. A Bayes
   factor for FLAG-1 can come from the MCMC (item 2) if needed.
