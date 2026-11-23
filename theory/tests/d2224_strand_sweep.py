"""D2224: D7 strand sweep (PREREG_D2224_D7_STRAND). Every strand point enumerated; linear pre-filter; survivors run exactly."""
import itertools, json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..', '..'); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(ROOT, 'tools', 'rings'))
import mpmath
import d2224_strand_engine as E
import rings as G
ReS = math.sqrt(3) / 2; ReT = 28 - 9 * ReS
def L(a):
    tau = mpmath.mpc(a, ReT); q = mpmath.exp(2j * mpmath.pi * tau); eta = mpmath.exp(2j * mpmath.pi * tau / 24) * mpmath.qp(q)
    return float(-mpmath.log(ReT * abs(eta) ** 4))
Ls = {a: L(a) for a in (0.0, 0.25, 0.5, 0.75)}; L0 = Ls[0.0]
SIG = math.sqrt(0.0009 ** 2 + 0.00057 ** 2); MMIN = 1.145e16 * (2.4 / 16) ** 0.25
a0, M0 = E.alpha_s(0, 0); a32, _ = E.alpha_s(0, -0.25); a12, _ = E.alpha_s(0.3, 0)
g32, g12 = (a32 - a0) / -0.25, (a12 - a0) / 0.3
pts = []
for c, m1, m3, b32, b12 in itertools.product((1.0, 1 / (2 * math.pi)), range(1, 6), range(1, 6), range(-6, 7), range(-6, 7)):
    d32 = c * (m3 ** 2 - 9) * ReS + b32 * L0 / (4 * math.pi); d12 = c * (m1 ** 2 - 9) * ReS + b12 * L0 / (4 * math.pi)
    lin = a0 + g32 * d32 + g12 * d12
    pts.append(dict(c=round(c, 4), m1=m1, m3=m3, db32=b32, db12=b12, d32=d32, d12=d12, lin_pull=(lin - 0.118) / SIG))
cand = [p for p in pts if abs(p['lin_pull']) <= 4]
cache = {}
for p in cand:
    k = (round(p['d12'], 9), round(p['d32'], 9))
    if k not in cache:
        try: cache[k] = E.alpha_s(p['d12'], p['d32'])
        except Exception as e: cache[k] = (float('nan'), float('nan'))
    a, M = cache[k]; p.update(alpha_s=a, M12=M, pull=(a - 0.118) / SIG)
    p['hoyle_inside'] = bool(G.W.weave_nuclear({'dalpha_s': a - 0.118, 'alpha_s': 0.118})['inside']) if a == a else False
    p['stable'] = bool(a == a and abs(p['pull']) <= 2 and M >= MMIN and p['hoyle_inside'])
st = [p for p in cand if p['stable']]
nat = sorted([p for p in st if p['m1'] == 3 and p['m3'] == 3], key=lambda p: (abs(p['db32']) + abs(p['db12']), abs(p['pull'])))
frac = len(st) / len(pts)
reading = 'landscape allows it, not a prediction' if frac > 0.10 else ('forces ring cannot balance on this strand' if not st else ('CONDITIONAL: natural point stable' if nat else 'stable only off the natural point'))
out = dict(guard=a0, M12_0=M0, slopes=dict(d32=g32, d12=g12), L_by_ImT=Ls, n_points=len(pts), n_prefiltered=len(cand), n_exact_runs=len(cache), n_stable=len(st),
           frac_stable=frac, natural=nat[:3], reading=reading, stable=st)
json.dump(out, open(os.path.join(ROOT, 'field_tests', 'results', 'd2224_strand.json'), 'w'), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != 'stable'}, indent=1))
for p in st: print({k: (round(v, 5) if isinstance(v, float) else v) for k, v in p.items() if k not in ('lin_pull',)})
