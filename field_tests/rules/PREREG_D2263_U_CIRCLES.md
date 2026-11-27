# PREREG D2263 — Flip symmetry on the true circles u = const (locked 27 Nov 2026)

**Context.** D2262 H1 failed because it used Euclidean circles in tau. Möbius maps fixing tau0 are exact rotations of the disk coordinate
u = (tau - tau0)/(tau - conj tau0); inverse tau = (tau0 - u conj tau0)/(1 - u).
**Hypotheses (exact, from symmetry, before computing).**
- H1 (rho, order-3 flip): on |u| = r, E(theta) contains only angular modes n = 0, 3, 6, ...: |c1|/|c3| and |c2|/|c3| < 1e-10 at r = 0.02 and 0.05.
- H2 (i, order-2 flip): on |u| = r, only even modes: |c1|/|c2| and |c3|/|c2| < 1e-10; the cos 2theta mode carries the saddle.
- H3 (CP mirror): with theta measured from the mirror direction, the sin parts vanish (|Im c_n|/|c_n| < 1e-10 for the surviving modes after
  rotating to the mirror axis) — reported, pass if the surviving-mode phases are multiples of pi/n to 1e-8.
- H4 (measured, not predicted): r-scaling of c3 at rho and c2 at i (fit exponent from r = 0.02, 0.05).
**Method.** mpmath Fourier E (as D2261, dps 30, nmax 30), 72 points per circle, s = 2 and 3/2. Run once.
Output field_tests/results/d2263_u_circles.json.
