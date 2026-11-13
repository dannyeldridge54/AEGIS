"""D184: the direction in moduli space that keeps the matter sector's UV scale fixed, and its rung. AI-assisted.
Moduli s_i = Re(field) with K = -sum k_i ln s_i. Move along s_i = e^{a_i sigma}: kinetic metric = sum k_i a_i^2 / 4 per unit sigma^2, so the
path is an effective disk with 3 alpha_eff = (sum k_i a_i^2) / (normalisation of the lead modulus) — we report k_eff such that the
path behaves like K = -k_eff ln t for the rung-3 modulus t (a_T = 1).
Scale constraints: Type IIB (D3/D7 matter): M_s/M_P ~ g_s^{1/4} V^{-1/2}, with Re S = 1/g_s and Re T ~ V^{2/3} -> exponents (-1/4, -3/4).
Heterotic M-theory (Horava-Witten): M_GUT/M_P ~ (Re S Re T)^{-1/2}. Weakly coupled heterotic: M_s/M_P ~ (Re S)^{-1/2}."""
import math
cases = {"type IIB (S: k=1, T: k=3)": ((1, 3), (-0.25, -0.75)),
         "heterotic M-theory (S: k=1, T: k=3)": ((1, 3), (-0.5, -0.5)),
         "weakly coupled heterotic (S: k=1, T: k=3)": ((1, 3), (-0.5, 0.0))}
for name, (k, p) in cases.items():
    # scale fixed: p_S a_S + p_T a_T = 0 with a_T = 1
    aT = 1.0; aS = -p[1] * aT / p[0] if p[0] else 0.0
    keff = k[0] * aS ** 2 + k[1] * aT ** 2
    lam = math.sqrt(2 / keff)        # tail slope for V ~ 1/t along the path (as rung keff/3)
    print(f"{name}: scale-preserving path a_S = {aS:+.2f} per unit ln T -> behaves like rung 3alpha = {keff:.0f} (tail slope {lam:.3f})")
print("gauge coupling 1/g^2 = Re S (+ b Re T) also varies along any path with a_S != 0: holding BOTH the UV scale and 1/g^2 fixed")
print("needs two conditions on the a_i -> at least three moduli moving together.")
