# PREREG D717: Sugra rung: modular-invariant Epstein Kahler potential with constant W0
Locked 2026-11-15 before computing. Script: theory/modular/sugra_rung_d717.py. Output: field_tests/results/sugra_rung_d717.txt.

## Question
Can the SERAPIS plateau come from ordinary N=1 supergravity, with NO negative-tension source (the D703/D712 wall), using a modular-INVARIANT Kähler potential K = −(3α/2) ln E(τ,2), a constant superpotential W0 (allowed because K is invariant) and a τ-independent uplift V_up > 0?

## Inputs (fixed now)
- Model: V = e^K |W0|² (K^{ττ̄}|∂_τK|² − 3) + V_up, along Re τ = ½; V_up tuned so V(ρ) = 0. Derived before running (asymptotics): e^K → E^{−3α/2} ~ y^{−3α}, K^{ττ̄}|K_τ|² → 3α, so V → V_up − (3−3α)|W0|² y^{−3α}: a plateau approached from below only if α < 1, with exponent p = √(6α) in the canonical field. Since SERAPIS-E needs p = 2√2 > √6, this family cannot reproduce SERAPIS-E; it is a distinct rung.
- Grid: α ∈ {1/3, 1/2, 2/3, 0.8, 0.9}; tilt C·Ê multiplying V as in D691, C ∈ {0, 1e-7, 1e-6, 1e-5} (rescaled per α if needed); N* ∈ {48.4, 49.9}.
- Data: none (theory); comparison targets: n_s 0.970 (SPA+DESI 0.9728 ± 0.0029), SERAPIS frozen r band (4.6–5.7)e-4 and caps (n_s ≤ 0.985, r ≤ 8.3e-4).

## Method
Double-precision E(τ,2) Fourier series (D692 code), derivatives by central differences (h = 1e-4), K_ττ̄ = ¼(∂x² + ∂y²)K, canonical φ = ∫√(2K_ττ̄) dy, first-order slow roll on a spline of V(φ). Report: whether ρ is the minimum and V ≥ 0 on the line; untilted (n_s, r, α_s); C giving n_s = 0.970 and the r there.

## Decision rule (written before running)
- VIABLE if: ρ is the minimum with V ≥ 0, n_s = 0.970 reachable, y* ≤ 25, |α_s| ≤ 0.009, r ≤ 1.1e-3 (data-level kill). Report separately whether r falls inside the frozen SERAPIS band or above its 8.3e-4 cap (a distinct prediction if above).
- NOT VIABLE if any of those fails.
- What happens if the run crashes or times out: fixes only through D717_DEVIATIONS.md, written before any rerun.

## Labels
Mark every number in the write-up as computed / estimate / literature / from memory.
