# PREREG_D1654_G6B_CHANNELS_NEFF — does the minimal dark sector survive TODAY's N_eff data, for realistic decay channels? (Janus genesis G6b; locked 2026-11-19 ~23:08Z before any number)
Data [literature, read this tick via search]:
- ACT DR6 extended models (arXiv:2503.14454): N_eff = 2.86 ± 0.13 (P-ACT-LB); 2.89 ± 0.11 with BBN; ACT talk slide: N_eff − 3.044 < 0.17 (95 %).
- arXiv:2603.13226: N_eff = 2.990 ± 0.070 (68 %), LBT Y_p + CMB, "tightest constraint to date".
- Forecast: Simons Observatory σ(N_eff) = 0.055 baseline (arXiv:1808.07445). (CMB-S4 ended July 2025, D1440.)
- SM N_eff = 3.044.
Inputs from D1646 (unchanged): ξ_today = ξ_R × 0.46524 for the minimal sector (Dirac dark fermion + massless dark photon, g_sD 5.5 → 2); ΔN_eff = 0.20629 ξ_R⁴; ξ_R⁴ = f·(106.75/5.5), f = ρ_D/ρ_V at reheating.
Channel scenarios for f (the inflaton is the string coupling; its universal coupling is through the gauge kinetic function f ∝ S):
- S1 democratic per degree of freedom (D1646's A-dem): ξ_R = 1.
- S2 gauge-boson channel dominates (dilaton → gauge pairs via the gauge kinetic function; fermion pairs helicity-suppressed ∝ m_f²): f = N_gauge,D/N_gauge,V = 1/12.
- S3 gauge + Higgs-doublet scalars at equal weight per channel: f = 1/(12 + 4) = 1/16.
- S4 gauge-dominated with a dark QCD (if the "dark baryon" is composite, SU(3)_D + U(1)_D = 9 gauge bosons; g_sD adds 16 gluon d.o.f., g_sD(T_R) = 21.5, g_sD(0) = 2): f = 9/12 (ξ_today recomputed with g_sD 21.5 → 2).
Per scenario report ΔN_eff and pulls: vs ACT P-ACT-LB z = (3.044 + ΔN_eff − 2.86)/0.13 and vs 2603.13226 z = (3.044 + ΔN_eff − 2.990)/0.070; and the maximum f allowed at 2σ by 2603.13226.
Rules (locked): a scenario is CONSISTENT if both pulls ≤ 2σ; TENSION if the larger is 2–3σ; EXCLUDED if > 3σ. Also re-score D1646 case B (S1) — if it is not CONSISTENT, D1646's "VIABLE" (bound 0.3) is corrected by a D1646a note.
Escape routes listed, not scored: a massive dark photon (non-relativistic before recombination ⇒ ΔN_eff → 0); a dark sector with more heavy states (colder).
Script: field_tests/scripts/janus_g/g6b_channels.py → field_tests/results/D1654_G6b_channels.json
