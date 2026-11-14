# PREREG D419 — Route A: can a tiny superpotential deformation (K kept = −3 ln(T+T̄)) bring the Twist to n_s ≈ 0.974? (locked 17:50 CT)
Danny 17:42 "Set this up" (Route A after the crown, D410). Script theory/twist2/routeA_d419.py: F → (T + ε) cliff/√(1+T/μ), i.e. one added
holomorphic term; scan ε ∈ {0, ±10⁻⁶, ±3×10⁻⁶, ±10⁻⁵, 2–3×10⁻⁵}; solve ε for n_s = 0.9736 (the crown's THAW_FREE value) at N* = 57.2.
Report n_s, r, α_s, B1, B2 per ε and at the solution, plus cross-sector factors (1 + ε/x)² at the end of inflation and at x_E (Λ).
Reading (left ladder + centre): ROUTE A WORKS if a solution exists with |ε| ≤ 10⁻³ AND the end-of-inflation factor differs from 1 by < 1% (so
kination/N*/D391 are unchanged) AND the Λ factor differs from 1 by < 10⁻⁴ (absorbed in n without retuning beyond 10⁻⁴). The new predictions
(r, α_s, B1, B2 at the solution) are then LOCKED as the Twist-2 inflation predictions; n_s is no longer a prediction but a fit (stated).
If no solution: ROUTE A FAILS for this deformation. Next (only if it works): rerun the crown THAW_TWIST with the new n_s (needs a new lock).
No reruns to chase; fixes via PREREG_D419_ROUTE_A_DEVIATIONS.md first.
