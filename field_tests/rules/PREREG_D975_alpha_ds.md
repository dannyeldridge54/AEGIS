# PREREG D975: alpha_s with exact de Sitter initial modes (follows D974: not converged with the plain Bunch-Davies start)
Solver: tools/serapis_calc/ms.py spectra(..., ic='ds') (per-mode, 5-point +-0.1 stencil); selftest must pass (incl. L4f).
Points and models exactly as PREREG_D960 (SERAPIS-E C=1.0e-6 N*=48.4; Chronos eps=1.3e-4 N*=46).
Runs: bd in {200, 1000, 5000}.
Converged if |alpha_s(5000)/alpha_s(1000) - 1| <= 2% AND |alpha_s(1000)/alpha_s(200) - 1| <= 2%.
If converged: compare alpha_s(5000) with the published bands (SERAPIS-E -(9.4-10.6)e-4; Chronos -(8.8-10.2)e-4): inside or within 5% of an edge -> "published alpha_s stands"; else a correction note. If not converged: report; method change needs a new lock.
Script theory/flux/alpha_ds_d975.py; output field_tests/results/alpha_ds_d975.txt.
