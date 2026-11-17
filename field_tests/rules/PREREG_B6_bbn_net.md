# PREREG B6 — Hyperion bbn_net module (LINX primary) (Djl D) — locked 2026-11-17
Module (written after this lock): tools/janus_astro/bbn_net.py, function abundances(ombh2, dNeff_init=0, tau_n_fac=1).
- Calls LINX: BackgroundModel(ΔN_init), AbundanceModel(NuclearRates('key_PRIMAT_2023')), eta_fac = ombh2/linx.const.Omegabh2.
- Returns a dict with explicit names: Yp_mass, Yp_BBN (= 4Y), DH, He3H, Li7H, Neff_final.
- Mass-fraction formula as in D1106 (PRIMAT atomic masses).
Tests:
- T1 regression: at (0.02242, 0, 1) it reproduces D1106/B5 (Yp_mass 0.24592, 10⁵DH 2.4360, 10¹⁰Li 5.699) to the printed digits.
- T2 ΔN response: [X(ΔN_init = 0.3) − X(0)] from bbn_net vs the PRIMAT-table response for the same ΔN, for X = Yp_mass and DH. Agreement within 15%.
  - Our table's ΔN is relative to N_eff = 3.044, while LINX's ΔN is an initial value, so the 15% allows for that mapping. Reported: LINX Neff_final.
- T3 ω_b response: X(0.0230) − X(0.02242) from bbn_net vs the table, within 10%, for Yp_mass and DH.
B6 VALIDATED iff T1, T2 and T3 pass. Fixes only via DEVIATIONS.
Script theory/janus_astro/b6_check.py.
