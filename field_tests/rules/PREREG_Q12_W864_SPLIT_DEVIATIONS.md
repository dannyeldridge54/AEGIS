# Q12 DEVIATIONS (written before the fixed run)
D1 (code, no result seen): first run crashed after VALIDATION PASS with KeyError 'T' (targets/tolerances live after the split point of the reused Q8 file). Fix: copy T and TOL verbatim from q8_ckm_split.py. No observable was computed before the crash; rule unchanged.

## D-tol (20 Nov 2026, from the independent referee; recorded, no rerun)
The lock text writes the CKM tolerances as "|V_us| ±10%, |V_cb| ±20%, |V_ub| ±30%, J ±50%"; the code applied them as two-sided factors (×/÷1.1, 1.2, 1.3, 1.5). The two readings differ only for values below target: under the lock's ±30% a |V_ub| of 0.70–0.74× PASSES, under the code's ÷1.3 (0.769) it FAILS. Both readings are reported; the overall verdict (FAIL) is the same under either, because m_s/m_b and |V_cb| (Q12) or m_s/m_b, |V_us|, |V_ub|, J (Q8) fail under both.
