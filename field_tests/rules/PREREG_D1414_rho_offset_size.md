# PREREG D1414 — can a D640-type offset explain the ρ vacuum's 3.4 % Janus miss? (size estimate first)

Locked 2026-11-19 (UTC) before computing (JANUS tick 12; ladder flag janus: recheck after D1413).
SERAPIS-E (D691): V/V0 = P_E(1 + CÊ), P_E = Ê/(Ê+1), Ê = E(τ,2) − E(ρ,2). With E(τ,2) = Σ' y²/|m+nτ|⁴ ≈ 2ζ(4)y² + O(1/y)
(+ exponentially small), the plateau is 1 − 1/(Ê+1) with Ê + 1 ≈ 2ζ(4)y² + B, B = 1 − E(ρ,2): an offset in I² = 2ζ(4)y²
(D691's effective I = √(2ζ(4))·y), the analogue of D640's I = y − c at τ = i.
Compute: E(ρ,2) by direct lattice sum (|m|,|n| ≤ 400, tail estimate), B, and the fractional offset δ = B/I*² at the A1 point
(I*² = 2ζ(4)y*², y* = 14.1–14.7 from D691). Compare with τ = i's c/I* (D640/D1412: c = 1.18646, I* ≈ 23.6 → 5.0 %, which
produced a 10.8 % α_s miss, ratio ≈ 2.1).
Rule (estimate tier): "offset can explain it" if |δ|·(the τ = i ratio 2.1, as a rough scaling, stated) is within a factor 2 of
3.4 %; "offset too small" if it is below 0.85 %; otherwise "inconclusive". No claim beyond the estimate tier.
No reruns to chase results; fixes only via PREREG_D1414_DEVIATIONS.md written first.
