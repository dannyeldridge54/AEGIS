# PREREG R2b5 — Coulomb-sector diagnosis of the D1170 factor ~3 — locked 2026-11-17, before any run
Setup as in r2b4_nocoulomb.py. M = 2000 GeV. S = sΓs†, Γ = [[2, √2], [√2, 3]].
Check 1 (scored):
- Open side at x = 1.01 with full α, tails = (0, ALPHA). R = R0, 2R0 and 4R0, where R0 = 300/min(k) (the default).
- PASS iff max|S(R)/S(R0) − 1| ≤ 0.05.
- FAIL → the open solver's Coulomb asymptotics are not converged: a code fault, and the prime D1170 suspect.
Check 2 (reported, not scored):
- α scaled by λ ∈ {0, 0.1, 0.3, 1}.
- Closed side at x = 0.99: patch N.ALPHA = λ·ALPHA.
- Open side at x = 1.01: −λα/r in Vfun, tails = (0, λα).
- Report S, |s0|² and |s1|² on each side.
No tuning. Any fix goes in DEVIATIONS before a rerun.
