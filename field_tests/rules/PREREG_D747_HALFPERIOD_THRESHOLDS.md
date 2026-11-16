# PREREG D747: can D3 stacks at the half-periods give the plateau term through gauge thresholds?
Locked 2026-11-16 before computing. Script: theory/modular/halfperiod_thresholds_d747.py. Output: field_tests/results/halfperiod_thresholds_d747.txt.
Input (literature, BHK hep-th/0404087 eq. 40/44): stack-dependent threshold −ln|ϑ₁(A,U)/η(U)|² (+ a non-holomorphic πU₂a₄² piece). At the half-periods A ∈ {½, U/2, (1+U)/2}, |ϑ₁| becomes |ϑ₂|, e^{πU₂/4}|ϑ₄| and e^{πU₂/4}|ϑ₃|.
Checks (numerical, U = ½ + iy, y ∈ {2, 5, 10, 14, 20}):
1. Identity ϑ₂ϑ₃ϑ₄ = 2η³: equal stacks give a U-independent combined threshold (up to the non-holomorphic piece).
2. Large-y behaviour of a single-stack threshold ln|ϑ_k/η|², k = 2, 3, 4: linear in y (so the potential ∝ e^{−cy}) vs the plateau's needed power law 1/E(U,2) ∝ y^{−2}.
Decision: if (1) holds to 1e-10 and (2) shows linear-in-y thresholds, route (i) of D746 (a gauge-threshold condensate) is EXCLUDED for this brane setup; the plateau stays open. Otherwise report what is found.
