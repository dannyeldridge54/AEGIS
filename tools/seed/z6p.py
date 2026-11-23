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
# ---- generator (PREREG_D2146 addendum 2)
from fractions import Fraction as Fr
H = Fr(1, 2)
T2_TABLE = {  # (s1,s2),(s5,s6) -> {T3 parity: [(i1,j1),(i1,j2),(i2,j1),(i2,j2)]}  (Table 2, (n1,m1) odd,odd)
 ((0,0),(0,0)):  {'oo': [(1,1),(1,3),(6,1),(6,3)], 'oe': [(1,1),(1,2),(6,1),(6,2)], 'eo': [(1,1),(1,4),(6,1),(6,4)]},
 ((0,0),(0,H)):  {'oo': [(1,2),(1,4),(6,2),(6,4)], 'oe': [(1,3),(1,4),(6,3),(6,4)], 'eo': [(1,1),(1,4),(6,1),(6,4)]},
 ((H,0),(0,0)):  {'oo': [(4,1),(4,3),(5,1),(5,3)], 'oe': [(4,1),(4,2),(5,1),(5,2)], 'eo': [(4,1),(4,4),(5,1),(5,4)]},
 ((H,0),(0,H)):  {'oo': [(4,2),(4,4),(5,2),(5,4)], 'oe': [(4,3),(4,4),(5,3),(5,4)], 'eo': [(4,1),(4,4),(5,1),(5,4)]},
 ((0,0),(H,0)):  {'oo': [(1,2),(1,4),(6,2),(6,4)], 'oe': [(1,1),(1,2),(6,1),(6,2)], 'eo': [(1,2),(1,3),(6,2),(6,3)]},
 ((0,0),(H,H)):  {'oo': [(1,1),(1,3),(6,1),(6,3)], 'oe': [(1,3),(1,4),(6,3),(6,4)], 'eo': [(1,2),(1,3),(6,2),(6,3)]},
 ((H,0),(H,0)):  {'oo': [(4,2),(4,4),(5,2),(5,4)], 'oe': [(4,1),(4,2),(5,1),(5,2)], 'eo': [(4,2),(4,3),(5,2),(5,3)]},
 ((H,0),(H,H)):  {'oo': [(4,1),(4,3),(5,1),(5,3)], 'oe': [(4,3),(4,4),(5,3),(5,4)], 'eo': [(4,2),(4,3),(5,2),(5,3)]}}
def orbit(i, j, w3, w4):
    """Z6' orbit of d_ij x (w3 pi3 + w4 pi4) in the (delta, dtilde) basis (Table 1). Point 1 drops out."""
    d = [0]*4; e = [0]*4; k = j - 1
    if i == 4: d[k] += w3; e[k] += w4
    elif i == 5: e[k] += -w3; d[k] += w4; e[k] += -w4
    elif i == 6: e[k] += w3; d[k] += -w3; d[k] += -w4
    return d, e
def bulk(w):
    n1, m1, n2, m2, n3, m3 = w
    a = n1*n2 - m1*m2; c = n1*m2 + m1*n2 + m1*m2
    return [a*n3, c*n3, a*m3, c*m3]
def exceptional(w, sig, tau):
    n1, m1, n2, m2, n3, m3 = w
    assert n1 % 2 and m1 % 2, 'use the (odd,odd) representative on T1'
    par = ('o' if n3 % 2 else 'e') + ('o' if m3 % 2 else 'e')
    s12 = (Fr(sig[0]), Fr(sig[1])); s56 = (Fr(sig[2]), Fr(sig[3]))
    if s12 == (H, H): s12 = (0, 0)            # caption: (1/2,1/2) acts like (0,0) for (odd,odd)
    if s12 == (0, H): s12 = (H, 0)            # underlined: either ordering
    pts = T2_TABLE[(s12, s56)][par]
    t0, t1, t3 = tau; signs = [1, (-1)**t3, (-1)**t1, (-1)**(t1 + t3)]   # order: i1j1, i1j2, i2j1, i2j2
    d = [0]*4; e = [0]*4
    for (i, j), s in zip(pts, signs):
        dd, ee = orbit(i, j, n2, m2)
        for k in range(4): d[k] += s*dd[k]; e[k] += s*ee[k]
    g = (-1)**t0
    return [g*x for x in d], [g*x for x in e]
def cycle(w, sig, tau):
    d, e = exceptional(w, sig, tau); return bulk(w) + d + e
def susy_ABa(c, rho):
    P, Q, U, V = c[:4]
    return (Fr(P - Q)/(2*Fr(rho)) - (U + V) == 0) and ((P + Q) - Fr(2, 3)*Fr(rho)*(V - U) > 0)
