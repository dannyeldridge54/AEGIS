# PREREG D1448 — τ = i at second-order SR on NA12's exact plateau 1 − 1/(I² + 1)

Locked 2026-11-19 (UTC) before computing (JANUS tick 44, node band_i).
Model: V = 1 − 1/(I² + 1) + (ε/2)I, φ = ln(I + c)/√2, c = ln1728/2π — NA12's integrated potential (running_d632.py) with
I = y − c and I₁ = I/2, verified to 4e-15 at y 20–30 (D1447). Only change vs D1446: the "+1" in the plateau.
Method, references, implementation check (ε within 10 %) and reporting: identical to D1446 (script field_tests/scripts/d1448/tau_i_exact.py
= d1446 script with V changed). NA12 references use the pre-D1417 5-pt estimator (~0.1–0.2 % precision, stated).
Rule: PASS if max |α_pred/α_exact − 1| < 0.3 % over the five NA12 points; FAIL otherwise.
No reruns to chase results; fixes only via PREREG_D1448_DEVIATIONS.md first.
