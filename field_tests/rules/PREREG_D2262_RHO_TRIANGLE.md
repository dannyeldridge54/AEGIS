# PREREG D2262 — The triangular shape of the bowl at rho (locked 27 Nov 2026)

**Context.** D2261: rho is a round minimum of E(tau,s) at second order (forced by the order-3 flip). The order-3 flip allows the first
non-round term only at third order, ~ r^3 cos(3(theta - theta0)) (as j(tau) ~ (tau - rho)^3; Mohseni-Vafa arXiv:2510.19927).
**Hypotheses (before computing).**
- H1: on a small circle tau = rho + r e^{i theta}, the r^3 angular part is cos(3 theta) type; the cos(theta) and cos(2 theta) parts are smaller,
  vanishing faster than r^3 as r drops (checked at r = 0.02 and 0.01).
- H2: the three shallowest directions point along the three mirror geodesics from rho to the neighbouring saddles (images of i):
  theta = 30 deg (arc |tau| = 1 to i), 150 deg (arc |tau+1| = 1 to -1+i), 270 deg (line Re tau = -1/2 down to (-1+i)/2).
  The three steepest directions are 90, 210, 330 deg (toward the cusps 0? no: up toward i*inf at 90 deg, and the two flips of it).
- Pass: fitted minima within 1 deg of 30/150/270 for s = 2 and s = 3/2; H1 amplitude ratios |c1|/|c3|, |c2|/|c3| fall when r halves.
**Method.** E via the mpmath Fourier form (as D2261, dps 30, nmax 30). 72 points on each circle; discrete Fourier coefficients of
E(r,theta) - mean. Run once. Output field_tests/results/d2262_rho_triangle.json.
