# PREREG D2130: the Weave UFE v4 built as a ΛCDM-format cosmology ("our world in standard parts"), scored on compressed Planck 2018 + DESI DR2 BAO. Ping-pong: referee RW-1…RW-5 folded in. Locked before computing.

## Standard parts → Weave source
| Part | Value | Status |
|---|---|---|
| Curvature | Ω_k = 0 | [P], inflation |
| Photons | T_CMB = 2.7255 K | standard input |
| Neutrinos | N_eff = 3.044 (ΔN_eff ≈ 0, brane split, [P]). **Σm_ν = 0.0587 eV**, 3 massive, normal ordering (m₁ ≈ 0) (Weave seesaw/TM1, [D]) | |
| Baryons | ω_b | **free** (η_B, leptogenesis window, is an input) |
| CDM | ω_c | **free**. m_X = 12.8 GeV is derived *from* Ω_DM/Ω_b; the non-thermal wino (~0.02) sits *inside* ω_c |
| Dark energy | the reverse thread V = V_L(1 − A e^{−βφ}), A = 16ζ(2)/(3ζ(3)) = 7.30, β = 2√2 (the code already used in cmb-fit/rt_planck_fit.py, D1636). Exact w(a) table → CAMB DarkEnergyPPF (**RW-1**: no CPL inside the fit). Start amplitude u_i **free**; V_L by flatness | |
| Primordial | **n_s = 0.9706 fixed**, α_s = −9.7e-4, r = 5.4e-4 | [P/D] |
| A_s, τ | — | unconstrained by these data (RW-2) |
| DM–DE coupling | b_A = 0 | consistent with full Planck (D1713ff); keeps the priors valid |

## Data
- **Planck 2018 distance priors, 4-parameter version** (Chen–Huang–Wang, arXiv:1808.05724, Table 1, verified via ar5iv): R = 1.7502 ± 0.0046, ℓ_A = 301.471 ± 0.0895, ω_b = 0.02236 ± 0.00015, n_s = 0.9649 ± 0.0043, with the printed 4×4 correlation matrix. z* from the Hu–Sugiyama fit, R = √(Ω_m H0²) D_M(z*)/c, ℓ_A = π D_M(z*)/r_s(z*).
- **DESI DR2 BAO** (arXiv:2503.14738, Table IV, as fetched by the referee): BGS D_V/r_d; six bins of (D_M/r_d, D_H/r_d) with r_{M,H}. D_V is not double-counted.
- **SN: none in this lock.** A Pantheon+/DES-Y5 extension needs Danny's download OK and gets its own lock.

## Not testable with these data (stated up front, RW-2)
r, α_s, A_s, τ, lensing, birefringence β ≈ 0.28°.

## Models (minimised with Nelder–Mead from 4 starts; the best is kept)
| Model | Free parameters | Fixed |
|---|---|---|
| M1 ΛCDM | ω_b, ω_c, H0, n_s | Σm_ν = 0.06 |
| M2 **Weave** | ω_b, ω_c, H0, u_i | everything else per the card |
| M3 Weave-a-priori | ω_b, ω_c, H0 | u_i = 0.1129 (the stored full-Planck+DESI+Pantheon+ best fit, cmp_rtP.json) |
| M4 Weave with CPL proxy (−0.79, −0.36) | ω_b, ω_c, H0 | reported only, to show the proxy bias |
| M5 ΛCDM with Weave n_s and Σm_ν | ω_b, ω_c, H0 | isolates the DE effect |
| M6 w0waCDM | ω_b, ω_c, H0, n_s, w0, wa | reference |

## Output
χ² by block, Δχ² and ΔAIC versus M1. Derived: H0, Ω_m, r_d, the thread's w0/wa from a CPL fit of its w(a) over z < 2, and the n_s pull.

## Verdict rules
- The Weave is **CONSISTENT** if ΔAIC(M2 vs M1) ≤ +2.
- **DISFAVOURED** if ΔAIC > +6.
- **PREFERRED** if ΔAIC < −2.
- The n_s-fixed test is reported in σ.
