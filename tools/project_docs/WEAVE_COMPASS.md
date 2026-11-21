# The Weave compass (Danny 16:06): every measurement fingerprinted with a direction and a vector

Legend: ● on target (inside the bar by > 0.3 dex or < 1σ); ◔ passes but thin; ↑! / ↓! fails now and must move up / down; ↑ / ↓ (data) outside 1σ; ○ prediction, input or info (no pull). Corrected after referee D1935. Headroom is in σ (data) or dex (bounds); smaller means tighter.

| # | ring | notch | quantity | value | dir | headroom | knobs it pulls | source | note |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0 | centre: rung step | |u| one-spurion window (bisected to 2e-10) | 0.02663 | ○ |  | — | D1932/D1932a | window [0.02588, 0.02740], width x1.059, ONE fixed assignment, f7 22-23 %, fJ 61-66 %. Contains 0.027 BY CONSTRUCTION (search started there, D1935); upper edge is a x2-cut artefact; window non-monotone (0.0203 isolated point) |
| 2 | 0 | centre: rung step | |u| single-flavon window centre (U32) | 0.09656 | ○ |  | — | D1928 | SECONDARY window, assignment varies |
| 3 | 0 | centre: rung step | lepton slip / down slip | 0.9768 | ● | 1.54 σ | u 0 | v4 (D1832) | same-lock fit; conflicts with Koide at rho |
| 4 | 1 | quarks | f7 (two-size lock) | 0.1802 | ● | 0.56 dex | u_u 0, u_d 0 | d1829_cp.json | PHENOMENOLOGICAL |
| 5 | 1 | quarks | fJ | 0.3077 | ◔ | 0.19 dex | — | d1829_cp.json | PHENOMENOLOGICAL |
| 6 | 1 | neutrinos | ratio natural fraction | 0.0133 | ◔ | 0.12 dex | flux(4,4,8) 0 | d1821_neutrino.json | thin: 0.12 dex headroom |
| 7 | 1 | neutrinos | M_N vs leptogenesis window top | 1.844e+11 | ● | 1.13 dex | n_theta 0, tan_beta + | v4 (D1822) |  |
| 8 | 1 | neutrinos | M_N vs window bottom | 1.844e+11 | ● | 0.61 dex | — | v4 (D1822) |  |
| 9 | 1 | leptons | Koide delta | 0.2222 | ○ |  | — | v4 | TRUST |
| 10 | 2 | spectrum | wino M2 [GeV] vs 700 GeV (ATLAS+CMS, 2507.15934) | 686.5 | ↑! | -0.01 dex | m3/2 + | D1947: bar 660 (ATLAS 2201.02472) - 700; INDETERMINATE | on the collider edge |
| 11 | 2 | spectrum | gluino M3 [GeV] | 4926 | ● | 0.33 dex | m3/2 + | v4 |  |
| 12 | 2 | forces | alpha_s(M_Z) single-stack (no threshold, +top-Yukawa 2-loop) | 0.114 | ↑ | -1.75 σ | Delta3 threshold + | D1944 (th err 0.00057); valid only under the single-stack assumption (D1942) | d alpha_s / d ln m3/2 = -0.00290 (measured, ±10 %): wants m3/2 DOWN; opposes the wino arrow |
| 13 | 2 | forces | Delta3 after Higgs pair + gauge | -0.09424 | ↑! | 0.28 dex | b_prime -, brane threshold + | v4 (D1881b) | needs +0.044 more |
| 14 | 2 | forces | alpha_s with S at i (self-consistent spectrum) | 0.1112 | ↑ | -5.56 σ | S vacuum rho | D1929 | S at i pushes the wrong way |
| 15 | 2 | forces | S-T seam: supergravity-form threshold (non-universal part) | 1e-09 | ↑! | -7.64 dex | non-universal threshold +, split stacks (f3 != f2) + | D1938 (Conlon-Palti 0901.4350) | universal on one stack: cancels in Delta3; plotted as 1e-9 |
| 16 | 2 | forces | proton lifetime [yr] | 1.6e+35 | ● | 0.82 dex | M12 + | v4 |  |
| 17 | 3 | inflation | n_s | 0.9706 | ● | 1.19 σ | — | v4 | inside its band (0.8σ): no pull counted (D1935); N* = 50.3 not yet cross-checked against T_R |
| 18 | 3 | inflation | n_s with S at i | 0.9704 | ● | 1.11 σ | S vacuum rho | D1926 |  |
| 19 | 3 | inflation | r | 0.00054 | ● | 1.82 dex | — | v4 |  |
| 20 | 3 | cosmology | T_R vs M_N (thermal leptogenesis) | 3.7e+08 | ○ |  | — | v4 (D1897) | a bound the model sidesteps (non-thermal leptogenesis): NOT a pull (D1935) |
| 21 | 3 | cosmology | non-thermal leptogenesis: derived Br(phi->NN) vs 9.5 % needed | 0.051 | ↑! | -0.27 dex | p in M_N ∝ (Re S)^p +, S-coupled hidden gauge groups - | D1946a (64 pi; best case p=3, SM only) | FAILS even at p=3 after the factor-2 fix; other channels only lower it |
| 22 | 3 | cosmology | gravitino lifetime vs BBN (A8) | 0.0014 | ● | 1.85 dex | — | D1946 | decays before BBN |
| 23 | 2 | spectrum | lightest stabilised modulus vs 30 TeV (F10) | 2.58e+05 | ● | 0.93 dex | — | D1946 |  |
| 24 | 2 | forces | A3/A2 needed 0.752 vs fixed-point ratio 3/4 | 0.75 | ○ |  | — | D1946a: UNCONSTRAINED COINCIDENCE (target ±8 %, ~50 % chance) | no mechanism; fixed points enter ln A additively |
| 25 | 3 | cosmology | non-thermal wino Omega from gravitinos (Omega ∝ T_R) | 0.01966 | ● | 0.79 dex | T_R - | D732 (Y3/2 ∝ T_R) | D732: Omega 0.017 at T_R 3.2e8 (M2 0.66 TeV), 0.11 at 3.0e9 ⇒ T_R capped at ~3e9 |
| 26 | 3 | cosmology | Delta N_eff | 1e-06 | ● | 5.23 dex | — | v4 | 0 exactly; plotted as 1e-6 |
| 27 | 3 | cosmology | dark-matter mass [GeV] | 12.8 | ○ |  | — | v4 |  |
| 28 | 4 | reverse | alpha drift zeta | 3.785e-10 | ● | 3.64 dex | b_bf - | v4 (D1887) |  |
| 29 | 4 | reverse | thread slope lambda (DESI needs ~0.95) | nan | ○ |  | — | D1906 | OPEN: non-Kähler only |

