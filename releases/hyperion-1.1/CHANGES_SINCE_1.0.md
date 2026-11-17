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

## Update 17 Nov 16:55 UTC (D1103–D1115)
### More validated
| Module | What it does | Checked against | Note |
|---|---|---|---|
| bbn_net | full BBN network (Y_p mass/nucleon, D, ³He, ⁷Li; ΔN_eff, τn, rate nuisances) on the LINX engine | PRIMAT table, PRyMordial, LINX: three codes agree (Y_p 3e-4, D/H 0.17%, Li 2.5%) | D1104, D1106, D1107, D1109 |
| gw tides 6.5PN | tail tidal term (Henry–Faye–Blanchet 2020) | LALSuite ≤ 9e-10 rad | D1111 |
| wino γγ line | absolute σv_γγ from the Sommerfeld vector; J-factors per Milky Way model | H.E.S.S. 2018 benchmark J within 5% | D1110, D1114 |
### Physics results
- Wino at NLO vs the CMB: band 2.18–2.62 TeV (f_eff 0.14) up to ≤ 2.76 TeV (0.41). The thermal wino (2.84–2.86) is allowed, with f_max ≥ 1.19 (D1103; the NLO convention was chosen post hoc).
- SERAPIS-E 1 TeV wino vs the H.E.S.S. γγ line: f_max 0.50–0.68 across the Milky Way bracket vs f = 0.26 → PASS with ~×2 margin (D1110, D1114).
- Milky Way: the data sets disagree. K-giant Jeans masses want a light halo; the escape speed and BHB stars want a heavy one. MWPotential2014 and McMillan17 bracket them: M200 ≈ 0.7–1.3e12 M_⊙, ρ_⊙ ≈ 0.29–0.39 GeV/cm³ (D1105, D1108, D1112).
- Li-7: 5.56–5.70e-10 from two networks; the lithium problem (factor ~3.5) is reproduced (D1104, D1107).
### Not validated / open
- 7PN tidal term: 0.33% coefficient difference vs LAL, fully explained (LAL's coefficient via ripplegw), but which is correct is open (D1111, D1113, D1115).
- NLO wino convention (√2) is still post hoc; no blind second number yet (D1095, D1099, D1103).
### Corrections
- D1082a: bbn.Yp is the nucleon fraction. The SERAPIS Y_p pull is +0.17σ (was +0.56σ); bbn.Yp_mass added.
- D1112a: the heavy-halo line estimate (f_max → 0.27) was mis-anchored; the real J-factors give 0.50–0.55.
- D1087 superseded by D1103: the "marginal" thermal wino is allowed at NLO.

## Update 17 Nov 17:55 UTC (D1116–D1128)
- NLL-resummed wino line (Ovanesyan–Slatyer–Stewart 2014): R = 0.71 at 1 TeV; robust to scale variation (D1121, D1124).
- H.E.S.S. Inner Galaxy Survey 2026 (line limit 2.3e-28 at 1 TeV) with its own geometry (25 annuli, 0.5°–3°; our benchmark J within 7.4%): SERAPIS-E's 1 TeV wino is excluded except for the light halo at NLO. 0.66 TeV passes for realistic haloes (bracketed). The wino window is ≈ 0.67–0.9 TeV (D1125, D1126, D1128).
- τ=i hidden sectors through bbn_net: D/H prefers ΔN ≈ 0.3, ACT excludes it; U(1) is OK (D1122).
- 7PN tidal term PARKED: pre/post-erratum HFB vs LAL, 0.33% (D1117, D1120).
- Corrections: D1118's and D1119's "one-loop ×3–4" columns were withdrawn by D1121.

## Final update 17 Nov 18:32 UTC (D1129–D1145)
- HL-LHC wino reach 0.5–0.9 TeV (D1131). N_eff forecasts: SO 0.045, CMB-S4 0.03 (D1136).
- Gaia DR3 v_esc profile → light halo, M200c 0.55e12 (D1139). 1 TeV wino verdict for that halo: FAIL (LO) / marginal (NLO); concentration-dominated (D1142, correcting D1139).
- Side summaries: A wino (D1143), B first minutes (D1144), C Galaxy (D1145). All parked at diminishing returns pending new data, the PC, or a new direction.

## Milky Way potential (D1193–D1195)
- Horta+2026 (arXiv:2601.18876) measures v_c(R☉) = 235.3 km/s. MWPotential2014 gives 219.5 (−4.3σ, FAIL); McMillan17 gives 233.2 (PASS, C8).
- New mapper_feed.orbit_params_galpy(pot=...) supports McMillan17 through galpy's C integrator. It reproduces our MWPotential2014 integrator to ≤ 6.4e-5 (D9, after a unit fix).
- The default is still MWPotential2014. Flipping it, together with the Sun's frame constants (R0 = 8.21, v0 = 233.1), is the next step.
