# PREREG D581: allowed ε window for two-term SERAPIS, with the full consistency chain (locked before computing)

Grid: ε ∈ {5e-5, 7e-5, 1e-4, 1.3e-4, 1.6e-4, 2e-4}; c_Γ ∈ {1, 10}; Phase-A bounds w = 3/5 and w = 0.

Machinery:
- Exactly the D578 script functions (model 'e'), with one N* iteration as in D578.
- For leptogenesis, the D579 formula with M₁ = m/3 and Br = 1.

Report per row: N*, y*, home-safe, n_s, r, σ vs SPA and SPA+DESI, m, T_RH, Y_B,max, lepto pass.

Window definition: ε is ALLOWED if every row for that ε (both c_Γ, both w) satisfies all three conditions:
- home-safe (y* ≤ 25);
- |n_s − 0.9728| ≤ 2 × 0.0027;
- Y_B,max ≥ 8.75e-11.
Report the allowed set and its width, ε_max/ε_min.

Naturalness reference values (fixed now, compared only afterwards):
- q(i)^{3/2} = e^{−3π} = 8.07e-5;
- (1/16π²)² = 4.0e-5;
- 1/16π² × 1/(4π) = 5.0e-4.
Any coincidence counts only if a reference value falls inside the window. It is labelled numerology unless a mechanism is given.

Fixes go in PREREG_D581_DEVIATIONS.md, written first.
