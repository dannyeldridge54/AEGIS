# PREREG SPEED-Zurvan (rotation rung 3), locked 2026-11-23 ~09:28 CT before code
Reference: tools/gifts/zurvan/zurvan.py (numerical central differences of the CW potential). Fast path zurvan_fast.py:
the exact eigenvalue derivative of each 2x2 sfermion matrix (and the fermion masses), no finite differences.
Z1: every Sigma term on P1-P3 matches the reference to 1e-6 relative (the reference's own step error is ~1e-7 to 1e-9),
    and Delta_EW (both views) to 1e-6. Timing: median of 3 over 200 evaluations.
Field map: supersymmetry and electroweak naturalness -> releases/field_maps/susy_naturalness.md.
