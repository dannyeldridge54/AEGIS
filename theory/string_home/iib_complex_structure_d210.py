"""D210: a rung-3 direction that is NOT the overall volume: the overall complex-structure modulus U of a factorisable T^6 orientifold in
type IIB, with Standard-Model matter on D3-branes. AI-assisted symbolic check of the tree-level couplings.
K = -ln(s) - sum ln(t_i) - sum ln(u_i) (+ matter), s = Re S, t_i = Re T_i, u_i = Re U_i (factor-2 conventions dropped).
D3-D3 untwisted matter metric Z_i ~ 1/(t_i u_i): obtained from the D5 metric 1/(s u_1) of hep-th/0404134 by T-duality on T^2_1
(D5 wrapping T^2_1 -> D3; s <-> t_1, U unchanged). Physical Yukawa Y = e^{K/2} W_ijk / sqrt(Z_1 Z_2 Z_3)."""
import sympy as sp
s, t1, t2, t3, u1, u2, u3, W = sp.symbols("s t1 t2 t3 u1 u2 u3 W", positive=True)
eK = 1 / (s * t1 * t2 * t3 * u1 * u2 * u3)
Z = [1 / (t1 * u1), 1 / (t2 * u2), 1 / (t3 * u3)]
Y = sp.simplify(sp.sqrt(eK) * W / sp.sqrt(Z[0] * Z[1] * Z[2]))
print("physical D3 Yukawa:", Y, " -> depends on u_i?", any(Y.has(u) for u in (u1, u2, u3)))
print("D3 gauge coupling f = S: independent of U.  M_s/M_P ~ g_s^{1/4} V^{-1/2}: independent of U (V = t-dependent, g_s = 1/s).")
print("Overall U (u1 = u2 = u3 = u): K_U = -3 ln(U + Ubar) -> rung 3. 10-d string coupling: g_s = 1/s, independent of U.")
# KK masses: a T^2 of area A (string units) and complex structure u: radii sqrt(A u), sqrt(A/u)
for A, u in ((30, 89), (89, 89), (300, 89)):
    print(f"T^2 area {A}, u = {u}: radii {((A*u)**0.5):.1f} and {((A/u)**0.5):.2f} string lengths")
