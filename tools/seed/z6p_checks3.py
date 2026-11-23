"""D2146 addendum 3 checks: end-to-end control, bulk-cycle saturation, representative invariance."""
import json, os, sys, math, itertools, random
sys.path.insert(0, os.path.dirname(__file__)); import z6p as Z
from fractions import Fraction as Fr
H = Fr(1, 2); out = {}
# (1) end-to-end: regenerated cycles -> control 1
W = {'a': (1, -1, 1, 0, 0, 1), 'b': (1, 1, 2, -1, 1, 1), 'c': (1, -1, -1, 2, 1, 0), 'd': (1, 1, 1, -2, 0, 1), 'e': (1, 1, 1, -2, 0, 1)}
SIG = {'a': (H, 0, H, 0), 'b': (H, 0, 0, 0), 'c': (H, 0, 0, H), 'd': (0, 0, H, 0), 'e': (H, 0, 0, 0)}
TAU = {'a': (0, 1, 1), 'b': (1, 1, 0), 'c': (1, 1, 1), 'd': (0, 1, 1), 'e': (0, 1, 0)}
NN = {'a': 3, 'b': 2, 'c': 1, 'd': 1, 'e': 1}
S = {k: (NN[k], Z.cycle(W[k], SIG[k], TAU[k])) for k in W}
tp = Z.tadpole(S.values(), Z.image_ABa, Z.O6_ABa); ch = Z.chiral(S, Z.image_ABa, Z.O6_ABa)
pub = {('a','c'):-3,("a","b'"):3,("a","c'"):-3,('b','c'):-9,('b','d'):6,("b","c'"):-9,("b","d'"):3,('c','d'):-3,("c","d'"):3}
bad = {str(k): v for k, v in ch.items() if v != pub.get(k, 0)}
out['end_to_end'] = dict(tadpoles_zero=bool(abs(tp).max() < 1e-9), mismatches=bad, PASS=bool(abs(tp).max() < 1e-9 and not bad))
# (2) saturation of SUSY non-overshooting bulk cycles
def susy_bulk(B, rho=H):
    P, Q, U, V = B; return Fr(P - Q)/(2*rho) == U + V and (P + Q) - Fr(2, 3)*rho*(V - U) > 0
sat = {}
for L in (3, 4, 5, 6):
    rng = range(-L, L + 1); s = set()
    for n1, m1, n2, m2, n3, m3 in itertools.product(rng, repeat=6):
        if math.gcd(n1, m1) != 1 or math.gcd(n2, m2) != 1 or math.gcd(n3, m3) != 1: continue
        B = Z.bulk((n1, m1, n2, m2, n3, m3))
        if susy_bulk(B) and 0 <= B[0] + B[1] <= 8 and abs(B[2] - B[3]) <= 24: s.add(tuple(B))
    sat[L] = sorted(s)
out['saturation'] = {L: len(v) for L, v in sat.items()}; out['saturated'] = sat[5] == sat[6]
out['bulk_cycles'] = [list(x) for x in sat[6]]
# (3) representative invariance on (odd,odd) orbits
def frac_set(w):
    s = set()
    for sig in itertools.product((0, H), repeat=4):
        for tau in itertools.product((0, 1), repeat=3):
            try: s.add(tuple(Z.cycle(w, sig, tau)))
            except Exception: pass
    return s
random.seed(1); cand = []
for n1, m1, n2, m2, n3, m3 in itertools.product(range(-3, 4), repeat=6):
    if n1 % 2 and m1 % 2 and math.gcd(n1, m1) == 1 and math.gcd(n2, m2) == 1 and math.gcd(n3, m3) == 1 and (n3 or m3) and (n2 or m2):
        if susy_bulk(Z.bulk((n1, m1, n2, m2, n3, m3))): cand.append((n1, m1, n2, m2, n3, m3))
random.shuffle(cand); tested = []; ok = True
for w in cand[:20]:
    n1, m1, n2, m2, n3, m3 = w
    reps = [w, (-n1, -m1, n2, m2, -n3, -m3), (n1, m1, -n2, -m2, -n3, -m3), (-n1, -m1, -n2, -m2, n3, m3)]
    sets = [frac_set(r) for r in reps]; same = all(x == sets[0] for x in sets); ok &= same
    tested.append(dict(w=w, same=same, n_frac=len(sets[0])))
out['representatives'] = dict(n_tested=len(tested), all_same=ok, rows=tested)
print(json.dumps({k: v for k, v in out.items() if k != 'bulk_cycles'}, indent=1, default=str)[:3000])
json.dump(out, open(os.path.join(os.path.dirname(__file__), 'z6p_checks3.json'), 'w'), indent=1, default=str)
