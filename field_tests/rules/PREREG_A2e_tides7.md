# PREREG A2e — tidal phase through 7PN (Henry–Faye–Blanchet 2020) vs LAL (Djl B) — locked 2026-11-17
Source (fetched, arXiv:2005.13367 Eq. 6.6a and its definitions):
- ψ_tidal = −(9v⁵/16ν²){[(1+22ν)μ̃₊ + Δμ̃₋] + [6PN]v² − π[(1+22ν)μ̃₊ + Δμ̃₋]v³ + [7PN]v⁴ + [7.5PN]v⁵}, with v = (πGmf/c³)^{1/3}.
- μ̃± = ½[X₂X₁⁴Λ₁ ± X₁X₂⁴Λ₂]. Δ = (m₁−m₂)/m.
- σ̃ (magnetic) = μ̃^(3) (octupole) = 0 here: only quadrupolar Λ is passed to LAL. This is labelled as an assumption about LAL's handling.
- Coefficients as recorded in the fetch (PREP below the code).
Transcription check (done before the lock): equal-mass 5PN reproduces VFH 2011's −624 (D1098). −(9/16)(16)(6.5)(Λ/32) = −1.828Λ, matching 3/32 · (−624/32)Λ.
Code (written after this lock): gw.taylorf2_tidal_dphase_hfb(f, M1, M2, Λ1, Λ2, order ∈ {5, 6, 6.5, 7, 7.5}).
Tests (LAL TaylorF2 with − without tides, detrended, the D1098 method; cases as A2d):
- E1: ours(order 6) vs LAL PNTidalOrder 6PN ≤ 1e-6 rad. This is a cross-check of HFB vs VFH at 6PN.
- E2: ours(6.5) vs LAL 65PN ≤ 1e-6 rad.
- E3: ours(7) vs LAL 7PN ≤ 1e-6 rad.
Reported: 7.5PN vs LAL 75PN, if that enum exists.
A2e VALIDATED iff E1–E3 pass. Fixes only via DEVIATIONS.
Script theory/janus_astro/a2e_check.py.
