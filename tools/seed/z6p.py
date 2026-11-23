"""D2146 B2 builder: IIA T6/Z6' (= the Weave's Z6-II twist (1,2,-3)/6) fractional D6-branes, from Gmeiner-Honecker 0708.2285.
Cycle = (P,Q,U,V, d1..d4, e1..e4); fractional cycle = 1/2 of that vector. Lattice ABa (b=0) implemented for the control."""
import numpy as np
BULK = np.array([[0, 0, 4, 2], [0, 0, 2, 4], [-4, -2, 0, 0], [-2, -4, 0, 0]])   # rho_i o rho_j
def form():
    M = np.zeros((12, 12), dtype=int); M[:4, :4] = BULK
    for i in range(4): M[4 + i, 8 + i] = -2; M[8 + i, 4 + i] = 2     # delta_i o dtilde_i = -2
    return M
F = form()
def inter(x, y): return int(round(0.25*(np.array(x) @ F @ np.array(y))))   # (1/2 x) o (1/2 y)
def image_ABa(c):
    P, Q, U, V = c[:4]; d = c[4:8]; e = c[8:12]
    return [Q, P, -V, -U] + [-v for v in e] + [-v for v in d]
O6_ABa = [2, 2, 6, -6] + [0]*8          # Pi_O6 = rho1 + rho2 + 3(rho3 - rho4), stored as a doubled vector (x = 2 Pi)
def tadpole(stacks, image, O6):
    tot = np.zeros(12)
    for N, c in stacks: tot += N*(np.array(c) + np.array(image(c)))
    return tot - 4*np.array(O6)           # both sides are doubled vectors
def chiral(stacks, image, O6):
    out = {}
    names = list(stacks)
    for a in names:
        Na, ca = stacks[a]; ia = image(ca)
        out[(a, 'Anti')] = (inter(ca, ia) + inter(ca, O6))//2 if (inter(ca, ia) + inter(ca, O6)) % 2 == 0 else (inter(ca, ia) + inter(ca, O6))/2
        out[(a, 'Sym')] = (inter(ca, ia) - inter(ca, O6))/2
        for b in names:
            if names.index(b) <= names.index(a): continue
            out[(a, b)] = inter(ca, stacks[b][1]); out[(a, b + "'")] = inter(ca, image(stacks[b][1]))
    return out
