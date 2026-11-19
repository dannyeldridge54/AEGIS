# PREREG P3S_TABLE — prediction table for P3-S across its tilt band, per tilt class (for the paper)

Locked 2026-11-19 (09:45 CT) before computing. DpL cycle 10.
Model: P3-S species plateau (PREREG_SPECIES32 code path, D1 stencil), engine F (third-order flow + self-consistent N*, T_R 8.94e8;
D1521/D1532: matches exact MS to ~5e-6 in n_s), tilt classes and C values fixed now from the filed band intervals:
  T2 (Λ^{−4}, ~y):      C ∈ {1.26, 1.37, 1.48}e-5         (D1529)
  T3 (Λ^{−6}, R⁴):      C ∈ {6.8, 8.0, 9.37}e-7           (D1529/D1532)
  T5 (E(τ,5/2), D⁴R⁴):  C ∈ {6.2, 8.1, 10.0}e-9           (D1529)
  TF (flux, KL):        C ∈ {2.26, 2.46, 2.66}e-5         (D1533/D1538)
Report per point: n_s, r, α_s, β_s, N*, y*. Data distances (σ units, n_s only): CMB-SPA 0.9684 ± 0.0030 and CMB-SPA+DESI 0.9728 ± 0.0027
(the frozen F3 references); r vs BK18 bound r < 0.036 (all trivially pass).
Discriminators to report: Δr between classes at equal n_s (interpolated at n_s = 0.9706, the D1532 centre) and Δα_s.
This is a bookkeeping run of filed models: no verdict rule beyond reporting; any value that disagrees with the filed band rows by
> 1e-4 in n_s is flagged, not rerun. Fixes only via PREREG_P3S_TABLE_DEVIATIONS.md written first.
