# PREREG_D1653_G9B_TAU_PLANE — where the dark thread ends in the full τ plane (Janus genesis G9b; locked 2026-11-19 ~23:00Z before any number)
Model (stated choices):
- Fields τ = x + iy with the SL(2,Z)-invariant kinetic term ½·(ẋ² + ẏ²)/(b²y²), b = √2 (D = 10). Along x = ½ this is exactly v3's canonical φ (y = e^{bφ}); off the line the axion gets the same normalisation because SL(2,Z) invariance forces it [derived].
- Potential: v3's gradient form taken with the full field-space gradient, V = V_Λ·(4/9)·y²[(∂_x ln E)² + (∂_y ln E)²]·[1 + C(E − E(ρ))], C = 8e-7. On x = ½ (∂_x E = 0) it equals p3s.V exactly [derived]. E(τ, 3/2) from its Fourier series with cos(2πnx) (n ≤ 40, same truncation as p3s).
- Background as D1644 (Ω_m 0.31, Ω_r 9e-5, frozen at a = 1e-3, V_Λ re-shot to H₀ = 1 per run), start amp = D1638 best (0.29268) on x = ½ plus an axion offset δx, integrate to a = 50.
- Sigma-model EOM in e-folds with Poincaré-half-plane Christoffels (Γ^x_xy = −1/y, Γ^y_xx = 1/y, Γ^y_yy = −1/y).
Runs: δx ∈ {0, 1e-6, 1e-3, 1e-2}.
Checks / rules (locked):
R0 (code check) δx = 0 reproduces D1644: a_end_acc within 1 % of 1.232 and settling y within 2 % of 0.500. If R0 fails the run is a bug — DEVIATIONS before any rerun.
R1 For each δx, classify the end point (mean τ over the last 20 % of e-folds) by its SL(2,Z) image: "i-class" if j(τ) ≈ 1728 (map to the fundamental domain, compare with i within 0.02), "ρ-class" if it maps to ρ within 0.02, else "other".
Verdict: ROBUST if every δx > 0 run ends i-class (the D1644 end point survives a free axion); FRAGILE if any ends ρ-class or other (D1644's end point is a 1D artefact for that run). Also report max |x − ½| reached and late ⟨w⟩ per run.
Caveat: the 2D gradient form is the natural extension of v3, not separately derived; quantum/perturbation effects not included.
Script: field_tests/scripts/janus_g/g9b_tau_plane.py → field_tests/results/D1653_G9b_tau_plane.json
