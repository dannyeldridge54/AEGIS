# D2120b DEVIATIONS (written before the rerun)
The first run hit a RecursionError in the integer row-echelon insertion (`hnf_add`), with a buggy Euclid swap, before any output. **Fix:** replace it with the standard extended-gcd row combination. The method and criteria are unchanged.
