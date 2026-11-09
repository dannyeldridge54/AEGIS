# Can the Twist give a momentum coupling (dark scattering)? (8 Nov 2026)

**Answer: not derived. Label: CHOSEN (an add-on) if it is used.**

- Pure momentum exchange (Pourtsidou, Skordis & Copeland 2013, "type 3"; Simpson 2010) needs a term coupling the
  dark-energy field's gradient to the dark-matter **velocity**, Z = u^μ ∂_μ φ, in the action.
- The Twist's couplings are: (1) the dilaton/conformal coupling, m_c ∝ exp(β φ), which exchanges **energy** (the β of
  the fits); (2) the angle's Nieh–Yan / axial coupling ∂θ · J5, which couples to **spin** (the axial current), not to
  velocity. For ordinary, unpolarised dark matter the average axial current is zero, so (2) gives no fluid-level
  momentum exchange.
- Neither gives a u·∂φ term. A momentum coupling would have to be added by hand, with its own parameter ξ.

## Code smoke test (DS-CLASS, branch IDE_DS, commit 7a909f4; not a gate result)
CPL dark energy at the Spiral's own fit (w0 = −0.92, wa = −0.13), otherwise Planck-like; Newtonian gauge (the code's
coupling acts only there). σ8 change vs ξ = 0:
| ξ [b/GeV] | A_ds = ξ(1+w0) | σ8 change |
|---|---|---|
| 10 | ≈ 0.8 | −0.04% |
| 125 | ≈ 10 | −0.45% |
| 375 | ≈ 30 | −1.07% |
The code works and slows growth as expected, but because the Spiral's dark energy is close to w = −1 (1 + w is small),
the effect is weak: about 1% in σ8 at A_ds ≈ 30, already above the KiDS-1000 bound (|A_ds| ≤ 20 b/GeV at 68%,
Carrion et al. 2024). S8-J needs roughly 2–3% to pass DES Y3 cleanly. **Momentum coupling looks like a weak path for
our model;** it is kept as a draft, not locked.
