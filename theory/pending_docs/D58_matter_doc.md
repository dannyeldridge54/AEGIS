## Development 58 — Dark matter must be a fermion (13 Nov 07:15)

**Caveat closed from D38.** Besides being made in the hot plasma, gravity-only dark matter is also made by inflation itself. A light scalar (m ≪ H_inf ≈ 10¹³ GeV) with ordinary coupling to gravity picks up quantum fluctuations ⟨X²⟩ = 3H⁴/(8π²m²); their energy 3H⁴/(16π²) is frozen until H = m and then behaves like matter. For m = 10⁵–10⁷ GeV that overproduces dark matter by **10²²–10²⁵**. A fermion is conformal when massless and gets no such condensate (estimated, not computed in detail).

**Crossroads.** A. Scalar, minimally coupled — ruled out by 10²²+. B. Scalar with conformal coupling ξ = 1/6 — possible, but an extra tuned coupling. C. Fermion — no condensate, no new parameter. **Taken: C.**

**Prediction, sharpened.** The dark matter is a fermion that interacts only through gravity, with mass **1.4–6.6×10⁶ GeV** at the derived reheating temperature (T_RH = 3–5×10¹⁴ GeV, D42). Code: theory/matter/dm_inflation_production.py.

PAPER (Section 6, gravity-only dark matter paragraph): replace "Prediction: null results in direct detection. Production from the inflaton condensate through gravity is not yet included." with "Inflation itself would overproduce a light, minimally coupled scalar by 10²²–10²⁵ (frozen fluctuations 3H⁴/16π²), so the dark matter must be a fermion (or a conformally coupled scalar): a gravity-only fermion of 1.4–6.6×10⁶ GeV at the derived T_RH. Prediction: null results in direct detection."

ADD TO DEVELOPMENT 57 (table row): base-theory slope with coupling (K816: κ = √(2/3), β = 0.034, KAPPA-ALPHA1 FULL fit): w₀,eff −0.907, w_a,eff −0.16, lowest w_eff −1.01. With the base theory's own slope the coupling still makes w_eff dip just below −1, and w_a sits between PURE-TWIST and FLAG-1 — well inside the −0.40 ceiling.

## Development 59 — The gravitational-wave hum from inflation (13 Nov 07:25)

From r = 0.0034–0.0040 (frozen) and the standard radiation-era transfer, the primordial gravitational-wave background today is Ω_GW h² ≈ 4–5×10⁻¹⁸, flat from LISA to ground-based frequencies (tilt n_t = −r/8 ≈ −0.0005). Kination after the cliff (about 2 e-folds at the derived heat share) would boost it only above ~10⁷ Hz, by at most ~10× — out of reach of any planned detector. Rough detector reaches: LISA ~10⁻¹³ and Einstein Telescope ~10⁻¹² cannot see it; BBO (~10⁻¹⁷) cannot; a DECIGO-class mission (~10⁻¹⁸ or better) is at the edge. Prediction: no primordial background in LISA or ground detectors; the Twist's tensor signal is for CMB B-modes (LiteBIRD) and, ultimately, DECIGO-class missions. Detector reaches are approximate. Code: theory/inflation/gw_background.py.
