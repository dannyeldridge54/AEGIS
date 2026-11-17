# PREREG B4b — three-code BBN agreement at Planck ω_b (Djl B; follows DEVIATIONS_B4 D1) — locked 2026-11-17
Fix for D1: copy PRyMordial (commit 725d8a8d) to a second scratch directory and edit ONLY the line `Omegabh2 = 0.02230` → `0.02242` in the copy's PRyM/PRyM_init.py. Then run exactly as in B4 (small network, Python path).
Codes at Ωbh2 = 0.02242, ΔN = 0:
- PRIMAT 2021 table via bbn.Yp_mass / bbn.DH
- LINX key_PRIMAT_2023 (D1106 values, not rerun: Y_p 0.24592, 10⁵D/H 2.4360, 10¹⁰Li 5.699)
- PRyMordial copy: Y_p(CMB, a mass fraction)
Scored (B4b VALIDATED iff all three):
- max−min of Y_p(mass) over the three codes ≤ 0.001
- D/H spread ≤ 3% of the mean
- ⁷Li/H (PRyMordial vs LINX) within 5%
Reported: τn per code (PRIMAT 879.4, PRyMordial 878.4, LINX default as printed if available), and the bbn_net.py plan.
Script theory/wiring/b4b_three.py (written after this lock).
