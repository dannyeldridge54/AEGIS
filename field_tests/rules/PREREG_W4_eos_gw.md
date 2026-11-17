# PREREG W4 — EoS → Λ → GW tidal phase chain (A3 → A2d wiring; Djl A fallback) — locked 2026-11-17
Why the fallback: 2009.00640 quotes no second resonance or Sommerfeld value usable for a blind A1e (fetched list: only plot masses, saturation statements and accuracies). A1e stays open.
Chain: ns.at_mass(PPEOS(SLy or AP4), 1.4) → Λ_1.4 → gw.taylorf2_tidal_dphase(f, 1.4, 1.4, Λ, Λ, 6), on f = 20 Hz to 0.8 f_ISCO (2.8 M_⊙), detrended (constant + linear fit removed).
- T1 (wiring lossless, scored): the chained phase equals the direct call with the same Λ, bit-identical.
- T2 (scored): Λ_1.4 reproduces D1059/A3c (SLy 296, AP4 248) to ±1.
Reported: the SLy−AP4 tidal-phase difference (rad), with D1098's estimate of ~0.13 rad as a check. Also, as an estimate, the 6.5/7PN LAL-ALL increment for scale.
Script theory/wiring/w4_eos_gw.py (written after this lock).
