## Development 62 — Reheating without a free range (13 Nov 08:10)

**What was open.** D42 bracketed how far the inflaton rolls before the preheated χ particles decay (Δφ = 0.1–1 M_P). That distance is calculable: χ's mass grows as g·Δφ while the inflaton moves at φ̇ = 3.0×10⁻⁶ M_P² (from the model), and χ decays to Standard Model fermions at Γ = h²m_χ/8π. It decays when Γ·(Δφ/φ̇) = 1, so **Δφ = √(8πφ̇/(h²g))**.

| g | h (χ's Yukawa) | Δφ (M_P) | heat share f | T_RH (GeV) |
|---|---|---|---|---|
| 0.03 | 0.1–1 | 0.05–0.50 | 4×10⁻⁵–4×10⁻⁴ | 1.1–2.0×10¹⁴ |
| **0.1** | **0.1–1** | **0.03–0.28** | **4×10⁻⁴–4×10⁻³** | **2.1–3.7×10¹⁴** |
| 0.3 | 0.1–1 | 0.02–0.16 | 4×10⁻³–4×10⁻² | 3.6–6.4×10¹⁴ |

**Reading.** T_RH depends only weakly on the couplings (as the ¼ power of f): across a factor 10 in g and in h it stays within 1.1–6.4×10¹⁴ GeV. At the natural g ≈ 0.1 it is **2.1–3.7×10¹⁴ GeV**, slightly cooler than the 3–5×10¹⁴ GeV used since D42. Knock-on effects: the gravity-only fermion dark matter (D58) moves to **3.5×10⁶–1.9×10⁷ GeV**; the matter yield rises somewhat at the smaller f (D42 trend), so the hidden mass that gives exactly 1× shifts up from ~3×10¹⁰ GeV (to be rechecked with one run); lepto-axiogenesis still has T_RH far above its 10¹³ GeV requirement. Code: theory/inflation/chi_decay_distance.py.

## Development 63 — Frozen predictions for the headline model (13 Nov 08:20)

The base-slope coupled Twist (K816: κ = √(2/3), β fitted) is the headline late-time model since D61. Its predictions are frozen before DESI DR3 and Euclid (field_tests/results/k816_predictions.json; same methods as D39), from both its Pantheon+ fit (β = 0.034) and its DES Y5 fit (β = 0.030):

- Effective dark energy: w₀ ≈ −0.907, w_a ≈ −0.16 (both fits), inside the −0.40 ceiling.
- Growth: fσ₈ about 1–1.6% below ΛCDM at z = 0.5 (the coupling partly offsets the slower growth of PURE-TWIST, −3.3%); E_G about 3.4–3.6% above ΛCDM.
- S₈ = 0.807–0.808 vs ΛCDM 0.798–0.800: the coupling makes matter clump slightly **more**, the opposite of PURE-TWIST (0.793). Weak-lensing surveys that prefer S₈ ≈ 0.78 would favour PURE-TWIST over K816 — a way to tell the two apart.
- BAO distances at the DESI DR2 redshifts: per-bin D_M/r_d and D_H/r_d with % differences from ΛCDM, stored in the JSON.
