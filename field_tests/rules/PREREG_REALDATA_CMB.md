# PREREG_REALDATA_CMB — add the CMB: DESI DR2's compressed CMB prior on (θ*, ω_b, ω_bc) (locked D1694, 2026-11-20 01:25 UTC)
Prior (arXiv:2503.14738 App. A, eqs. A1–A2; from CamSpec, Lemos–Lewis): mean (θ*, ω_b, ω_bc) = (0.01041, 0.02223, 0.14208); covariance × 10⁻⁹ = [[0.006621, 0.12444, −1.1929], [0.12444, 21.344, −94.001], [−1.1929, −94.001, 1488.4]].
New parameters: h and ω_b (ω_bc = Ω_m h² − ω_ν, with ω_ν = 0.00064 for Σm_ν = 0.06 eV). Radiation from T_CMB = 2.7255 K, N_eff = 3.044.
- r_d: Aubourg et al. 2015 fit, r_d = 55.154 e^{−72.3(ω_ν + 0.0006)²}/(ω_bc^{0.25351} ω_b^{0.12807}) Mpc. BAO now uses c/(H₀ r_d) directly (no free α).
- θ* = r_s(z*)/D_M(z*), with z* from Hu–Sugiyama and r_s = ∫ c_s dz/H for z > z*. One CALIBRATION factor on θ*, fixed BEFORE any model fit: it makes Planck-2018 ΛCDM (h = 0.6736, ω_b = 0.02237, ω_c = 0.1200) give 100θ* = 1.04110. That factor must lie within 1 ± 0.005, else STOP.
- Dark energy above z = 2.5: frozen threads hold their z = 2.5 density; CPL is analytic; ΛsCDM is negative above z†.
Models: ΛCDM, CPL, Weave thread (β = 2√2), ΛsCDM, and the R1/R2 reversals (if R1/R2 beat the thread in PREREG_REALDATA_REVERSE, they are included; otherwise skipped).
Data: the same DESI DR2 BAO + DES Dovekie SN, plus this CMB prior.
Sanity: ΛCDM h ∈ [0.66, 0.70] and Ω_m ∈ [0.29, 0.33], else STOP.
Reading: report Δχ² versus ΛCDM. The thread is "supported" if Δχ² ≤ −4 with BAO + CMB + SN (it was −7.0 without the CMB).
Script: field_tests/scripts/realdata/cmb.py
