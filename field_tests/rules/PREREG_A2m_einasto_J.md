# PREREG A2m — 1 TeV wino vs the H.E.S.S. IGS line limit for the Einasto Gaia DR3 haloes of Singh & Desai — locked 2026-11-17, before code or run
Convention, pinned from arXiv:2605.16994v1 Eq. (22): ρ = ρ0 exp[−(2/α)((r/r_c)^α − 1)], so ρ(r_c) = ρ0. This is identical to the jfactor.einasto(r_c, α) shape.
Table A1 medians, ρ0 [1e7 M☉ kpc⁻³], r_c [kpc], α:
- B0/D1: (0.80, 15.29, 1.01)
- B0/D2: (0.83, 14.84, 0.45)
- B0/D3: (0.55, 16.69, 1.35)
- B0/D4: (1.00, 14.29, 0.74)
- B1/D2: (0.57, 15.97, 0.43)
Method: identical to a2l_burkert_J.py.
- ρ☉ = ρ(R0 = 8.178 kpc); J in the 0.5–3° annuli / J_bench.
- 1 TeV LO/NLO line with NLL band factors (0.794, 0.658); limit 2.3e-28.
- f_pred = serapis_inputs.wino_fraction(1.0) = [0.124, 0.205].
Verdicts as in A2l: PASS / BAND-DEP / FAIL.
