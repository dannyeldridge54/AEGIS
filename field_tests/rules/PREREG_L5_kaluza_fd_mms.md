# PREREG L5-K — first use of the L-5 verification kit: KALUZA fd_schrodinger order of accuracy on an exact case
Locked 2026-11-17 before running. Case: −ψ'' + Uψ = m²ψ in z with Dirichlet ends, U = 0, written in a curved coordinate y ∈ (1e-9, √π]
with J(y) = dz/dy = 2y (z = y², z ∈ [0, π]) — tests the y→z map as well as the FD operator. Exact m_n² = n² (n = 1, 2).
Grids N = 500, 1000, 2000 (h = π/(N+1)). Claims: K1 observed order (tools/lockbench/verify.py observed_order) within 2 ± 0.1 for both modes
on both grid pairs; K2 GCI_fine (Celik 2008, Fs 1.25) at N = 2000 ≤ 1e-5 and |m²_ext − n²|/n² ≤ 1e-7.
Both → KALUZA FD OPERATOR VERIFIED (2nd order); else NOT. Results: field_tests/results/l5_kaluza_fd_mms.txt (+ stamp).
