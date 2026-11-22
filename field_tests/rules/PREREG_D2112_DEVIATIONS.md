# D2112 DEVIATIONS (written before the rerun)

The first run crashed with a Python TypeError (subscripting an `enumerate` object) in the K8 helper. It crashed before anything was printed or saved, so no results were seen.

**Fix:** a syntax-level rewrite of that one line into an explicit two-element list. The method, inputs and pass criteria are unchanged.
