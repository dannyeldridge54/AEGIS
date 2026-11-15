# D492 DEVIATIONS
D1. First run violated closure (Σ Ω fell from 1.000 to 0.039 by N = 5): the separately evolved ln Ω_r drifted, a bug in my bookkeeping. Fix: drop the Ω_r equation and enforce
closure, Ω_r = (1 − x₁² − y²)/(1 + a/a_eq), Ω_m = (1 − x₁² − y²) − Ω_r. Everything else unchanged. Buggy output kept as results/twistm_history_d492_run1_bug.txt.
