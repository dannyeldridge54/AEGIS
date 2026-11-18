
## 17 Nov 2026 day (CT) — Hyperion + nonstop Djl loop (session 014Gbst…; D1052–D1102)
- Names (Danny): **Chronos Clock** = string/early-universe calculator (tools/janus_calc). **Hyperion** = late-universe + astrophysics calculator (tools/janus_lt + tools/janus_astro). docs/TOOL_NAMES.md.
- Hyperion 1.0 built (A0–A8d, D1052–D1078) and packaged in releases/hyperion-1.0 (+zip). NOT uploaded: needs Danny's "Publish" and a linked PC.
- Wiring: W1 Chronos⇄Hyperion (D1079); W2 Mapper⇄Milky Way⇄wino (D1080); B2 Chronos→BBN (D1085); W4 EoS→Λ→GW (D1099). Toolkit atlas docs/TOOLKIT_ATLAS_333.md.
- Nonstop 3-min Djl loop (Danny: "continue Janus djl no stopping"), rotating A dark-matter / B first-minutes / C Galaxy / D roadmap. Results D1081–D1102:
  - A:
    - Wino vs Planck CMB: excluded only near the resonance (~2.0–2.7 TeV); matches the literature 2.18–2.5 (D1081, D1084).
    - LO resonance reproduces Beneke+2020 (2.2855 vs 2.282, D1087).
    - NLO module built; NOT VALIDATED as locked (2.394 vs 2.419; √2 convention gives 2.423, post hoc) (D1091, D1095).
    - Thermal wino vs CMB is marginal at NLO / high f_eff [estimate].
  - B:
    - BBN module, SERAPIS Y_p and D/H consistent (D1082).
    - GW ΔN ≤ 7e-12 (D1085).
    - τ=i hidden sector: U(1) OK; SU(2) in tension with ACT DR6 N_eff 2.86±0.13 (D1088, D1092).
    - D/H 1.7σ and Li-7 ×3.1 are SM-level; SERAPIS neutral (D1096, D1100).
  - C:
    - Jeans module (D1083).
    - Halo-star dispersions (D1089), Gaia-era masses (D1093) and M200 (D1097) bound the halo amplitude to ~0.8–1.1.
    - Dust prep: R_G CV18 coded; maps need the PC.
  - D:
    - NS module VALIDATED after finding that the referee's tolerance was the bug (D1090, D1094).
    - GW tides 5PN+6PN vs LAL 8.8e-10 rad (D1098).
    - SLy vs AP4 needs SNR 35–41 (D1101).
    - Hyperion 1.1 draft notes in releases/hyperion-1.1/CHANGES_SINCE_1.0.md (D1102). This is a major rung for Hyperion; awaiting "Publish".
- Open: A1e (blind NLO check), dust/Mapper per-star data (PC), Li-7 calculator, 3PN spin–spin.

## Update 16:55 UTC (D1103–D1115)
- A:
  - NLO CMB band ends at 2.76 TeV; the thermal wino is allowed (D1103).
  - γγ line: SERAPIS-E 1 TeV passes H.E.S.S. with ~×2 margin for every Milky Way model (D1110, D1114). D1112a corrected.
- B:
  - Three BBN codes agree (D1107); bbn_net LINX module VALIDATED (D1109).
  - Y_p convention bug fixed (D1082a, via D1106).
  - Li-7 reproduced (D1104).
- C:
  - Escape speed confirmed at 2 r200 (D1108).
  - McMillan17 vs MWPotential2014: the MW data disagree; bracket M200 0.7–1.3e12 (D1105, D1112).
- D:
  - Tides 6/6.5PN validated. 7PN differs from LAL by 0.33%, explained (LAL coefficient via ripplegw), but which is correct is open (D1111, D1113, D1115).
- Hyperion 1.1 notes updated (releases/hyperion-1.1/CHANGES_SINCE_1.0.md). Still awaiting Danny's "Publish" and a linked PC.

## Update 17:55 UTC (D1116–D1128)
- KEY: the H.E.S.S. Inner Galaxy Survey (2026) line limit excludes SERAPIS-E's 1 TeV post-hoc wino except for the light MWPotential2014 halo at NLO. 0.66 TeV survives for realistic haloes. Post-hoc wino window ≈ 0.67–0.9 TeV, f ≈ 5–10% [estimate]; HL-LHC covers it (D1125, D1126, D1128).
- The v3.3 draft paragraph and the forward-table row are updated (unposted).
- NLL line machinery is in Hyperion (D1121, D1124). bbn_net τ=i scan (D1122). 7PN tide parked (D1120).
- Note: D1127 is another session's J7g note; mine are D1125, D1126 and D1128.

