# PREREG_REALDATA_NEG — "negative space" on REAL data: ΛCDM vs CPL vs the Weave reverse thread vs sign-switching Λ (locked D1692, 2026-11-20 01:15 UTC)
Danny 19:08: "Negative space lock test" + "Dl data" (download OK).
Data, downloaded from GitHub (hashes recorded):
- DESI DR2 BAO, ALL GCcomb mean + cov (CobayaSampler/bao_data @ bb0c1c90; mean sha256 9ac154ab…, cov 252a1432…).
- DES-SN5YR "Dovekie" recalibrated Hubble diagram + STAT+SYS inverse covariance (des-science/DES-SN5YR @ c9a4fcaf; HD 2f57019d…, cov ffd3124b…). NOTE: this is the 2025 recalibration, NOT the DESY5 set used in DESI DR2.
- No CMB (BAO + SN only), stated.
Likelihood:
- BAO: χ² with the full covariance. D_M, D_H, D_V in units of c/H₀, times α = c/(H₀ r_d), profiled analytically (χ² is quadratic in α).
- SN: μ = 5 log₁₀((1 + z_hel) D_C) + const, with the offset marginalised analytically (Goliath et al. A9–12, as in the DES likelihood). Our own code; the downloaded script is not executed.
- Flat; Ω_r h² = 4.18 × 10⁻⁵ with h = 0.68 fixed in radiation only.
Models (best fit by grid + Nelder–Mead):
- M0 ΛCDM (Ω_m).
- M1 CPL (Ω_m, w₀, w_a).
- M2 Weave reverse thread, leading-order V = V_Λ(1 − 7.30e^{−βφ}), β = 2√2, frozen at a = 10⁻³ (Ω_m, amp; V_Λ by closure).
- M3 sign-switching ΛsCDM (Akarsu et al.): Ω_Λ → −Ω_Λ for z > z† (Ω_m, z†).
Reported: χ²_min and Δχ² versus ΛCDM. Reading set in advance:
- "negative space" (M3) is PREFERRED over the Weave thread (M2) if χ²(M3) < χ²(M2) − 2 (one parameter each beyond ΛCDM).
- M2 vs M1: Δχ² ≤ 2.3 means the thread captures most of what CPL gains.
- Sanity: ΛCDM best-fit Ω_m must land in [0.28, 0.34] for BAO + SN, else STOP and debug before reporting any model comparison.
Script: field_tests/scripts/realdata/run.py (runs in the background).
