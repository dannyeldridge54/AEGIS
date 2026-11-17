# PREREG L9a — Janus-LT gets a matter transfer function: Eisenstein–Hu 1998 no-wiggle shape, validated vs CAMB
Locked 2026-11-17 before any L9a number. Formulas fetched (ar5iv astro-ph/9709112 §4.2): s = 44.5 ln(9.83/Ω₀h²)/√(1+10(Ω_bh²)^{3/4}) Mpc (26);
q = k/(h Mpc⁻¹)·Θ₂.₇²/Γ_eff (28); L₀ = ln(2e + 1.8q) (29); Γ_eff = Ω₀h(α_Γ + (1−α_Γ)/(1+(0.43ks)⁴)) (30);
α_Γ = 1 − 0.328 ln(431Ω₀h²)Ω_b/Ω₀ + 0.38 ln(22.3Ω₀h²)(Ω_b/Ω₀)² (31); T₀ = L₀/(L₀ + C₀q²), C₀ = 14.2 + 731/(1+62.5q). Θ₂.₇ = T_cmb/2.7.
Test: three flat ΛCDM cosmologies (h, ω_b, ω_c) = (0.6736, 0.02237, 0.1200), (0.70, 0.0224, 0.110), (0.64, 0.0220, 0.130), mν = 0 in both codes.
CAMB matter transfer (delta_tot, z = 0) normalised to its k → 1e-4 h/Mpc value; 30 log-spaced k in [1e-3, 0.5] h/Mpc.
EH no-wiggle has no BAO wiggles, so compare after smoothing CAMB? No — compare directly and claim: rms |T_EH/T_CAMB − 1| ≤ 5% and
max ≤ 12% per cosmology (wiggles are a few %). Pass all 3 → VALIDATED (shape only; amplitude/σ8 normalisation is the next lock).
Results: field_tests/results/janus_lt_l9a_eh.txt.
