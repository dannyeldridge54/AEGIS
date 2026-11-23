"""D2224 rerun (DEVIATIONS DEV-1..4): 1/alpha prefilter, clamp rejection, M_s variants, L and U(1) convention variants."""
import itertools, json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..', '..'); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(ROOT, 'tools', 'rings'))
import d2224_strand_engine as E
import rings as G
ReS = math.sqrt(3) / 2; L0 = 18.153466019666112
SIG = math.sqrt(0.0009 ** 2 + 0.00057 ** 2); MMIN = 1.145e16 * (2.4 / 16) ** 0.25; MS = {'0.1MP': 2.4e17, 'MP': 2.4e18}
a0, M0 = E.alpha_s(0, 0); a32, _ = E.alpha_s(0, -0.25); a12, _ = E.alpha_s(0.3, 0)
h32, h12 = (1 / a32 - 1 / a0) / -0.25, (1 / a12 - 1 / a0) / 0.3
cache = {}
def exact(d12, d32):
    k = (round(d12, 9), round(d32, 9))
    if k not in cache:
        try:
            a, M = E.alpha_s(d12, d32); cache[k] = (a, M, M < 1.01e10 or M > 0.99e20)
        except Exception: cache[k] = (float('nan'), float('nan'), True)
    return cache[k]
res = {}
for Lf, u1 in itertools.product((0.9, 1.0, 1.1), (1.0, 0.6)):
    L = L0 * Lf; pts = []
    for c, m1, m3, b32, b12 in itertools.product((1.0, 1 / (2 * math.pi)), range(1, 6), range(1, 6), range(-6, 7), range(-6, 7)):
        d32 = c * (m3 ** 2 - 9) * ReS + b32 * L / (4 * math.pi); d12 = u1 * c * (m1 ** 2 - 9) * ReS + b12 * L / (4 * math.pi)
        if abs(1 / a0 + h32 * d32 + h12 * d12 - 1 / 0.118) > 0.30: continue
        a, M, clamped = exact(d12, d32)
        if clamped or a != a: continue
        pull = (a - 0.118) / SIG; hoy = bool(G.W.weave_nuclear({'dalpha_s': a - 0.118, 'alpha_s': 0.118})['inside'])
        base = abs(pull) <= 2 and M >= MMIN and hoy
        if base: pts.append(dict(c=round(c, 4), m1=m1, m3=m3, db32=b32, db12=b12, alpha_s=round(a, 5), pull=round(pull, 2), M12=float(f'{M:.3g}'),
                                 under_Ms={k: M <= v for k, v in MS.items()}))
    key = f'L{Lf}_U1w{u1}'
    res[key] = dict(stable_base=len(pts), stable_by_Ms={k: sum(p['under_Ms'][k] for p in pts) for k in MS}, frac={k: sum(p['under_Ms'][k] for p in pts) / 8450 for k in MS},
                    natural=[p for p in pts if p['m1'] == 3 and p['m3'] == 3], points=pts)
P = res['L1.0_U1w1.0']; nP = P['stable_by_Ms']['0.1MP']; natP = [p for p in P['natural'] if p['under_Ms']['0.1MP']]
reading = 'landscape allows it, not a prediction' if nP / 8450 > 0.10 else ('forces ring cannot balance on this strand' if nP == 0 else ('CONDITIONAL: natural point stable' if natP else 'stable only off the natural point'))
out = dict(exact_runs=len(cache), primary='L1.0_U1w1.0 with M_s = 0.1 M_P', primary_stable=nP, primary_reading=reading,
           summary={k: dict(stable_base=v['stable_base'], **v['stable_by_Ms'], natural=len(v['natural'])) for k, v in res.items()}, variants=res)
json.dump(out, open(os.path.join(ROOT, 'field_tests', 'results', 'd2224_strand_rerun.json'), 'w'), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != 'variants'}, indent=1))
for p in P['points']: print(p)
