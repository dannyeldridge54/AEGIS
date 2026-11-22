# PREREG D2001: tile counting for a (3,10)-graph on 40 vertices (Danny 20:41: "count the tiles, the math should add up"). Locked before computing.
**Identity** (Goedgebeur & Radziszowski, arXiv 1210.5826). For a (3,10;40,e)-graph with n_d vertices of degree d:

  γ = 40·e − Σ_d n_d·(d² + e(3,9, 39 − d)) ≥ 0,  with 2e = Σ d·n_d and Σ n_d = 40.

**Degrees:** d ∈ {4,…,9}. The neighbourhood is independent, so d ≤ 9. The dual neighbourhood is a (3,9)-graph on 39 − d ≤ 35 vertices, so d ≥ 4.

**Inputs:** exact published e(3,9,m) for m = 30–35 = 86, 95, 104, 118, 129, 140 (Table 4).

**Output:** every degree composition (n_4,…,n_9) with γ ≥ 0, and the range of e.
- If none survives, R(3,10) = 40 is proved by counting. That is unexpected: the published work treats 40 as still open.
- If some survive, they are the search target's allowed degree patterns. The search will be constrained to them.
