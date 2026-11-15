# PREREG D574: deriving the τ = i vacuum (Danny 07:28 CT, "Derive τ = i")

Locked before any computation. Script: theory/modular/tau_i_d574.py. Output: field_tests/results/tau_i_d574.txt.

## Analytic claims to verify numerically (no fitting)
- **A. Stationarity.** Any S-invariant V that is C¹ at i has ∇V(i) = 0. Reason: S fixes i and acts there as δτ → −δτ.
  - Check: the gradient of the SERAPIS-KL V (D545/D564 form, p = 1, 2) at i is < 1e-8 of its value at |δ| = 0.01. Use a central difference with h = 1e-5.
- **B. Weight parity.** A modular form of weight w satisfies f(i) = i^w f(i), so f(i) = 0 unless w ≡ 0 mod 4.
  - Check: |E₄(i)| > 0.1; |E₆(i)| < 1e-12; |E₆'(i)| > 0.1 (a simple zero); j(i) = 1728 to 1e-10.
  - Check: j − 1728 has a zero of order 2 at i. Fit log|j(i+δ) − 1728| against log|δ| for δ = 1e-2 … 1e-4: slope 2.00 ± 0.02.
- **C. Curvature order.** If V depends on τ only through |j − 1728|² (as in I = (1/4π) ln(1 + |j − 1728|²/1728²)), then V − V(i) ∝ |τ − i|^{4p}. The vacuum is then MASSLESS (no quadratic term) for every p ≥ 1.
  - Check: the slope of log V against log|δ| (δ = 1e-2 … 1e-4, three directions) equals 4p ± 0.05, for p = 1 and 2.
- **C′. Derived fix.** Built on |j − 1728|¹ (∝ |E₆|²/|Δ|, the holomorphic-E₆ route of D537):
  - I₁ = (1/4π)·ln(1 + |j − 1728|/1728). Then V ∝ |τ − i|^{2p}: quadratic, so massive, at p = 1. At p = 2 it is still quartic.
  - Check: the slopes are 2p ± 0.05.
  - I₁ grows like y/2 at the cusp (y = Im τ), versus y for I.

## Scored inflation numbers for the C′ variant (SERAPIS-KL1)
- Same machinery as D564 (copied verbatim, with Iy replaced by I₁(y)); α = 1/3 kinetic term; p ∈ {1, 2}; N* ∈ {52, 55.6}.
- Report: n_s, r, y*, and whether it is home-safe (y* ≤ 25), plus the distances to SPA (0.9684 ± 0.0030) and SPA+DESI (0.9728 ± 0.0027).
- Vacuum mass for p = 1, in units of H_inf: m²/H² = 3·V''(φ_vac)/V_plateau, with φ canonical (α = 1/3, so φ = √(3α/2)·ln y... the D564 convention qn = 1/√2 per unit ln y). Report the number only.
- These are POST-HOC models (built after seeing the data), so they are scored only on future data. No rerun to tune anything; fixes go in PREREG_D574_DEVIATIONS.md, written first.

## Verdict rules
- If C holds: SERAPIS-KL (D545/D564/D567) has a massless quartic (p = 1) or octic (p = 2) vacuum. Reheating goes through an anharmonic oscillation (w = (n − 2)/(n + 2): 1/3 for n = 4, 3/5 for n = 8), so the D567 N* window (which assumes matter-like reheating) must be re-examined. This is recorded as a correction note.
- If C′ holds: the holomorphic-E₆ route gives a massive τ = i vacuum at p = 1 only.
