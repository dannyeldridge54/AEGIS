# PREREG R2b4 — threshold continuity with the photon Coulomb term off — locked 2026-11-17, before any run
Purpose: separate a solver normalisation bug from Coulomb/Rydberg physics (D1170).
- Closed side: sommerfeld_nlo.wino_s_nlo(M, v, nlo=False), with the module constant ALPHA set to 0 at runtime. V reads it at call time, so this removes −α/r from V_{+−}; nothing else changes.
- Open side: two_channel_open with Vfun lacking −ALPHA/r, and tails = (0, 0).
- M = 2000 GeV. x = E/2δm ∈ {0.99, 1.01}. Also reported, not scored: x = 0.95, 0.999, 1.001, 1.05.
- Quantity: S = sΓs†, Γ = [[2, √2], [√2, 3]]. Also report |s0|² and |s1|².
Score: PASS iff |S(1.01)/S(0.99) − 1| ≤ 0.20.
- PASS → the solvers agree, and the D1170 factor ~3 belongs to the Coulomb/Rydberg sector.
- FAIL → solver normalisation bug.
