# PREREG D829 (P3.2): the τ-dependence of the anti-D3 interaction energy on the inflaton T² for the D696 configuration
Locked before computing, 2026-11-16.
Physics (stated, to be checked by numbers): D3s and anti-D3s are points in T⁶. The leading anti-D3–D3/O3 interaction is closed-string exchange, a Coulomb potential in the transverse space. Reduced on the inflaton T² (other tori small), it is the 2D torus Green's function
G(z,U) = −ln|θ₁(πz|U)/η(U)|² + 2π (Im z)²/Im U   (z = separation in units of the lattice 1, U).
The coincident (self-image) term regularises to Δ(U) = −ln(Im U |η(U)|⁴) + const.
Configuration (D696): N = 5 stuck D3s at each half-period z_k ∈ {½, U/2, (1+U)/2} and N₀ = 1 at the origin. Anti-D3 at the origin (case A) or at a half-period (case B).
Compute (mpmath, jtheta):
(a) S(U) = Σ_k G(z_k, U) for U = i, ρ = e^{iπ/3}, and U = ½ + iy, y = 2, 5, 10, 20. Is S constant (S₃ symmetry), and what is its growth with y?
(b) Δ(U) at the same points (D798 values for checks: Δ(ρ) − Δ(i) = −0.0212).
(c) Case A total V_int(U) ∝ N·S(U) + N₀·Δ(U) (sign to be fixed by charges; report both shapes).
Prediction (pre-stated): S grows linearly in y (the 2π(Im z)² terms do not cancel), so V_int is a LINEAR-in-y additive term, i.e. a TILT of the εI₁/L type, not a 1/E plateau.
