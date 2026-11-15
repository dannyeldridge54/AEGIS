# PREREG D639: tree-level visible soft masses in the SERAPIS supergravity sector (referee R8 M1; D585a)
Locked before computation, 2026-11-15. Script theory/modular/soft_masses_d639.py (sympy, exact). Output field_tests/results/soft_masses_d639.txt.
Set-up (one point, no fitting): hidden sector K_h = −ln(−i(τ−τ̄)) + |S|² (S the nilpotent goldstino field, treated at S = 0 with F_S ≠ 0), W = W0 + f S, with f² = 2W0² so V0 = 0 at the point (Λ ≃ 0; the plateau V(τ) is added by hand as in the paper and vanishes at τ = i). Visible chiral field Q, W independent of Q. Evaluate V to order |Q|² at Q = 0, τ = i, and report m_Q² = V_QQ̄/K_QQ̄ in units of m3/2² = e^{K}|W0|².
Cases:
- A canonical: K = K_h + |Q|². Expectation: m_Q² = m3/2² (+V0) → soft masses ~ m3/2 ~ 1e11 GeV.
- B sequestered (conformal-frame / Randall–Sundrum form): K = −3 ln(e^{−K_h/3} − |Q|²/3). Expectation: m_Q² = V0 = 0 at tree level (soft masses then loop/anomaly-mediated ~ m3/2/16π²).
- C one-modulus "no-scale-type" coupling: K = K_h + |Q|²/(−i(τ−τ̄))^{n}, n = 1: reported only.
Verdict rule: if B gives 0 (to 1e-12) and A gives 1, the paper states that the soft-mass sector closes at tree level only if the visible sector is sequestered in the conformal-frame sense, with loop-level masses ~ m3/2/16π², and that this is an assumption. If B ≠ 0, the soft-mass sector stays open. Pure anomaly mediation's tachyonic-slepton problem is noted as a further assumption, not solved here. No reruns; fixes via DEVIATIONS written first.
