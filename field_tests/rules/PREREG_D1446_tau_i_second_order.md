# PREREG D1446 — τ = i offset model at second-order slow roll vs the five NA12 exact points

Locked 2026-11-19 (UTC) before computing (JANUS tick 42, node band_i).
Model (D635 potential with D640's exact field-map offset, not expanded in c): V/V0 = 1 − I⁻² + (ε/2)I, φ = ln(I + c)/√2,
c = ln1728/(2π) = 1.18646 (D640/D1412; asymptotic τ = i model, Epstein-type exponentially small terms dropped).
Method: D1442's second-order machinery (1609.04739 Eqs. 9–12; α_S to O(ε³) = dn_S/d ln k with d ln k = (1 − ε1)dN), mpmath dps 30,
solve (ε, I*) so second-order (n_s, r) = each NA12 point; predict α_s.
References: field_tests/results/na12_band_i_audited.txt (NA12 exact MS, ε 1.30–1.50e-4). Their file date 18 Nov 18:36 CT PREDATES
D1417's estimator fix (21:37 CT) ⇒ reference precision ~0.1–0.2 % (D1444 caveat), stated up front.
Implementation check: recovered ε within 10 % of each point's NA12 ε (D640 method B recovered ε), else "no result".
Rule: PASS if max |α_pred/α_exact − 1| < 0.3 % (beats D640's −0.29 … −0.34 %, D1412); FAIL otherwise.
Also report first-order values at the same model (expect ≈ D640's "method B" +1.1 … +1.6 % pattern, not required).
No reruns to chase results; fixes only via PREREG_D1446_DEVIATIONS.md first.
