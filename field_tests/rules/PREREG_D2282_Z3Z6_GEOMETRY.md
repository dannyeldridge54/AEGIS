# PREREG D2282 — Ping-pong item "Z3 x Z6 fold", step A: geometry and N = 2 sectors (locked 27 Nov 2026)
**Input (literature convention, Font-Ibanez-Quevedo / 1412.7327 class).** T6 = T2 x T2 x T2, twists v1 = (1/3, 0, -1/3), v2 = (0, 1/6, -1/6).
**Computed (script tools/field_engine/z3z6_geometry.py, run once):**
1. All twisted sectors g = k v1 + l v2 (k = 0..2, l = 0..5, not both 0); for each, which tori are left fixed (component integer).
2. N = 2 sectors = exactly one torus fixed; list them and the fixed torus.
3. For each torus, the rotation orders acting on it; complex structure U frozen at rho if an order-3 or order-6 rotation acts, at i if order 4,
   free if only order 2 or none.
4. SUSY check: each sector's components sum to an integer (N = 1 in 4D).
**Expected before running (pass criteria).** All three U frozen at rho (orders 3 and 6 on every torus); at least one N = 2 sector per torus;
SUSY sums integer. FAIL if any U is free or no N = 2 sector exists.
**Consequence fixed now.** If PASS: in this fold the i vacuum cannot be a complex-structure value; it must be a Kahler modulus T (or a Wilson-line/
twisted modulus) held dynamically (Zhinu, D2269).
