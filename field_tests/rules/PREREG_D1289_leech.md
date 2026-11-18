# PREREG D1289 — d=24: the Leech lattice (locked before computing)
Build Λ24 from the extended Golay code (quadratic-residue construction, length 23 + parity), generators in √8-scaled integer
coordinates {2c for Golay basis words, 4(e_i ± e_j), (−3, 1²³)}, reduce with LLL (fpylll), Gram/8. Enumerate all vectors with |v|² ≤ 4.
## Predictions (before computing)
- P0 (construction check): Golay code has 759 weight-8 words, min weight 8; Gram det = 1, all norms even.
- P1: no vectors of norm 2; exactly 196560 of norm 4 (kissing number 24).
- P2: self-dual (det 1) ⇒ θ_Λ(α) = α^{−12} θ_Λ(1/α): no flip at any scale.
- P3: at every α ≥ 1, Leech has lower Gaussian energy than E8³ (the other d=24 even unimodular lattice with roots); computed with the
  enumerated shells ≤ 4 plus a stated bound for the rest.
## Pass/fail: as stated.
