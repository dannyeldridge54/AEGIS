# Q12 DEVIATIONS (written before the fixed run)
D1 (code, no result seen): first run crashed after VALIDATION PASS with KeyError 'T' (targets/tolerances live after the split point of the reused Q8 file). Fix: copy T and TOL verbatim from q8_ckm_split.py. No observable was computed before the crash; rule unchanged.
