# PREREG D1286 — which lattice wins in d = 6 and d = 7, at every scale? (locked before computing)
Question (Danny 2026-11-18: "keep mapping out all the other parts of the lattices"): D1282 compared E6, E7 only with their own
duals. Here every standard family competes: Zⁿ, Dₙ, Dₙ*, Aₙ, Aₙ*, Eₙ, Eₙ* (n = 6, 7), unit covolume, Gaussian energy
θ(α) − 1 = Σ_{v≠0} e^{−πα|v|²}, α ∈ {1, 1.25, 1.5, 2, 3} computed by exact enumeration (|v|² ≤ 12), α < 1 from Poisson.
## Predictions (stated before any number is computed)
- P1: for α > 1 the winner in d=6 is E6 and in d=7 is E7 (they are the densest known lattice packings in those dimensions).
- P2: for α < 1 the winner is E6* (d=6) and E7* (d=7) (Poisson + P1).
- P3: Zⁿ never wins at any α in d=6,7.
- P4: every family pair L/L* ties exactly at α = 1 (Poisson), to ≤1e-9.
## Pass/fail
P1–P4 each PASS/FAIL as stated. Convergence: Q=10 vs Q=12 must agree to ≤1e-9 at α ≥ 1.25 (else that entry is reported unconverged, not scored).
Caveat stated in advance: these families are not all lattices; a FAIL of P1 would only mean some listed family beats Eₙ.
