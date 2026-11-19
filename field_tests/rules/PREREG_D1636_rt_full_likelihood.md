# PREREG D1636 — reverse thread (thawing species-plateau dark energy) vs ΛCDM and w₀w_aCDM, full BAO + SN likelihoods, compressed CMB

Locked before any number is computed. Danny 15:50 CT 19 Nov 2026: "Do that" (proper full-likelihood fit offered after D1626–D1628, which used a Gaussian approximation in the (w₀, w_a) plane).
Helper session's own run (not the P3 chat's locks; does not touch PREREG_GENESIS_DE*).

## Data (all public; fetched 19 Nov 2026 from github.com/CobayaSampler/bao_data and sn_data, read with Cobaya 3.6.2 likelihood classes)
- BAO: `bao.desi_dr2.desi_bao_all` (DESI DR2, full mean vector + covariance).
- SN (one at a time): `sn.pantheonplus`, `sn.union3`, `sn.desy5`, Cobaya defaults (absolute magnitude marginalised analytically).
- CMB: DESI DR2 (arXiv:2503.14738) Appendix A, Eqs. (A1)–(A2): Gaussian on (θ*, ω_b, ω_bc), mean (0.01041, 0.02223, 0.14208),
  covariance 1e-9 × [[0.006621, 0.12444, −1.1929], [0.12444, 21.344, −94.001], [−1.1929, −94.001, 1488.4]]. Main run uses the published mean as printed.
  Robustness (reported, not used for the verdict): θ* mean 0.0104110 (the paper's Eq. 16 value).

## Models (CAMB 2.0.5 background; Σm_ν = 0.06 eV, one massive; N_eff = 3.044; T_CMB 2.7255 K)
- ΛCDM: H₀, ω_b, ω_c.
- w₀w_aCDM: + w₀, w_a (CPL, DarkEnergyPPF; prior w₀ + w_a < 0, w₀ ∈ [−3, 1], w_a ∈ [−3, 2]).
- RT10 (main): + u_i ∈ (0, u_max). Field φ with V = V_Λ(1 − A e^{−βφ}), A = 16ζ(2)/(3ζ(3)) = 7.2983, β = 2√2; frozen at a = 1e-3 with A e^{−βφ_i} = u_i;
  V_Λ shot so that Ω_φ(a = 1) = 1 − Ω_m − Ω_r; scalar ODE in N = ln a with matter + radiation (massless-neutrino approximation inside the ODE only);
  w(a) passed to CAMB as a PPF w(a) table (w = −1 for a < 1e-3). u_max = largest u_i with V > 0 throughout (found numerically).
- RT6 (β = 2) and RT4 (β = √2): secondary, same method.

## Method
- Minimise total χ² = χ²_BAO + χ²_SN + χ²_CMB with scipy Nelder–Mead from 8 fixed starting points per model × SN set; keep the best. No MCMC.
- Report χ²_min per likelihood, Δχ² = χ²(model) − χ²(ΛCDM), ΔAIC = Δχ² + 2k (k = 2 for w₀w_a, 1 for RT), best-fit parameters, and RT's best (w₀, w_a) from a CPL fit to its w(a) over 0 < z < 2.
- Tuning flag for RT: fraction of the u_i range with Δχ² ≤ Δχ²_min + 1.

## Validation gate (reported first)
Our w₀w_a − ΛCDM Δχ² for each SN set is compared with DESI DR2 Table VI (−10.7 / −17.4 / −21.0, which used the FULL CMB, not the compressed prior).
PASS if each of ours is negative and within ±6 of DESI's value. If FAIL, the RT verdict is reported as "engine not validated".

## Verdicts (per SN set)
- RT preferred over ΛCDM if ΔAIC(RT) < 0; strongly if ΔAIC < −6.
- RT competitive with w₀w_a if AIC(RT) ≤ AIC(w₀w_a) + 2.
- Caveats stated in the note regardless of outcome: the model was formed after DESI DR2 (post-data); V_Λ is set by hand; compressed CMB, not full Planck/ACT.
- Fixes only through PREREG_D1636_rt_full_likelihood_DEVIATIONS.md, written before any rerun.
