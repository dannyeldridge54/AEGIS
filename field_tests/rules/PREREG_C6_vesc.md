# PREREG C6 — local escape speed: MWPotential2014 vs Gaia DR2 (Djl C) — locked 2026-11-17
Data (quoted, Deason et al. 2019, MNRAS 485, 3514, abstract): v_esc(r0 = 8.3 kpc) = 528 (+24/−25) km/s; M200,tot = 1.00 (+0.31/−0.24) e12 M_⊙.
Model: galpy MWPotential2014 (ro = 8, vo = 220), halo amplitude s ∈ {0.8, 1.0, 1.1, 1.2}. Evaluated at R = 8.3 kpc, z = 0. Two definitions:
- (i) v_esc = √(2[Φ(r_max) − Φ(r0)]) with r_max = 2 r200. This is my reading of the usual definition, labelled unverified. r200 is taken from the s-scaled NFW halo M200 (H0 67.66, 200 ρ_crit; C4 method).
- (ii) to infinity, √(−2Φ(r0)). The NFW halo potential converges.
Scored per s and definition: CONSISTENT if within 2σ (asymmetric errors).
Reported: which s range (i) allows, compared with the C4 window 0.8–1.1.
Script theory/wiring/c6_vesc.py (written after this lock).
