# PREREG S4c3 — convergence of the 6D KK first mass m1² (S4c2, D1033) by smaller cutoff + Aitken extrapolation
Locked 2026-11-17 before any S4c3 number. Same Prüfer shooting code as s4c2_pruefer.py (unchanged functions), cutoffs ε = 1e-5, 1e-6,
1e-7, 1e-8 at both ends of the interval. Model: m1²(ε) = m* + c ε^q.
From each consecutive triple (ε_i, ε_i/10, ε_i/100): q = log10(Δ1/Δ2), Aitken m* = m3 − Δ2²/(Δ1 − Δ2) with Δ1 = m1−m2, Δ2 = m2−m3.
T1: q from the triples (1e-5..1e-7) and (1e-6..1e-8) agree within 0.1. T2: their Aitken m* agree within 1e-3 relative. T3: m* > 0.
All pass → m1² = Aitken m* of the last triple, labelled [computed, extrapolated]; same for m2², m3² (reported, not tested).
Any fail → S4c3 NOT VALID, recorded as is. Results: field_tests/results/s4c3_richardson.txt.
