# PREREG L0b2 — Janus-LT's own recombination → drag epoch z_d and r_d vs CAMB (follows D1006)

Locked 2026-11-17 before any L0b2 number.
Equations (fetched; RECFAST, Seager–Sasselov–Scott, as transcribed in astro-ph/0602577 Eqs. 1–4, 6–10):
H: dx_p/dz = C_H/[H(1+z)]·[x_e x_p n_H R_H − β_H (1 − x_p) e^{−hν_H/kT_M}], R_H = 1e-19·F·a t^b/(1 + c t^d) m³/s,
t = T_M/1e4 K, (a,b,c,d) = (4.309, −0.6166, 0.6703, 0.5300), F = 1.14; β_H = R_H(2π m_e kT_M/h²)^{3/2} e^{−3.4 eV/kT_M};
C_H = [1 + K_H Λ_H n_H(1 − x_p)]/[1 + K_H(Λ_H + β_H) n_H(1 − x_p)], Λ_H = 8.22458 s⁻¹, K_H = λ_α³/(8πH), λ_α = 121.5682 nm.
He I: Eqs. 6–9 (q = 10^−16.744, p = 0.711, T₁ = 10^5.114 K, T₂ = 3 K, B = 3.97 eV, Λ_He = 51.3 s⁻¹, 60.1404 nm, 58.4334 nm),
f_He = Y_p/(4(1 − Y_p)). He II and early phases: Saha equilibrium (standard Saha with scipy.constants; stated as such).
T_M: Eq. 10. x_e = x_p + x_HeII (+ He III by Saha at high z). Constants from scipy.constants only.
Drag epoch [standard definition, CAMB's]: τ_d(z) = ∫_0^z x_e n_H σ_T c /[H(z′)(1 + z′) R(z′)] dz′, R = 3ρ_b/(4ρ_γ); z_d: τ_d = 1.
CAMB 2.0.5 run with YHe = 0.24 (fixed, to match), massless ν, same 50 seeded cosmologies (L0a/L0b).
Tests: T1 |z_d/zdrag − 1| ≤ 2e-3 on every cosmology; T2 |r_d/rdrag − 1| ≤ 2e-3 using our z_d (route 1 now fully Janus);
report also the 1e-3 level. Verdict L0b2 VALIDATED iff T1 and T2. Fixes only via DEVIATIONS written first.
Note stated in advance: CAMB's recombination (RECFAST with later corrections) differs from this minimal RECFAST; a miss at
the 1e-3–2e-3 level would be the known minimal-model accuracy, recorded as such.
