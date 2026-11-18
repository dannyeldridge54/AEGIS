# PREREG TK1 — audited SERAPIS-E through every applicable toolkit + data pulls
Locked before running. Model: tools/serapis_calc/pipeline.build('serapis_e', C) (n = 1, E(τ,2) plateau + BHK tilt).
Points: (i) the 3×1 grid C = 1.0, 1.15, 1.3e-6 at N* = 50.7 (centre of the audited window, D1235);
(ii) END-TO-END derived points: pipeline.predict(C, TR) self-consistent N* (tools/serapis_calc/nstar.py, exact end) at the audited ρ reheating T_R = 6.6e8 and 2.0e10 GeV, C = 1.0, 1.15, 1.3e-6.
Toolkits: (a) Janus core spectra3 (third-order flow); (b) exact Mukhanov–Sasaki (tools/serapis_calc/ms.spectra, BD initial conditions); (c) Janus core second-order spectra; (d) Janus relation α_s(n_s, r; p = 2√2, κ = 1);
(e) data pulls tools/serapis_calc/data.sigma (CMB-SPA 0.9684 ± 0.0030, CMB-SPA+DESI 0.9728 ± 0.0027) and r < 0.036; (f) CAMB 2.0.5: primordial-tensor BB at ℓ = 80 for each r (A_s = 2.1e-9, n_t = −r/8), information only.
ASPIC: not applicable (SERAPIS-E is not in the ASPIC library) — recorded, not run.
Agreement bars (PASS per point): exact MS vs (a): |Δn_s| ≤ 3e-4, |Δr/r| ≤ 2 %, |Δα_s| ≤ 5e-5; (d) vs MS α_s ≤ 6 % (D693).
Results: field_tests/results/tk1_serapis_e_toolkits.txt.
