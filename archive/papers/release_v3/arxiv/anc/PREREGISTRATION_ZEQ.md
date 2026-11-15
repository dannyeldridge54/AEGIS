# Pre-registration: the Locked Twist (fewer knobs)

Written 26 October 2026, 18:50 CT, before either fit below was run. Danny Lee Eldridge, with Claude.

## Why

The free Twist adds three settings to the standard model (ΛCDM): f_EDE (how much), z_c (when), θ_i (starting angle).
Its fit gain, Δχ² = −6.5, is almost cancelled by the penalty of 2 per setting (ΔAIC = −0.5, a near tie).
A theory with fewer free settings must earn less to win.

## The two reduced versions

| Version | Rule | Free extra settings | Passes if |
|---|---|---|---|
| **Twist-2** | Switch-on locked to matter–radiation equality: a_c = ω_r / (ω_b + ω_cdm), ω_r = 2.4728×10⁻⁵ (1 + 0.22711 × 3.044), computed from each trial universe's own matter density | 2 (f_EDE, θ_i) | Δχ² < −4 vs ΛCDM (ΔAIC < 0) |
| **Twist-1** | As Twist-2, and the field period fixed by the torsion value F = 1.2247 M_Pl (as in PREREGISTRATION_F.md) | 1 (θ_i; f_EDE follows from the potential's height) | Δχ² < −2 vs ΛCDM (ΔAIC < 0) |

Note on counting for Twist-1: the code samples f_EDE and θ_i and ties F to 1.2247 with a tight external constraint (1%). The three settings (f_EDE, z_c, θ_i) map one-to-one onto (F, Λ, θ_i), so locking z_c and fixing F leaves **one** free setting. The constraint's own χ² term is removed before comparing with ΛCDM.

Data: Planck 2018 (TT,TE,EE + low-ℓ + lensing) + DESI DR2 BAO + Pantheon+ (no SH0ES). Same code, same settings and same ΛCDM reference (χ² = 2434.06) as the free Twist. Compare likelihood χ² and χ²_eff both, and report both.

## Disclosure (not blind)

The equality lock was chosen **after** seeing the free fit, whose switch-on (z_c ≈ 3576) sits next to equality (z_eq ≈ 3553 for the same universe). Many early-dark-energy fits in the literature also prefer z_c near z_eq. So a pass shows the lock costs nothing; it does **not** count as a successful blind prediction. A blind test would need new data (for example ACT DR6 + SPT-3G, already queued) run with this same rule unchanged.

## Physical reason to expect the lock (open problem 2 in MODEL_v2.md)

If the field is triggered by the matter content (its coupling to the fermion axial current), it should switch on when matter starts to dominate. This is a hypothesis, not a derivation.

## Outcomes and what we say

- Twist-2 passes: "With two settings, the Twist beats the standard model on the fair score." Then run the same rule on Planck PR4 + ACT DR6 + SPT (the blind test).
- Twist-2 fails: say so on the page; the timing knob is doing real work.
- Twist-1 passes: strong support for the torsion origin. Fails: as already expected from the free fit (F ≈ 0.14), the torsion period needs a new derivation.
