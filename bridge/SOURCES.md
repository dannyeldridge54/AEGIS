# SOURCES — pinned AEGIS commit e1dfd3769d86852ea9938ce573265dc734eb435c (branch unify-bg), all paths relative to the repo root

Master record of every result: theory/pending_docs/D72_D75_weak_spots.md  (search for "## D<number>")
The full Weave equation:       theory/pending_docs/WEAVE_FULL_EQUATION.md   (tags: [der] [lit] [P] [EMP] [OPEN])
Postulates register:           theory/pending_docs/WEAVE_POSTULATES.md
Referee ledger:                REFEREE_LEDGER.md
Locks:                         field_tests/rules/PREREG_*.md (+ .sha256, *_DEVIATIONS.md)

Scalar field (the thread)
- Inflation potential V(tau_1), E(tau,3/2), plateau, endpoint at rho: WEAVE_FULL_EQUATION.md sections 1-2; D1527-D1616
- Basin flow (69% to i, 31% to rho): D1610; shapes.py / basins.py (tools/ - grep "def basins")
Quantum (fluctuations of that same scalar)
- Exact Mukhanov-Sasaki n_s, r: WEAVE_FULL_EQUATION.md section 1 (D = 10: n_s 0.97065, r 5.41e-4)
Negative space
- Lock: field_tests/rules/PREREG_NEGSPACE_DERIVE.md ; code: field_tests/scripts/negspace/negspace.py ; result: D1716, D1717
- Coupled thread: field_tests/rules/PREREG_COUPLED_THREAD.md ; D1710
- Full-Planck CLASS test: field_tests/rules/PREREG_PLANCK_CLASS.md ; field_tests/scripts/pc_planck/aegis_class_d1713.patch ; verdict D1725
- Knob-board scan of the coupling b: PREREG_D2134 (+ addendum, DEVIATION 2) ; verdict D2134, referee D2134a
Reverse thread (late-time copy of the plateau): D1626 ; doi:10.5281/zenodo.24380387
