# PREREG_RW5_ZETA5 — the ζ(5) flip of the plateau (Danny's plan, tools/project_docs/WEAVE_MIRROR_SYMMETRIES.md row 2)
Locked 21 Nov 2026 before computing. AI-assisted. Script theory/tests/rw5_zeta5.py; result field_tests/results/rw5_zeta5.json.
Likelihood: the D1692 one (field_tests/scripts/realdata/run.py, DESI DR2 BAO full covariance + DES-SN5YR Dovekie
STAT+SYS, no CMB), imported unchanged. Thread at leading order V = V_L(1 − A e^{−βφ}), frozen at a = 1e-3,
fit parameters (Ω_m, amp), amp = A e^{−βφ_i}.

## Locked inputs (from the plan, not refitted)
Forward: A = 7.30 = (8/3)·2ζ(2)/ζ(3), β = 2√2. Flip (ζ(5) copy from E(·,5/2)): A′ = 4.45 = (16/5)(4/3)ζ(4)/ζ(5),
correction ∝ y⁻⁴ ⇒ β′ = 2β = 4√2, height normalisation (5/3)².

## R0 — what the leading-order likelihood can see (derived, checked numerically)
φ → φ + c maps A → A e^{−βc}; V_L is shot to H₀. So A and the (5/3)² height norm are absorbed into φ_i and V_L,
and χ² cannot depend on A at fixed β. Check: best-fit χ² with A = 7.30 and with A = 4.45 (β = 2√2) agree to
|Δχ²| ≤ 0.01. If they do, Danny's pass rule for A ("4.45 within 1σ of free A and better than 7.30 by Δχ² ≥ 1")
is UNTESTABLE at leading order and is reported as such (not as a fail of the flip). If they differ by more,
the script is wrong: stop and write DEVIATIONS.

## R1 — the testable part, β′ = 2β
Fit (Ω_m, amp) with β′ = 4√2 (A′ = 4.45, which does not matter by R0) and with β = 2√2 (A = 7.30), same starts
as D1692 plus [0.31, 0.10]. Δ ≡ χ²(4√2) − χ²(2√2).
- FLIP FAVOURED if Δ ≤ −1; FLIP DISFAVOURED if Δ ≥ +1; TIE otherwise. Also report both against ΛCDM (fit in
  the same run).
- Sanity: the β = 2√2 fit must reproduce D1692's χ² = 1638.32 within 0.05; otherwise INVALID.
This is a post-data model comparison; it counts as evidence only on future data (DR3/Euclid).

## Not tested here (stated now)
A becomes physical only if the field origin is fixed by the knot (the exact SERAPIS curve, D1638). That test
needs the exact ζ(5) curve, which is not built; recorded as open.
