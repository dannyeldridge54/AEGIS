# PREREG D391 — N* for the Twist without the hidden σ sector (locked 13:10 CT 14 Nov 2026, before running)

Purpose: Twist-2 design (papers/twist_v6/TWIST2_DESIGN.md) drops the hidden σ sector (matter genesis by leptogenesis instead).
D387 found σ's matter-like phase cuts the kination shift to +1.0. This computes the shift with σ removed, at the v5 heat shares.
Script: theory/inflation/nstar_nosigma_d391.py = kination_Nstar.py (Development 84) with the heat-share list changed to (0.65%, 0.8%)
and nothing else. Statistic: N* and n_s printed for each heat share (converged column must agree to ±0.01, else "NOT CONVERGED").
Reading (reported, no pass/fail on the theory): N* ≥ 58 → "reaches the refined-Starobinsky ACT 2σ region (arXiv:2504.20757)", else
"below"; distance of n_s from CMB-SPA 0.9684 ± 0.0030 and CMB-SPA+DESI 0.9728 ± 0.0027 (arXiv:2609.19296) in σ.
Cross-sector: none computed here (leptogenesis yield not computed). No reruns; fixes via a DEVIATIONS file written first.
