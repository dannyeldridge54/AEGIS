# PREREG B7 — τ=i hidden sectors through bbn_net (Djl B) — locked 2026-11-17
For each target final ΔN_eff ∈ {0.054, 0.161, 0.301} (D1088 cases U(1), SU(2), SU(2)+gaugino):
- Solve dNeff_init by secant, starting from the D1109 ratio (final/init ≈ 0.261), until |ΔN_final − target| ≤ 0.003. At most 5 evaluations per target; ΔN_final = Neff_final − Neff_final(0).
- Report Y_p(mass), 10⁵ D/H and 10¹⁰ Li-7, plus pulls vs Aver Y_p 0.2453 ± 0.0034 and Cooke D/H 2.527 ± 0.030 (observational errors only, as in D1088).
- Compare with D1088's PRIMAT-table Y_p and D/H at the same ΔN, converting D1088's nucleon fraction to mass with bbn.Yp_mass.
Scored: bbn_net vs table agree within 0.001 (Y_p) and 2% (D/H) for every case. B7 VALIDATED iff all agree. Physics verdicts are reported.
Script theory/wiring/b7_taui_bbnnet.py (written after this lock).
