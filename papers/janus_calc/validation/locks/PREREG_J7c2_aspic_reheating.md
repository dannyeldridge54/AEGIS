<!-- AEGIS-FP KOZHBCLS7CESFZHT · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License) -->
# PREREG J7c2 — reheating-route head-to-head, corrected matching (replaces VOID J7c, see its DEVIATIONS D1)

Locked 2026-11-17 before any J7c2 number.
Matching (Martin & Ringeval 1004.5525 Eq. 15, exact): ΔN* = ln R_rad − N_0 + ln H* − ¼ ln(3 H_end²), physical units
(M_P = 1). With V = M⁴ V̂: H = M² Ĥ, so ΔN* = ln R_rad − N_0 + ln M + ln Ĥ* − ½ ln Ĥ_end − ¼ ln 3 [derived, arithmetic],
and M⁴ = P*/P̂(pivot), P̂ the scalar amplitude computed with V̂. P* = ASPIC powerAmpScalar = 2.1127e-9; N_0 = ASPIC Nzero.
- Exact reference: P̂ from exact Mukhanov–Sasaki (ms.spectra_fast 'PR' at the pivot, J7b settings); solve the
  matching by fixed-point/root-finding in the pivot e-fold (the amplitude depends on the pivot); then exact n_s, r, α_s.
- Janus: same equation, P̂ = Ĥ*²/(8π²ε1*)·[1 − 2(C+1)ε1 − Cε2] with C = γ_E + ln2 − 2 (ASPIC src/common/huflow.f90
  hubbleflow_corrections, case 2; = the standard second-order amplitude), ε's from Janus's exact-background flow; spectra3.
- ASPIC: as J7c (foo_x_rrad, raw output already committed: field_tests/results/janus_j7c_aspic_raw.txt).
Points, claims C1–C3, C5 and verdict rule: as PREREG_J7c. Added C6 (reported): ASPIC ΔN* error is expected to be
O(0.01–0.1) e-folds (its leading-order matching); a median > 0.5 would indicate a remaining convention mismatch and
is to be reported as such, not as ASPIC error.
