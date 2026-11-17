# PREREG S4a2: Route A of S4a redone exactly (new lock; S4a's locked verdict NOT VALIDATED stands as recorded)
Reason: S4a's Route A used finite-difference second derivatives (step 1e-4), whose truncation/round-off floor (~1e-6 relative) exceeded the locked 1e-6; the first-derivative equation was satisfied to 6e-11. This lock replaces the method, not the threshold.
Method: substitute the Basile–Thomée solution (2.8) into the three equations (2.3) symbolically (sympy) with γ = 3/2, simplify each residual; then evaluate the simplified residuals numerically at 50 points y ∈ [0.05, 3] (α_E = 1, φ₀ = 0) as a second check.
Pass (fixed now): all three symbolic residuals simplify to 0 (and numerical |residual| ≤ 1e-12) → S4a Route A VALIDATED; combined with S4a Route B (1e-10, recorded) → S4a VALIDATED. Otherwise NOT VALIDATED (and the transcription of (2.8) is suspect).
Script theory/strings/s4a2_dm_symbolic.py; output field_tests/results/s4a2_dm_symbolic.txt.