## Final update 18:32 UTC (D1129–D1145)
- All four loop sides are summarised and parked: A wino (D1143), B BBN/N_eff (D1144), C Galaxy (D1145), D roadmap (D-side note today).
- SERAPIS-E post-hoc wino: ≈ 0.67–0.9 TeV (f ≈ 5–10%); 1 TeV is undetermined (inner-halo concentration); HL-LHC reach 0.5–0.9 TeV.
- PC needed for: the Star Mapper orbit feed + per-star data, dust maps (downloads need Danny's OK), and the Zenodo upload of Hyperion 1.1 (needs "Publish").

## CORRECTION 18:50 UTC (D1152–D1153)
- The wino line verdicts in D1110–D1142 used the OLD D732 fractions (0.14/0.26/0.67), but the current SERAPIS-E wino is thermal (D784): f ≈ 0.05–0.09 (0.67 TeV), 0.12–0.21 (1 TeV), 0.42–0.70 (1.85 TeV).
- Re-scored: 0.67 TeV passes everywhere; 1 TeV passes for Gaia-calibrated haloes (marginal for the H.E.S.S. benchmark); 1.85 TeV fails.
- Window ≈ 0.67 to ~1–1.3 TeV (est.), f ≈ 5–20%. CTA (1 TeV cap ~7%) plus HL-LHC can close it.
- The v3.3 paragraph and table row are corrected (unposted).

## Evening update 22:20 UTC (D1156–D1201)
- **Relic module (Sommerfeld + freeze-out).**
  - Solvers validated:
    - two-channel open solver: free case, decoupled case, R-convergence, exact unitarity (D1158–D1180);
    - charged-pair resonance tower below threshold (D1159).
  - The threshold-averaging question is parked: it only affects a thin velocity band (D1180).
  - Thermal Sommerfeld factor at freeze-out, all charge sectors (Hisano matrices sourced): 1.29–1.37 (D1181–D1183).
  - Relic mass vs Beneke 2009.00640:
    - no boost: ours 2.325 TeV vs 2.207 (+5.4%), after the MS-bar α₂ fix;
    - LO Sommerfeld: ours 3.135 TeV vs 2.886 (+8.6%).
  - Remaining suspect: g_*(T). This needs Danny's OK to download the Saikawa–Shirai table ("yes table") (D1185–D1187).
- **Wino vs cored Gaia haloes (Singh & Desai 2605.16994):** the 1 TeV wino survives the H.E.S.S. IGS line limit for all 5 Burkert fits (3 PASS, 2 marginal at the upper fraction edge) (D1189–D1190). Window unchanged: 0.67 to ~1–1.5 TeV. No new collider or line limits (D1198).
- **Helium, LBT 2026 (Y_p = 0.2458 ± 0.0013), with theory errors (B8):**
  - SU(2)+gaugino hidden sector EXCLUDED at +3.1σ;
  - SU(2) at +1.7σ;
  - U(1) and base OK (D1191–D1192).
  - The D/H offset is the known theory dd-rate systematic (D1201).
- **Milky Way (Horta+2026, v_c☉ = 235.3):** MWPotential2014 FAILS (−4.3σ); McMillan17 PASSES (C8, D1193–D1194).
  - The Star Mapper orbit default is now McMillan17, via galpy with a consistent solar frame (D9, D10 tests PASS).
  - Legacy output is unchanged; new output goes to hyperion_mcm17/ (D1196–D1197).
- **SERAPIS v3.3 draft (unposted):** helium verdicts, the cored-halo sentence and 3 references added (D1199).
  - A full build needs revtex (on the PC).
- Plateau-origin rotation: NULL (D1188).
- **Waiting on Danny:**
  - "yes table" (g_* download);
  - a linked PC (Mapper run, revtex build, START_HYPERION_ORBITS.bat);
  - "Publish" (Zenodo).

## Overnight update 08:00 UTC 18 Nov (D1202–D1271)
- **Relic vs Beneke 2009.00640:**
  - The Saikawa–Shirai g_*(T) table is now in the repo: field_tests/data/saikawa_shirai_2020_gstar.dat, the PTArcade copy, checked against the IPMU original to < 0.01%. It was downloaded with Danny's "yes".
  - Born M_th = 2.252 TeV vs 2.207 (+2.0%, PASS; D1238).
  - LO Sommerfeld M_th = 3.013 vs 2.886 (+4.4%, PARKED).
  - The late-x tail and the velocity grid are ruled out (D1253, D1269). What is left needs Beneke's per-channel matrices: the Mathematica supplement of 1303.0200, which is not reachable here (D1259, D1266).
  - NOTE for the other loop: wino_window is no longer blocked on the g_* table (D1244).
- **Halo:** the 1 TeV wino survives H.E.S.S. IGS for all 10 Singh–Desai Gaia fits (8 PASS, 2 marginal; D1190, D1202).
- **Dark radiation:** N_eff 2026 (Goldstein–Hill) puts τ_i SU(2) at +3.1σ (D1208). SU(2)+gaugino is excluded by LBT Y_p (D1192). Both are in the v3.3 draft, unposted (D1199, D1209).
- **Galaxy:**
  - McMillan17 is the Star Mapper default (D1197). It passes Horta+2026 v_c, but its local slope is wrong in sign (D1203).
  - An NFW-only refit to Eilers+2019 was rejected (r_s ≈ 3 kpc; D1210).
- **GW:** the 7PN tidal coefficients match the independent Mandal et al. 2412.01706. LAL's 0.33% is the outlier (D1211).
- **Waiting on Danny:** a PC link for this session, or "hand off" to the PC session (Mapper run, revtex build); "Publish".
