"""D2228 (PREREG_D2228_SURVIVOR_SPLIT): tree alpha_3/alpha_2 = V_b/V_a on the stored Z6-II survivors (D2170 formula)."""
import json, math, os, collections
from fractions import Fraction as Fr
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
rho = Fr(1, 2)
def V(w): P, Q, U, Vv = w[:4]; return (P + Q) - Fr(2, 3) * rho * (Vv - U)
pub = dict(a=[0, 0, 1, -1], b=[3, 0, 3, 0]); Rpub = float(V(pub['b']) / V(pub['a']))
S = json.load(open(os.path.join(ROOT, 'tools', 'seed', 'z6p_scan3a.json')))['survivors']
Rs, bad = [], 0
for s in S:
    va, vb = V(s['a']), V(s['b'])
    if va <= 0 or vb <= 0: bad += 1; continue
    Rs.append(float(vb / va))
c = collections.Counter(round(r, 4) for r in Rs)
inD = sum(abs(math.log(r / 1.02)) < math.log(1.15) for r in Rs); inT = sum(abs(math.log(r / 1.02)) < math.log(3) for r in Rs)
out = dict(control_published=Rpub, n=len(S), n_nonpositive_volume=bad, distinct_R=sorted(c.items()), n_tree_unified=inD, n_needs_thresholds=inT,
           reading='no stored survivor can host the tau = i threshold route' if inT == 0 else 'candidates exist for the N=2 Delta b derivation')
json.dump(out, open(os.path.join(ROOT, 'field_tests', 'results', 'd2228_survivor_split.json'), 'w'), indent=1); print(json.dumps(out, indent=1))
