# Janus genesis card — scalar field → reheating → matter → light elements → dark energy (19 Nov 2026, D1647)

Every number is copied from the json named in its row and machine-checked by field_tests/scripts/janus_g/g10_card_check.py (D1647). Values are rounded as typed.

| quantity | value | file | key |
|---|---|---|---|
| n_s (SERAPIS v3, D = 10) | 0.97064 | field_tests/results/D1637_G1_reheat.json | base.ns |
| r | 5.407e-4 | field_tests/results/D1637_G1_reheat.json | base.r |
| N_* | 50.37 | field_tests/results/D1637_G1_reheat.json | base.Nstar |
| V∞^{1/4} (GeV) | 4.93e15 | field_tests/results/D1637_G1_reheat.json | Vinf_quarter_GeV |
| V''(ρ)/V∞ (D = 10) | 0.25 | field_tests/results/D1641_G1b_rho_curvature.json | rows.0.Vpp |
| V''(ρ)/V∞ (D = 6) | 0.125 | field_tests/results/D1641_G1b_rho_curvature.json | rows.2.Vpp |
| inflaton mass m (GeV) | 5.00e12 | field_tests/results/D1637_G1_reheat.json | m_GeV |
| T_R, κ = 1/(8π) (GeV) | 7.72e8 | field_tests/results/D1637_G1_reheat.json | TR_band.kappa_1_over_8pi |
| T_R, κ = 1 (GeV) | 3.87e9 | field_tests/results/D1637_G1_reheat.json | TR_band.kappa_1 |
| reheating verdict | CONSISTENT | field_tests/results/D1637_G1_reheat.json | verdict |
| η (baryon-to-photon) | 6.13e-10 | field_tests/results/GENESIS_MATTER/out.json | eta |
| m_DM at equal sharing (GeV) | 5.03 | field_tests/results/GENESIS_MATTER/out.json | T1.1 |
| ξ, minimal dark sector | 0.465 | field_tests/results/D1646_G6_dark_radiation.json | B_minimal_ADM.xi |
| ΔN_eff, minimal dark sector | 0.206 | field_tests/results/D1646_G6_dark_radiation.json | B_minimal_ADM.dneff |
| ΔN_eff, minimal sector: pull vs N_eff = 2.990 ± 0.070 (σ) | 3.72 | field_tests/results/D1654_G6b_channels.json | scenarios.S1_democratic.pull_2603 |
| max reheating share to the dark side (2σ) | 0.0215 | field_tests/results/D1654_G6b_channels.json | f_max_2sigma.S1_democratic |
| ΔN_eff, full mirror copy | 7.40 | field_tests/results/D1646_G6_dark_radiation.json | A_full_mirror.dneff |
| Y_p (BBN v3) | 0.2421 | field_tests/results/GENESIS_MATTER/bbn3.json | base.Yp |
| D/H | 2.59e-5 | field_tests/results/GENESIS_MATTER/bbn3.json | base.D_H |
| ³He/H | 1.03e-5 | field_tests/results/GENESIS_MATTER/bbn3.json | base.He3_H |
| Li/H | 4.35e-10 | field_tests/results/GENESIS_MATTER/li7.json | base.Li_H |
| lithium problem factor (vs Spite plateau) | 2.72 | field_tests/results/GENESIS_MATTER/li7.json | problem_factor |
| w₀ (exact-shape thread, best; Gaussian approximation, D1638) | -0.789 | field_tests/results/D1638_G2_thread_shape.json | best.w0 |
| w_a | -0.355 | field_tests/results/D1638_G2_thread_shape.json | best.wa |
| w₀, FULL likelihood (D1636, DESY5, compressed-CMB arm) | -0.872 | field_tests/results/D1636/rt10_desy5.json | cpl_fit.w0 |
| w_a, FULL likelihood (D1636, DESY5) | -0.212 | field_tests/results/D1636/rt10_desy5.json | cpl_fit.wa |
| w₀, FULL likelihood (D1636, Pantheon+) | -0.934 | field_tests/results/D1636/rt10_pantheonplus.json | cpl_fit.w0 |
| w₀, FULL likelihood (D1636, Union3) | -0.856 | field_tests/results/D1636/rt10_union3.json | cpl_fit.w0 |
| worst DESI Δχ² (≤ 6.18 passes; Gaussian approximation — superseded by D1636) | 5.64 | field_tests/results/D1638_G2_thread_shape.json | best.dmax |
| start-window probability (10D) | 0.0035 | field_tests/results/GENESIS_DE/rc2.json | beta=2.8284.P_window |
| acceleration ends at a | 1.23 | field_tests/results/D1644_G9_thread_future.json | end_of_acceleration.a |
| thread late ⟨w⟩ | -0.0175 | field_tests/results/D1644_G9_thread_future.json | late_w_mean |
| thread matter-like rule | PASS | field_tests/results/D1644_G9_thread_future.json | R1_matter_like |

Reading: one scalar field (the string coupling) drives inflation, ends at ρ with a bend fixed by symmetry ((D−2)/32), decays at T_R ~ 10⁹ GeV; one asymmetry gives both matter kinds (5 GeV dark baryon), a small dark sector with a massless dark photon is EXCLUDED by today's N_eff data (ΔN_eff ≈ 0.2 is 3.7σ high, D1654) unless the dark photon is massive or the dark side gets ≤ 2 % of the reheating energy; the light elements come out at textbook values (lithium problem inherited, not solved); the same curve at a far lower height is today's thawing dark energy (w₀ ≈ −0.79, w_a ≈ −0.36), (Gaussian-approximation fit; the full likelihood (D1636, other chat) prefers a less-thawed thread, w₀ ≈ −0.86 … −0.93 with w_a ≈ −0.1 … −0.24, and only DESY5 clearly prefers it over Λ (primary arm ΔAIC −7.4; Pantheon+ +0.7, Union3 −0.6)), which stops accelerating at a ≈ 1.23 for the D1638 start and ends as matter at the image of τ = i.
Open, stated: the decay strength κ; equal sharing per particle (A-dem); the dark/visible sharing factor and the asymmetry source (other chat, C3/C4); the ~1-in-300 start (D1642); V_Λ's size (by hand); D1636 full-likelihood fit pending.
