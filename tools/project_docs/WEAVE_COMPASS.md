# The Weave compass (Danny 16:06): every measurement fingerprinted with a direction and a vector

Legend: ● on target (inside the bar with margin); ↑ / ↓ the value must move up / down; ! the bar fails now; ○ prediction or input (no target yet). Headroom is in σ (data) or dex (bounds); smaller means tighter.

| # | ring | notch | quantity | value | dir | headroom | knobs it pulls | source | note |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0 | centre: rung step | |u| one-spurion window centre (7-null converged) | 0.02663 | ● | 1.54 σ | u 0 | D1932 | window [0.02588, 0.02740] contains the median; one fixed assignment; f7 22-23 %, fJ 61-66 % |
| 2 | 0 | centre: rung step | |u| single-flavon natural window centre | 0.09656 | ↓ | -55.97 σ | u + | D1928 | SECONDARY window (U32, assignment varies); primary one-spurion window sits on the median (D1932) |
| 3 | 0 | centre: rung step | lepton slip / down slip | 0.9768 | ● | 1.54 σ | u 0 | v4 (D1832) | same-lock fit; conflicts with Koide at rho |
| 4 | 1 | quarks | f7 (two-size lock) | 0.1802 | ● | 0.56 dex | u_u 0, u_d 0 | d1829_cp.json | PHENOMENOLOGICAL |
| 5 | 1 | quarks | fJ | 0.3077 | ↑ | 0.19 dex | — | d1829_cp.json | PHENOMENOLOGICAL |
| 6 | 1 | neutrinos | ratio natural fraction | 0.0133 | ↑ | 0.12 dex | flux(4,4,8) 0 | d1821_neutrino.json | thin: 0.12 dex headroom |
| 7 | 1 | neutrinos | M_N vs leptogenesis window top | 1.844e+11 | ● | 1.13 dex | n_theta 0, tan_beta + | v4 (D1822) |  |
| 8 | 1 | neutrinos | M_N vs window bottom | 1.844e+11 | ● | 0.61 dex | — | v4 (D1822) |  |
| 9 | 1 | leptons | Koide delta | 0.2222 | ○ |  | — | v4 | TRUST |
| 10 | 2 | spectrum | wino M2 [GeV] | 686.5 | ↑ | 0.02 dex | m3/2 + | v4 | marginal: wants m3/2 UP |
| 11 | 2 | spectrum | gluino M3 [GeV] | 4926 | ● | 0.33 dex | m3/2 + | v4 |  |
| 12 | 2 | forces | alpha_s(M_Z) no threshold | 0.1142 | ↑ | -2.22 σ | m3/2 -, Delta3 threshold + | D1929 run 1 (gluino 4.93 TeV) | d alpha_s / d ln m3/2 = -0.00290 (measured, ±10 %): wants m3/2 DOWN; opposes the wino arrow |
| 13 | 2 | forces | Delta3 after Higgs pair + gauge | -0.09424 | ↑! | 0.28 dex | b_prime -, brane threshold + | v4 (D1881b) | needs +0.044 more |
| 14 | 2 | forces | alpha_s with S at i (self-consistent spectrum) | 0.1112 | ↑ | -5.56 σ | S vacuum rho | D1929 | S at i pushes the wrong way |
| 15 | 2 | forces | proton lifetime [yr] | 1.6e+35 | ● | 0.82 dex | M12 + | v4 |  |
| 16 | 3 | inflation | n_s | 0.9706 | ● | 1.19 σ | N* +, T_R + | v4 | Δn_s needed +0.0022 ⇒ ΔN* ≈ +2.8 ⇒ T_R up |
| 17 | 3 | inflation | n_s with S at i | 0.9704 | ● | 1.11 σ | S vacuum rho | D1926 |  |
| 18 | 3 | inflation | r | 0.00054 | ● | 1.82 dex | — | v4 |  |
| 19 | 3 | cosmology | T_R vs M_N (thermal leptogenesis) | 3.7e+08 | ↑! | -2.70 dex | T_R +, M_N - | v4 (D1897) | fails by 2.7 dex ⇒ non-thermal; T_R arrow agrees with n_s |
| 20 | 3 | cosmology | Delta N_eff | 1e-06 | ● | 5.23 dex | — | v4 | 0 exactly; plotted as 1e-6 |
| 21 | 3 | cosmology | dark-matter mass [GeV] | 12.8 | ○ |  | — | v4 |  |
| 22 | 4 | reverse | alpha drift zeta | 3.785e-10 | ● | 3.64 dex | b_bf - | v4 (D1887) |  |
| 23 | 4 | reverse | thread slope lambda (DESI needs ~0.95) | nan | ○ |  | — | D1906 | OPEN: non-Kähler only |

## Where it points (per knob)

- **u**: wants ↑ from centre: rung step: |u| single-flavon natural window centre; wants ↓ from none.
- **tan_beta**: wants ↑ from neutrinos: M_N vs leptogenesis window top; wants ↓ from none.
- **m3/2** — TENSION: wants ↑ from spectrum: wino M2 [GeV]; spectrum: gluino M3 [GeV]; wants ↓ from forces: alpha_s(M_Z) no threshold.
- **Delta3 threshold**: wants ↑ from forces: alpha_s(M_Z) no threshold; wants ↓ from none.
- **b_prime**: wants ↑ from none; wants ↓ from forces: Delta3 after Higgs pair + gauge.
- **brane threshold**: wants ↑ from forces: Delta3 after Higgs pair + gauge; wants ↓ from none.
- **M12**: wants ↑ from forces: proton lifetime [yr]; wants ↓ from none.
- **N***: wants ↑ from inflation: n_s; wants ↓ from none.
- **T_R**: wants ↑ from inflation: n_s; cosmology: T_R vs M_N (thermal leptogenesis); wants ↓ from none.
- **M_N**: wants ↑ from none; wants ↓ from cosmology: T_R vs M_N (thermal leptogenesis).
- **b_bf**: wants ↑ from none; wants ↓ from reverse: alpha drift zeta.

## Interactions (where two arrows meet one knob)

- **m3/2 cannot fix α_s.** Closing α_s needs Δ ln m3/2 = -1.31 (m3/2 ×0.27). That puts the wino at 185 GeV, far below the 660 GeV bar, which already has only 4 % room. So α_s must come from a threshold (Δ₃), not from the spectrum.
- **T_R: two independent arrows agree.** Thermal leptogenesis needs T_R ≳ M_N = 1.8e11 GeV (×500 up). n_s at the data centre needs ΔN* ≈ +2.8, which means T_R ≈ 1.6e+12 GeV (×4227 up, with dN*/d ln T_R = 1/3 for w = 0 reheating, an estimate). Both point to **T_R ~ 1e11–1e12 GeV**, about 3 decades above the derived 3.7e8.
- **u: flavour sits ON the median (D1932).** The 7-null converged one-spurion window [0.02588, 0.02740] contains the six-sector median 0.027 (its centre 0.02663 is 1.4 % below). One fixed charge pattern covers it, natural throughout. The broad single-flavon window (0.063–0.148, U32) is secondary.

Knob convention: "+" means this measurement wants the knob raised, "−" lowered.

Measured: dα_s/d ln m₃/₂ = -0.00290; dn_s/dN* = 7.90e-04.
