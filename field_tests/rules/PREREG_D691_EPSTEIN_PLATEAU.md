# PREREG D691: SERAPIS-E — plateau, vacuum mass and tilt from the Epstein zeta E(τ,2) alone (Danny: "how do I make this work")
Locked before computation, 2026-11-15. Script theory/modular/epstein_plateau_d691.py; output results/epstein_plateau_d691.txt.
Idea: Ê(τ) = E(τ,2) − E(ρ,2) ≥ 0 (minimum at ρ, D689) is isotropically quadratic at ρ and grows as 2ζ(4)y² at the cusp. A plateau built from it, P_E = Ê/(Ê + 1), therefore (a) has a MASSIVE vacuum at ρ, (b) approaches 1 as 1 − 1/(2ζ(4)y²) — the same y^{−2} approach (p = 2√2) as SERAPIS. Add the BHK one-loop tilt multiplicatively (D689): V/V0 = P_E(τ)·[1 + C·Ê(τ)].
Compute (exact first-order slow roll along Re τ = 1/2, φ = ln y/√2, mpmath; Ê via the D689 Fourier series, verified there):
1. Vacuum: m²/H² = 3·d²P_E/dφ² at ρ (canonical, both directions via the isotropy check from D689); m_φ for H_inf = 3.7e12 GeV (estimate).
2. Untilted (C = 0): y*, n_s, r, α_s at N* ∈ {46.09, 49.49}.
3. Tilted: C ∈ {1e-8 … 1e-5} log grid; find C for n_s = 0.9682, 0.9728; report y*, r, α_s and Im S·Im ρ = 15N/(64π⁶C).
Verdict: VIABLE if n_s 0.965–0.975 reachable with y* ≤ 25, |α_s| ≤ 0.009, a vacuum mass m_φ ≳ 1e10 GeV (enough for the D601-type reheating), and natural Im S·Im ρ (≳ 1, ≲ 1e4 N). No tuning beyond C.
