# PREREG D632: running α_s for two-term SERAPIS versus the plain attractor (a possible distinguishing signature), locked before computing
Machinery: the D588 exact background + Mukhanov–Sasaki code, unchanged except that spectra are evaluated at k*·e^{s} for s ∈ {−0.1, −0.05, 0, 0.05, 0.1}.
- n_s(s) from central differences of ln P_R.
- α_s = dn_s/d ln k at s = 0, from the slope of n_s.
Models: HS-Kairos (ε = 0) and two-term ε ∈ {1.0e-4, 1.3e-4, 1.6e-4}; N* ∈ {47, 50}.
Comparison: the attractor relation α_s ≈ −(1 − n_s)²/2 evaluated at each model's own n_s.
Report α_s, the attractor value, and their ratio.
Verdict: a "distinguishing signature" if two-term α_s differs from the attractor relation by more than a factor of 2 OR has the opposite sign. Note the detectability: future σ(α_s) ~ 2e-3 (CMB-S4) to ~5e-4 (21 cm, optimistic).
