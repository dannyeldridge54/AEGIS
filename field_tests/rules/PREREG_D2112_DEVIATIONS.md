# D2112 DEVIATIONS (written before the rerun)

The first run crashed with a Python TypeError (subscripting an `enumerate` object) in the K8 helper. It crashed before anything was printed or saved, so no results were seen.

**Fix:** a syntax-level rewrite of that one line into an explicit two-element list. The method, inputs and pass criteria are unchanged.

## Addendum: lock slip on K4 (written before computing it)
D2110 set a standing rule: every new quantity is computed under both (j, k) orderings, P1 and P2. The K4 code used only P1 (the default).

The P1 result is final and recorded as it came out:
- sectors 1 and 3 match the paper exactly;
- sector 2 does not match;
- the rank is 5 = 5.

Now adding the required P2 evaluation of K4 (sector 2 is exactly where P1 and P2 differ). It is reported next to P1. Nothing else is rerun.
