# PREREG D715: TorsionLambda background audit
Locked 2026-11-15 before computing. Script: theory/review/torsionlambda_audit_d715.py. Output: field_tests/results/torsionlambda_audit_d715.txt.

## Question
Is TorsionΛ's background (torsion-lambda-toolkit v0.2.0, src/physics/cosmological-distances.ts: E² = Ω_r(1+z)⁴ + Ω_m(1+β)(1+z)³ + λ) consistent with the Planck 2018 compressed CMB distance priors, and is β distinguishable from Ω_m at background level?

## Inputs (fixed now)
- Model / parameters: E(z) exactly as coded (no renormalisation); cases (a) toolkit defaults β = 0, Ω_m = 0.315, λ = 0.685, Ω_r = 5e-5 (from Ω_r h² ≈ 4.2e-5 noted in code comments: use 9.1e-5 incl. neutrinos as stated test value too); (b) Danny's October parameterisation β = 0.192, H0 = 72.95, Ω_m = 0.315, λ = 0.685; (c) as (b) with λ renormalised so E(0) = 1.
- Data: Planck 2018 compressed priors (Chen, Huang & Wang 2019, arXiv 1808.05724): R = 1.7502 ± 0.0046, ℓ_A = 301.471 ± 0.090 (flat ΛCDM, TT,TE,EE+lowE). z_* from Hu–Sugiyama with ω_b = 0.02237, ω_m = Ω_m h².

## Method
R = √Ω_m^eff H0 χ(z*)/c with Ω_m^eff = Ω_m(1+β) (the matter actually in E) and also with bare Ω_m (as the toolkit's R formula uses p.Ωm0); ℓ_A = π χ(z*)/r_s(z*) with r_s from the standard integral (R_b from ω_b). Also: show that β enters E only via Ω_m(1+β) (algebraic degeneracy) by refitting case (b) with β = 0 and Ω_m' = Ω_m(1+β).

## Decision rule (written before running)
- PASS if: |ΔR|/σ < 3 and |Δℓ_A|/σ < 3 for case (c).
- FAIL if: either exceeds 3σ. Degeneracy is a statement, not a pass/fail.
- What happens if the run crashes or times out: fixes only through D715_DEVIATIONS.md, written before any rerun.

## Labels
Mark every number in the write-up as computed / estimate / literature / from memory.
