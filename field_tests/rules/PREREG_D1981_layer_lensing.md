# PREREG D1981: layer lensing / polarization map, 9 layers (Danny 18:24, 18:38). Locked 22 Nov 2026 00:4xZ, before computing.
## Object
Model: tools/loom/resonance.py margins(k) at the derived knobs D (u, MN, m32, TR in ln units; split raw). Knob space dimension n = 5.
**Lens of layer k:** the right-singular directions of J_k = d(margins of layer k)/d(knobs), keeping sigma_i > 1e-3 * sigma_max(k).
The number of lenses of layer k = numerical rank r_k (<= min(#margins_k, 5)). A layer with no margins (L3, L9: TRUST) is a **window**: it passes every direction.
**Transfer k -> next:** principal angles between the lens subspaces of layer k and the next non-window layer.
- PASS: smallest angle < 15 deg.
- BENT: smallest angle 15–75 deg.
- BLOCKED: smallest angle > 75 deg.
**Chain:** P = P_9 ... P_1 (projectors; window = identity). Transmitted dimension = rank(P); transmitted fraction = ||P||_F^2 / n.
**9 x 9 coupling matrix:** C_jk = max cos^2(principal angle) between the lenses of layers j and k (all pairs, not only neighbours). The hub is the layer with the largest row sum.
## Three readings (triangulation)
- R1: central finite differences, h = 1e-4.
- R2: random-probe regression, 400 perturbations uniform in ±3 % (seed 1981), least squares.
- R3: the declared map KNOBS_OF (hand labels, the prior).
R1 and R2 are numerical and independent in method; R3 is independent of the numerics. Per layer, the three must agree on r_k and on the class of each transfer. A disagreement makes that item INDETERMINATE, and is reported with which reading differs (an R3 disagreement means the hand label is wrong).
## Verdict rule (6 non-window transfers: 1-2, 2-4, 4-5, 5-6, 6-7, 7-8)
- **Lensing SUPPORTED in this model:** at least 2 of 6 BENT and chain transmitted dimension >= 1.
- **DECOUPLED (lensing picture not supported here):** at least 5 of 6 BLOCKED.
- Otherwise MIXED.
## Stated before computing (honest priors)
- **Structural:** the model has 5 knobs, so a 9-axis lens geometry cannot exist in it; at most 5 lenses per layer. A real 9-dimensional lens structure needs at least 4 more derived knobs (not fits). For example, the geometric moduli the model does not yet carry as knobs: Im S, the T_i of the three tori, U3.
- **Expected by construction:** obs() gives most observables their own knob, so DECOUPLED is the likely outcome. If so, it is a property of the hand-built engine (datasheet D3 lesson), not physics. That is the same reason the still-point axes came out pure.
- The shape-based lens counts (torus, pyramid, cube, ...) are **not defined anywhere in our docs**. They are not tested here. If Danny gives them, they become a prediction to compare with r_k.
- No tolerance changes after this lock. Any fix goes into DEVIATIONS before a rerun.
