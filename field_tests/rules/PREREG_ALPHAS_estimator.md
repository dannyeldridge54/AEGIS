# PREREG — α_s estimator precision (D1410 open item). Locked 2026-11-18 21:05 CT before computing (Danny "3 min loop on this").

Diagnosis to test: ms.spectra fits a degree-4 polynomial through 5 points at Δln k = ±0.1 (exact interpolation), so α_s = 2c₂ has
noise ≈ σ_lnP/h² with h = 0.05; σ ~ 1e-6 gives ~4e-4 — the size seen in D1410.
New estimator (option, default unchanged until the test passes): 11 points Δln k ∈ [−0.5, 0.5] step 0.1, least-squares cubic;
n_s = 1 + c₁, α_s = 2c₂ (cubic absorbs β_s; bias from the quartic term ~ (0.5)²·δ/… expected ≲ 1e-5 for SERAPIS).
Test (serapis_point model, C = 1.25e-6, T_R = 8.94e8, pipeline.predict path, two setups whose true α_s is identical):
  A: bd = 200 (default), B: bd = 300 (deeper Bunch–Davies start). Old estimator and new estimator on both.
Pass rules: (P1) new |α_s(A) − α_s(B)| ≤ 3e-5; (P2) new n_s agrees with old n_s to ≤ 2e-5 in both setups;
(P3) old |α_s(A) − α_s(B)| is recorded (expected ≥ 1e-4, confirming the diagnosis). If P1 and P2 pass, the new estimator becomes
the default (a code change recorded in the D-note); if not, the D-note records the failure and nothing changes.
No reruns to chase results; fixes only via PREREG_ALPHAS_estimator_DEVIATIONS.md written first.
