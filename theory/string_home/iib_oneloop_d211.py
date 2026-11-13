"""D211: one-loop leak in the D210 lead (rough estimate). AI-assisted.
Berg-Haack-Kors (hep-th/0508171 eq. 12): K1 = (1/256 pi^6) sum_I [ E2^D3(A_I, U_I)/((S-Sbar)(rho_I-rhobar_I)) + E2^D7(0,U_I)/(...) ].
The D3 open-string scalars A_I sit inside E2(A,U) = sum' U2^2/|n + m U|^4 e^{2 pi i (Wilson-line phase)}: expanding in A gives a one-loop
correction to the D3 matter metric. Leading (m = 0, KK modes of the long direction) term: d^2E2/dA dAbar ~ 4 pi^2 zeta(2) (A normalised by U2).
Tree metric from K0: Z_A ~ 1/(8 pi rho2 U2). Ratio dZ/Z ~ 8 pi U2 * 4 pi^2 zeta(2) * c_D3 / (256 pi^6 S2), c_D3 = O(100) from the brane
multiplicities in their example (128N - 8N...), taken as 1 here (lower bound) and 128 (their coefficient)."""
import math
z2 = math.pi ** 2 / 6
def ratio(U2, S2, c=1.0):
    return 8 * math.pi * U2 * 4 * math.pi ** 2 * z2 * c / (256 * math.pi ** 6 * S2)
gYM2 = 4 * math.pi / 25          # SM-like unified coupling: on D3-branes 1/g^2 = Re S, so S2 ~ 1/gYM2
for S2 in (1 / gYM2, 10.0, 100.0):
    for c in (1, 128):
        r = ratio(89, S2, c); beta = 0.5 * r / math.sqrt(1.5)        # m ~ Z^-1/2, d/dphi of a term growing as U2
        print(f"Re S = {S2:6.2f} (g_s = {1/S2:.3f}), c = {c:3}: one-loop dZ/Z at U2 = 89 ~ {r:.2e}, beta ~ {beta:.1e} (Cassini 3.4e-3), grows ~ U2")