## Where it points (per knob)

- **tan_beta**: wants ↑ from neutrinos: M_N vs leptogenesis window top; wants ↓ from none.
- **m3/2**: wants ↑ from spectrum: wino M2 [GeV] vs 700 GeV (ATLAS+CMS, 2507.15934); spectrum: gluino M3 [GeV]; wants ↓ from none.
- **Delta3 threshold**: wants ↑ from forces: alpha_s(M_Z) single-stack (no threshold, +top-Yukawa 2-loop); wants ↓ from none.
- **b_prime**: wants ↑ from none; wants ↓ from forces: Delta3 after Higgs pair + gauge.
- **brane threshold**: wants ↑ from forces: Delta3 after Higgs pair + gauge; wants ↓ from none.
- **non-universal threshold**: wants ↑ from forces: S-T seam: supergravity-form threshold (non-universal part); wants ↓ from none.
- **split stacks (f3 != f2)**: wants ↑ from forces: S-T seam: supergravity-form threshold (non-universal part); wants ↓ from none.
- **M12**: wants ↑ from forces: proton lifetime [yr]; wants ↓ from none.
- **p in M_N ∝ (Re S)^p**: wants ↑ from cosmology: non-thermal leptogenesis: derived Br(phi->NN) vs 9.5 % needed; wants ↓ from none.
- **S-coupled hidden gauge groups**: wants ↑ from none; wants ↓ from cosmology: non-thermal leptogenesis: derived Br(phi->NN) vs 9.5 % needed.
- **T_R**: wants ↑ from none; wants ↓ from cosmology: non-thermal wino Omega from gravitinos (Omega ∝ T_R).
- **b_bf**: wants ↑ from none; wants ↓ from reverse: alpha drift zeta.

## Interactions (where two arrows meet one knob)

- **m3/2 cannot fix α_s.** Closing α_s needs Δ ln m3/2 = -1.31 (m3/2 ×0.27). That puts the wino at 185 GeV, far below the 660 GeV bar, which already has only 4 % room. So α_s must come from a threshold (Δ₃), not from the spectrum.
- **T_R is boxed, not pulled (corrected D1935).** Gravitino→wino production caps T_R at ~3e9 GeV (Ω ∝ T_R; 0.11 at 3e9, D732). Thermal leptogenesis (T_R ≳ M_N) is a bound the model sidesteps, and n_s already sits inside its band. So T_R cannot rise 3 dex, and leptogenesis must be non-thermal. The earlier "two arrows agree, T_R ~ 1e11–1e12" is withdrawn.
- **u (corrected D1935):** the one-spurion window [0.02588, 0.02740] is narrow (×1.059) and has one fixed charge pattern, natural throughout. That it contains 0.027 is by construction (the search started there), so it is not a convergence. u_d = 0.02587 still fails by 0.05 %. The window is non-monotone in u (isolated point 0.0203; U32 0.063–0.148).

Knob convention: "+" means this measurement wants the knob raised, "−" lowered.

Measured: dα_s/d ln m₃/₂ = -0.00290; dn_s/dN* = 5.84e-04.
