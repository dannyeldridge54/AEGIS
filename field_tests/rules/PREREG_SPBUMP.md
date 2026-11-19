# PREREG SPBUMP — P3-S with a dilaton-dependent gravitino mass: the Casas–Ibáñez plateau turned into a bump (hilltop) — does it inflate in band?

Locked 2026-11-19 (09:50 CT) before computing. DpL cycle 12.
Derivation (stated before computing): the one-loop species potential (arXiv:2507.05345) is δV ∝ m_3/2²·g^{ij̄}∂ln Λ∂̄ln Λ. With the IIB dilaton
in K = −ln(−i(τ − τ̄)), m_3/2² = e^{K}|W|² carries a factor (Im τ)^{−1} for τ-independent W (the minimal case: dilaton F-term
F^τ = e^{K/2}K^{ττ̄}K_τW₀ ≠ 0). So V = V₀^{species}(y)·(y_ref/y)^q with q = 1 (CI's "m_3/2² ~ 1/u^r ⇒ bump"). At large y, V ∝ e^{−√2qφ}
(ε → q²): no plateau; a maximum forms where the species approach (1 − 7.30/y²) meets the 1/y fall-off (y_max ≈ √(3·7.30) ≈ 4.7 for q = 1).
Runs (engine F, T_R 8.94e8, D1 stencil, start by the D1 bisection rule on the ρ side of the maximum; no tilt):
  q ∈ {1, 0.5, 0.25, 0.1}.
Report: y_max, n_s, r, α_s, N*, whether 100–200 e-folds exist on the ρ side; in band / near (PREREG_SMSCAN).
Expectation stated now: hilltop inflation near y_max with strongly red n_s (|η| large: n_s ≲ 0.95) for q = 1; q ≤ 0.1 approaches the
untilted plateau (n_s ≈ 0.96, slightly redder). No in-band point expected without a tilt.
No reruns to chase results; fixes only via PREREG_SPBUMP_DEVIATIONS.md written first.
