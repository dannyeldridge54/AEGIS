# PREREG ANGLEGB — the Kähler-modulus Gauss–Bonnet coupling F₁ ~ (π/12)c₂·t projected on an angled trajectory: can it tilt P3-S?

Locked 2026-11-19 (11:00 CT) before computing. 1-min derivation loop (D1562: dilaton GB absent at N = 2; Kähler F₁ ~ 1e2–1e3).
Model (straight-line reduction, as D1553; the volume potential is taken FLAT along the path to isolate the GB effect — stated):
  canonical dilaton φ = ln y/√2; canonical Kähler χ = √(3/2) ln(2t) (K = −3 ln(T + T̄)); path φ = ψ cos θ, χ = ψ sin θ;
  V(ψ) = A·V₀^{P3-S}(y = e^{√2 ψ cos θ}), A = 1.68e-11; ξ(ψ) = s·F₀·e^{√(2/3) ψ sin θ} (F₁ ∝ t, F₀ = (π/12)c₂t at ψ = 0 ≡ "c₂t" scale), s = ±1.
Guo–Schwarz first-order formulas (as PREREG_GBTILT), N* = 50.3, end at ε₁ = 1.
Grid: θ ∈ {0.01, 0.03, 0.1, 0.3, 0.6, 1.0} rad × F₀ ∈ {1e1, 1e2, 1e3, 1e4} × s ∈ {+1, −1}.
Report: in-band points; the smallest F₀ that reaches the band; compare with the natural F₁ ~ 6e2–1.3e3 (D1562).
Expectation stated now: ξ' ∝ sin θ·F₀·e^{…}; the needed ξ'V matches D1561's (ξ₀E' ≈ 3.3e4·E' ~ 7e7 at y*) only for F₀·sin θ ≫ 1e3 ⇒ no band
at natural sizes; a band may appear at F₀ = 1e4 for large θ — where the dilaton plateau is also stretched (cos θ < 1 changes r).
No reruns to chase results; fixes only via PREREG_ANGLEGB_DEVIATIONS.md written first.
