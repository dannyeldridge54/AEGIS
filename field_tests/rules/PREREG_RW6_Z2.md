# PREREG_RW6_Z2 — does the Z₂ at τ = i protect α from the thread? (plan row 5)
Locked 21 Nov 2026 before computing. AI-assisted. Script theory/tests/rw6_z2.py; result field_tests/results/rw6_z2.json.

## Derivation (to be written in the D-note; no number depends on it)
Near the fixed point i, u = (τ − i)/(τ + i) and S: τ → −1/τ acts as u → −u. Any S-invariant real function of τ
(the physical, modular-invariant one-loop threshold, e.g. built from Im τ |η(τ)|⁴) is even in u, so its
gradient vanishes at i: ln α(φ) = ln α_i + (c/2)(φ − φ_i)² + O((φ−φ_i)⁴).

## Inputs (fixed now)
- c (per M_P²): natural size = the D1851 one-loop coefficient per M_P, c ∈ [3.9e-4, 7.5e-4]; report also an
  O(1) band ×[0.3, 3].
- Δφ = 0.64 M_P: thread excursion from the frozen start (z*) to today (engine default, D1749 RIGHT note).
- d = distance today → knot (unknown exactly). Estimate (labelled): d ≈ φ'·ln(a_knot), φ' = √(3(1+w₀)Ω_DE),
  w₀ = −0.74, Ω_DE = 0.69, a_knot = 1.89 (D1644 G9 json). The plan's form c(Δφ)²/2 is the d = 0 case, a LOWER
  bound on the drift since (d + Δφ)² − d² ≥ Δφ².
- Bounds: MICROSCOPE ζ < 1.66e-6 (D819); quasar/ESPRESSO-level |Δα/α| ≲ 1e-6 since z ~ 1–2 (the level used in
  the D1749 RIGHT note); atomic clocks |α̇/α| ≲ 1e-18 /yr (level quoted in D-notes; report only).
  H₀ = 67.4 km/s/Mpc.

## Tests
- T1 (decides): drift since z*, |Δ ln α| ≥ c_low·Δφ²/2 (d = 0, most favourable). PASS if < 1e-6.
- T2: ζ today = c·d with the estimated d; PASS if < 1.66e-6. Also report d_max = 1.66e-6/c_low.
- T3 (report): α̇/α today = c·d·φ'·H₀ vs 1e-18 /yr.
Verdict: PASS only if T1 and T2 pass at c_low; FAIL if T1 fails at c_low; TENSION otherwise.
Thresholds will not be loosened.
