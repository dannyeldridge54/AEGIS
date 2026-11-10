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
