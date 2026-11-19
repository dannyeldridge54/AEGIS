<!-- AEGIS-FP P3S-NOTES · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License) -->
# P3-S cheat sheet (state at end of 19 Nov 2026) — for tools/serapis_calc/p3s.py

## The equation (SERAPIS_FINAL_EQUATION.md v3; paper Zenodo 10.5281/zenodo.24377930, v1.1 24378141/2)
    V(τ) = V∞ · ((2/3) y ∂_y ln E(τ,3/2))² · [1 + C (E(τ,3/2) − E(ρ,3/2))],   Re τ = ½,  ρ = e^{iπ/3}
    = V∞ (1/3 + (4/3) ∇² ln Λ_QG) [1 + C(…)],   Λ_QG = M_P E^{−1/6},  λ_sp = 1/√8      (D1546, exact)
    large y:  V ≈ V∞ [1 − 7.30 y^{−2}],  7.30 = 16ζ(2)/(3ζ(3))                            (D1523)
    canonical field: y = e^{bφ}, b = √(D−2)/2  (D = 10: φ = ln y/√2;  D = 6: φ = ln y)
    tilt C = w χ /(4(2π)³ 𝒱), w = 1 (F-term) or 2/3 (D7 D-term); blue needs χ > 0          (D1566, D1565a; estimate)

## Locked exact (Mukhanov–Sasaki) anchors
| run | C | n_s | r | α_s | N_* |
|---|---|---|---|---|---|
| SPECIES32 X, D = 10 (D1532) | 8e-7 | 0.97065 | 5.41e-4 | −9.68e-4 | 50.37 |
| P3D6 X, D = 6 (D1593) | 2.64e-6 | 0.97056 | 1.069e-3 | −9.59e-4 | 50.57 |
| untilted D = 10 (engine F, D1523) | 0 | 0.9601 | 4.0e-4 | | |
Band: n_s 0.969–0.975, r 4.55–5.7e-4. Tilt band (D = 10): C ≈ 6.8–9.4e-7.
Untilted analytic: n_s = 1 − 2/N − 3/((D−2)N²), r = 8/((D−2)N²). r ladder at n_s ≈ 0.9706: r_D ≈ 5.41e-4 · 8/(D−2)
(10D 5.4e-4 · 9D 6.2e-4 · 8D 7.2e-4 · 7D 8.7e-4 · 6D 1.07e-3 · 5D 1.4e-3 · 4D 2.2e-3).
CMB-S4/LiteBIRD σ(r) ~ 5e-4 [from memory, not looked up this session] ⇒ 10D vs 6D ≈ 1σ; 10D vs 4D is the clean split.

## p3s.py speed and accuracy (D1635)
`point(C, D)` ≈ 0.2 s (exact MS ≈ 30 min). Against the two anchors: |Δn_s| ≤ 5.1e-6, |Δr/r| ≤ 0.013 %, |Δα_s| ≤ 5.3e-7, |ΔN_*| ≤ 1.3e-5.
`tilt_for_ns(target, D)` recovers C = 8.005e-7 (D = 10) and 2.642e-6 (D = 6) in ~5 s. Also returns n_t (second order, D1555).
Use it to screen and to forecast before a locked exact run; quote exact MS numbers in papers.

## What else today established (one line each; all read-only checks unless marked)
- Endpoints: the inflaton exits at ρ for every kick (D1606; classification rule changed pre-outcome in DEVIATIONS D2); slow fields drain to i with f_i = 0.69 (D1610); invariant terms cannot move the i minimum (D1614), κ y^{1/2}|η|² gives a smooth split τ ≈ 1.05i–1.17i (D1618).
- Control: P3-S-F at 𝒱 ≈ 3.5e7 has ξ̂/𝒱 ~ 1e-3 (our M5 flag is DILMIX-only, D1536); BBHL tilt route has ξ̂/𝒱 0.7–1.4e-3 (D1566, checked in D1567).
- Open: no supergravity derivation of the plateau prefactor (D1541–D1550, D1583); Andriot-type rate bound ×42 (D1527); H/m_3/2 needs KL racetrack (D1537–D1538); BBN toy failed its lock (Y_p 0.202, D1632; upgraded network D1633 pending).
- Reverse thread (plateau as thawing DE vs DESI DR2): fits all SN sets only in a ~1–2 % tuned window, after a post-data recalibration (D1626–D1628); paper Zenodo 24380387 states both.
- Our own: forecast record 22/22 locked P3 points |Δn_s| ≤ 5.3e-6 (d1485 engine); physical-frame DILMIX in band (D1512); tensor tilt n_t ≈ −6.2e-5, n_t + r/8 ≈ −1.5e-6 (D1555).
- Paper flags still open in species v1.1: abstract "reads off D" overstated; 6D r 1.07e-3 (tilted) vs 8.01e-4 (untilted) unlabelled.
