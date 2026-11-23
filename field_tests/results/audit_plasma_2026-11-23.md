# Back-end audit, plasma/plant side (R98, sonnet, read-only; scratch /tmp/audit_p) — 23 Nov 2026, requested by Danny 13:48-13:49
Verdict: physics core sound (Bosch-Hale, Q, E_n 14.0284, Gamow 5.906/6.088 keV, Albajar, IPB98, Martin/IPB99, tbr_required, 56.083 kg,
545 Gbar all verified); weaknesses in test/lock hygiene and two CubeMind cards. Findings and actions (DEVIATIONS written before fixes):
1 locked results overwritten by imports (test_prom6 writes JSON at import; prom6/7/8 locked JSONs rewritten 13:10; prom5 run-1 FAIL overwritten)
  -> JSON writes moved under __main__; locked-run JSONs restored from their first commits (git); prom5 rerun content kept as prom5_rerun.json.
2 old locked tests no longer run (test_s2_s3 T_avg->Te_avg; test_s4_s6 dpa_conversion; speed V3 baseline predates PLANT_DEMO change)
  -> s2_s3/s4_s6 repaired to run (keys only); speed V3 marked STALE-BASELINE (not re-scored).
3 PROM-9 rerun used the pre-DEV PROM-7 ARC (T_ped 5.46): ARC 471.1 MW / H98 1.856 quoted in D2203; post-DEV values 480.2 / 1.862 -> D2203a.
4 PROM-7 rerun SPARC inherited ITER f_He 0.032 -> f_DT 0.786, Z_eff 1.564 (not 0.85 / 1.50 as written in D2201); other inherited ITER keys:
  f_reflect 0.6, beta_T 2, T_sep 0.1; T_ped = 0.39 T_pub makes D1/D2 partly circular -> D2201a (recomputed values labelled post-audit, not a new test).
5 fusion_cards ignition card missing KEV_J (would teach CubeMind a wrong number); cooling card wrong for Ne (Z 9.41, bare 0.53 at 0.5 keV)
  -> both cards corrected; redeploy to the PC.
6 adas L_imp negative for He (PRB - C_B<z^2> sqrt T, -1.5e-37..-5.9e-37 W m^3); clipping the SUM hid it -> clip per species; n_e fixed 1e20 noted;
  plasma_fast non-pedestal fallback ignores line_model/synch (noted); adas/popcon/extra_imp/synch branches lack a reference check (noted).
7 PREREG_PROM3 E2 text calls 1686 MW 'P_n' (it is fusion power; code right, M 1.2387) -> recorded here (lock text error).
8 tests that cannot fail: sim A5/B2, fraction sums, G8/G9, I5/E1 circular, L7 engine outputs, prom9 can_fail not in pass_, prom6 D3 passes on no-root
  -> listed; future locks must state the can-fail explicitly in pass_.
9 element_cards: IAS isomers 8/9 named 'm8/m9'; nuclide_binding('H-1') TypeError; trailing 'm' ignored; 'Hf-178m2' rejected; estimated masses not
  flagged; mixed year lengths -> fixed (H-1 returns BE 0 / None safely, isomer names m1..m2 only for iso 1-2, 'IAS' for 8/9, estimated flag carried).
10 small: goal dials at the top of the P_aux set (73); DEV-14 He 220 vs code 140; D2196 W 1.9e-31 vs 3.3e-31; NIF 5.0 MJ and N210808 not source-verified.
