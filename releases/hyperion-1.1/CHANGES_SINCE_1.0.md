# Hyperion 1.1 — changes since 1.0 (DRAFT release notes; not packaged, not uploaded)
Status: draft, collected 17 Nov 2026 (D1081–D1101). Packaging and a Zenodo upload wait for Danny's "Publish" and a linked PC.

## New validated modules (locked tests passed)
| Module | What it does | Checked against | Note |
|---|---|---|---|
| bbn | helium Y_p and D/H from the baryon density and N_eff (wraps PRIMAT 2021 and PArthENoPE tables) | CAMB interpolators (lossless); the two codes agree on Y_p within 6e-4 | D1082 |
| jeans | spherical Jeans velocity dispersions (constant β) | galpy (1.5e-11), exact point-mass law (3e-16) | D1083 |
| ns (fixed) | neutron stars SLy/AP4: M–R, Love number, Λ | independent TOV code to 8e-11 after the referee's tolerance fix | D1090, D1094 |
| gw tides | TaylorF2 tidal phase 5PN + 6PN (Vines–Flanagan–Hinderer 2011) | LALSuite (≤ 8.8e-10 rad) | D1098 |
| sommerfeld (LO check) | wino resonance with the published couplings | Beneke–Szafron–Urban 2020: 2.2855 vs 2.282 TeV | D1087 |
| wiring | Chronos → BBN; EoS → Λ → GW phase | lossless | D1085, D1099 |

## Physics results with Hyperion (AEGIS applications)
- Wino vs Planck CMB: excluded only near the resonance (about 2.0–2.7 TeV). This matches the published band 2.18–2.5 TeV (D1081, D1084). At NLO the thermal wino is marginal at high f_eff (D1087, D1091).
- SERAPIS light elements: consistent in both codes (D1082). GW dark radiation ≤ 7e-12 (D1085). τ=i hidden sector: U(1) is fine, while SU(2) is in tension with ACT DR6 (D1088, D1092).
- Milky Way halo: halo-star dispersions, Gaia-era enclosed masses and M200 all favour MWPotential2014 within about ×0.8–1.1 (D1089, D1093, D1097).
- Neutron-star equation of state: SLy vs AP4 differ by 0.133 rad of tidal phase. Telling them apart needs SNR ≈ 35–41 (upper-bound forecast) (D1099, D1101).
- Shared Standard-Model open items that SERAPIS inherits unchanged: D/H at 1.7σ (D1096) and Li-7 at a factor of 3.1 (D1100).

## Not validated as locked (kept on record)
- NLO wino potential: the pre-declared convention gives 2.394 vs 2.419 TeV (−1.02%; the lock was 1%). The √2 convention gives 2.423, consistent but chosen after seeing that number (D1091, D1095). A blind second check is open (A1e).
- The A3a–A3d neutron-star cross-checks failed on the referee's tolerance, not on Hyperion. Resolved in D1094.

## Corrections made in this period
- D1082 → D1096: the PArthENoPE table shipped with CAMB is stale for D/H. The real gap between the two codes is about 2.8%, not 5.6%.
- D1088 → D1092: the ACT allowance for extra radiation is tighter (ΔN < 0.066–0.076 at 2σ).
- D1099 → D1101: the SNR needed to tell SLy from AP4 is 35–41, not about 8.
- D1086 → D1090: the neutron-star mismatch came from the referee's tolerance (the surface-definition diagnosis was wrong).

## Still blocked
- Dust maps and the per-star Star Mapper data (need Danny's PC).
- 3PN spin–spin terms (A2b2), realistic stars (A1), a Li-7 calculator.
