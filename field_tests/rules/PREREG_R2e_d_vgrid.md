# PREREG R2e-d — velocity-grid convergence of the relic (D1238 candidate ii) — locked 2026-11-18, before code or run
Code unchanged: r2c_b_alls.run(Ms, XS, [n]) with n = 40, 80, 160. The closed-side grid is 5n, as built into run(). The R_eff tables feed r2e_b_gstar.omega (g_*(T), MS-bar α̂₂, x to 1e8, R held beyond 3e4). M = 2800 and 3000 GeV. The 25 R2e-b x points.
Scored: Q = max over the two masses of |Ω(n = 160)/Ω(n = 40) − 1|.
- Q > 1% → grid resolution MATTERS for the L1 gap.
- Otherwise it is RULED OUT.
Also reported: Ω at n = 80, and n = 40 vs R2e-b (0.1048 / 0.1195; this should reproduce, since it is the same grid).
