# PREREG L3 — DESI DR2 BAO likelihood in Janus-LT (data: data/desi/dr2_bao_table4.txt, fetched from 2503.14738 Table IV)
Locked 2026-11-17 before any χ² is computed.
Likelihood: BGS uses D_V/r_d; the six others use (D_M/r_d, D_H/r_d) with correlation r_MH (2×2 Gaussian blocks);
blocks independent (as quoted per tracer). 13 data points. Model distances from Janus-LT Cosmo; r_d as a free
combination h·r_d (BAO-only fits depend on H0 r_d) for the validation, and from Janus-LT's own chain (L0b2) elsewhere.
Validation V: flat ΛCDM BAO-only fit over (Ω_m, h·r_d) by χ² minimisation (and the Δχ² = 1 errors from the Hessian):
reproduce DESI's Ω_m = 0.2975 ± 0.0086 and h·r_d = 101.54 ± 0.73 Mpc (Eq. 17; marginalised posteriors) — pass if both
central values are within 0.3σ and the errors within 15 %. Then report χ² (13 points) for: (i) Planck-like ΛCDM
(Ω_m = 0.3153, h = 0.6736, r_d from L0b2 chain), (ii) TorsionΛ D715/D1025 case (b) (β = 0.192, H0 = 72.95), (iii) the
DESI best-fit w0–wa direction is NOT fitted here (later step).
