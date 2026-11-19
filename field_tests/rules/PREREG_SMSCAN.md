# PREREG SMSCAN — "integrate out the torus area" family (Danny 03:33 "start this testing too"): which (s, m) land in band?

Locked 2026-11-19 before computing.
Mechanism (D-note to follow): V(A,U) = a/A^p − c·E(U,s)/A^q (shape-blind term + one-loop Casimir on T²); minimising over the heavy
area gives V(U) ∝ −E(U,s)^{−m}, m = p/(q − p); with a constant uplift tuned at the minimum: V = V₀[1 − (E(ρ,s)/E(U,s))^m].
Vacuum at ρ for every s by Montgomery's theorem (hexagonal lattice minimises E(·,s) at fixed area, s > 0).
Note: this family has NO free a (the plateau is fixed in units of E(ρ,s)) — a physical frame, unlike D698's λ.
Implementation: pipeline serapis_e path (Re U = ½, n = 1), E_paper → (E(U,s)/E(ρ,s))^m so that e = (E/E_ρ)^m − 1 and the pipeline's
e/(e+1) = 1 − (E_ρ/E)^m exactly; λ = 1; C = 0 (pure plateau; the tilt is a separate question). Start point by the DILATON32
DEVIATIONS D1 bisection rule (N_end ∈ [100, 200]) adopted up front. T_R = 8.94e8. Engine pipeline.predict (D1417 α_s estimator).
Grid (s, m): (3, 1/3), (3, 2/3), (3, 1), (2, 1/2), (2, 1), (2, 3/2), (1.5, 1), (1.5, 4/3).
Report n_s, r, α_s, N* per point, and the approach exponent s·m. Rules: "in band" (n_s 0.969–0.975, r 4.55–5.7e-4), "near"
(within 0.003 in n_s and 30% in r). Expectation stated now: r is set mainly by s·m (s·m = 1 → r ≈ 1.6e-3 like D1398; s·m = 2 → r near
SERAPIS); n_s at C = 0 may sit below 0.969 (SERAPIS needs its tilt) — so "near" points count as candidates for a tilt study.
No reruns to chase results; fixes only via PREREG_SMSCAN_DEVIATIONS.md written first.
