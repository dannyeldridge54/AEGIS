# PREREG D2120b: exact integral even lattice for the Z_n test (referee R2-6). Locked before computing.

**Method:**
1. Represent a cycle as an integer vector u = (X, Y, x_{kα}, y_{kα}) in Z³², with ω(u,v) = ¼(X_u Y_v − Y_u X_v − Σ(x_u y_v − y_u x_v)), i.e. z2z6p.chi.
2. F is the Z-span of all fractional cycles with |n|,|m| ≤ 2 × 256 labels. This is a proxy for H₃(Z); check saturation with |n|,|m| ≤ 3 on a random subsample of 20,000.
3. R is the orientifold map from z2z6p.image (P2).
4. **E = F ∩ ker(R − 1)**, computed exactly with integer linear algebra (HNF / unimodular column reduction).
5. Z_n survives iff Σ_x k_x N_x ω(Π_x, e) ≡ 0 (mod n) for every basis vector e of E.

This covers every integral even element, including half-sums.

**Normalisation cross-check:** run the same code on the six-stack model (p.tex ~3627–3633) and compare with 1303.6845 Table 5 (Z4^a, Z2^b, Z2^c, Z4^d, Z2^e, Z2^f, as seen in our fetch). Our expectation is that the trivial single-stack Z_{N_x} always survive. Report the full survivor list for both models.

**Verdict:** K9 is final per the surviving Z_n's Yukawa selection. If only centre-like or trivial Z_n survive, the 1⊕2 obstruction is withdrawn.
