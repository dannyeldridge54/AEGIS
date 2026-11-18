# PREREG R2e-b — wino relic with the Saikawa–Shirai g_*(T), h_*(T) — locked 2026-11-18, before code or run
Data: field_tests/data/saikawa_shirai_2020_gstar.dat (provenance file alongside), interpolated linearly in ln T.
Boltzmann (Gondolo–Gelmini form; changes vs R2e-a only):
- dY/dx = −√(π/45) M_Pl g_*^{1/2}(T) (m/x²) ⟨σv⟩(x) (Y² − Y_eq²), with T = m/x.
- g_*^{1/2} = (h_*/√g_*)(1 + (T/3h_*) dh_*/dT), where h_* = g_*s and g_* = g_*ρ.
  - dh/dT is by central differences in ln T on the interpolant.
- Y_eq = 45/(4π⁴) (g_χ/h_*(T)) x^{3/2} e^{−x} √(π/2), with g_χ = g_eff = 6 as before.
- Everything else is as in R2e-a:
  - MS-bar α̂₂(2M) in Γ;
  - R_eff(x) from r2c_b_alls (n = 40), held beyond 3e4;
  - x from 3 to 1e8;
  - the same S0 and ρ_c h².
Mass grid as R2e-a: {2.2, 2.4, 2.6, 2.8, 3.0, 3.2} TeV, log–log interpolation. The Born root is found by brentq.
Scored:
- B1: Born M_th within 3% of Beneke's 2.207 TeV.
- L1: LO-Sommerfeld M_th within 3% of Beneke's 2.886 TeV. Same Ω h², same potential constants, now the same EOS class.
Reported:
- the shift of each mass vs R2e-a (constant g_* = 106.75): R2e-a gave Born 2.325 and LO 3.135;
- the Born result starting at x = 1 vs x = 3 (Beneke starts at x = 1).
No tuning. Any fix goes in DEVIATIONS before a rerun.
