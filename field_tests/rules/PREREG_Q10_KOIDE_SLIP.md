# PREREG Q10 — can the charged leptons sit on rung 1 (slip |ε| = 0.024 off ρ) and keep Koide Q = 2/3? (locked 2026-11-20, before computing)
Koide in the Weave is the Z₃ circulant √M = a + bC + b̄C² (D1595, P-F1), exact only with the residual Z₃ of the knot ρ.
A slip ε breaks Z₃; at first order it adds a NON-circulant piece to √M of relative size κ|ε| with κ an O(1) coefficient.
Model: √M₀ = circulant reproducing (m_e, m_μ, m_τ) PDG exactly (Brannen a, b, δ from data); √M = √M₀ + |ε|·a·K, K a random complex 3×3
with entries κ_ij, |κ_ij| log-uniform in [1/3, 3], uniform phases; |ε| = 0.02395 (Q11 rung 1). 2e5 samples, seed 7.
Masses = (singular values of √M)². Report ΔQ = Q − Q₀ distribution.
Koide precision: σ_Q = 7.7e-6 (Belle II, D1594) ⇒ tolerance 3σ = 2.3e-5.
Rule: the fraction f of samples with |ΔQ| ≤ 2.3e-5 is the "accident probability".
 COMPATIBLE if f ≥ 0.05. INCOMPATIBLE (needs tuning) if f < 0.05 ⇒ charged leptons cannot sit on rung 1 with Koide exact;
 the rung-1 assignment of D1734 T1 is then withdrawn for leptons (they stay on the knot) OR Koide is an accident.
Also report the median |ΔQ| and the |ε| at which median |ΔQ| = 2.3e-5 (scaling).
No reruns.
