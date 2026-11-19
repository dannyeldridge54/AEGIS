# PREREG SPTILT_T1X — extend the slow tilt family to see whether a y^{1/2}-type tilt (BBHL-term shape) can reach the band at all

Locked 2026-11-19 (09:30 CT) before computing. DpL cycle 4.
Motivation [derived this cycle]: the BBHL α'³ potential term V_α' = 3ξ̂ e^{K}|W₀|²/(4𝒱³) with ξ̂ = ξ·(Im τ)^{3/2} → SL(2,Z)-completed
ξ·E(τ,3/2)/(2ζ(3)) and e^{K} ⊃ 1/(2 Im τ) gives, at fixed 𝒱 and W₀, V_α' ∝ E(τ,3/2)/Im τ ~ y^{1/2}. As a tilt on P3-S this is
T1-like (y^{1/2}) if the plateau term carries no e^{K}, and T3-like (E ~ y^{3/2}) if it shares the 1/Im τ of e^{K}.
Runs (same script field_tests/scripts/sptilt/run.py, families unchanged):
  T1 (X = E^{1/3} ~ y^{1/2}) at f ∈ {3, 4, 5, 6}  and  a new family TB: X = E(τ,3/2)/Im τ (the literal BBHL shape) at f ∈ {1, 2, 3, 4, 5, 6}.
Rule: report the band interval in f (interpolated) or "never in band up to f = 6"; r at n_s = 0.969 if reached.
Expectation stated now: T1 reaches n_s 0.969 near f ≈ 3.3 with r ≈ 5.7e-4 (edge); TB similar to T1.
No reruns to chase results; fixes only via PREREG_SPTILT_T1X_DEVIATIONS.md written first.
