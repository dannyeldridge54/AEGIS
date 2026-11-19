# PREREG_D1659_G6D_DP_STRIP — where is the massive dark photon still allowed? (Janus genesis G6d; locked 2026-11-19 ~23:55Z before any number)
Approximate exclusion bands [literature, read this tick; band edges are approximate and mass-dependent — stated, not refined]:
- Colliders (LHCb, BaBar, NA48/2, A1, KLOE): ε ≳ 1e-3 excluded for 0.01–10 GeV (2511.03883; BaBar ε ≲ 1e-3 for 0.02–10.2 GeV, PoS 350/182).
- Beam dumps / fixed target (E137, E141, E774, NA64, NA62): 1e-7 ≲ ε ≲ 1e-3 for m below "a few GeV" (2005.01515, 2511.03883) — taken as m ≤ 3 GeV.
- SN1987A: ε ≈ 1e-10 – 1e-6 excluded for m ≲ 100 MeV (1612.07295; mass range 1611.03864).
- BBN floor (D1657): ε > ε_min(m) for τ < 1 s, ε_min from D1657's json (interpolated in log m).
Window from D1657: 1.022 MeV < m < 5030 MeV.
Compute at m = 2, 10, 50, 100, 300, 1000, 3000, 5000 MeV: the allowed ε intervals = (ε_min(m), 1e-3) minus the bands that apply at that m. Report each open interval and its width in decades.
Reading (locked): strip OPEN at a mass if an interval ≥ 1 decade remains; the P-M dark photon is "allowed" if any mass is OPEN. Band edges are approximate ⇒ intervals touching a band edge within a factor 3 are reported as "marginal".
Script: field_tests/scripts/janus_g/g6d_dp_strip.py → field_tests/results/D1659_G6d_dp_strip.json
