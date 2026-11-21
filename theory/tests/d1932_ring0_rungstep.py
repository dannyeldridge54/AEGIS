"""D1932: pulse ring 0 (rule 6h, 7 nulls): the one-spurion window around the median rung step 0.027."""
import json, math, cmath, statistics, sys
sys.path.insert(0, 'tools/loom'); from triangulate import bracket
src = open('theory/tests/d1925_onespurion.py').read().split('u = U(0.0457')[0]; exec(src)
has = lambda a: len(scan(a)) > 0
assert has(0.027) and not has(0.0234) and not has(0.0311), 'VOID: bracket ends do not straddle the edges'
logL, logH = [], []
lo, lw, ln = bracket(has, 0.0234, 0.027, 1e-6, log=logL)
hi, hw, hn = bracket(has, 0.027, 0.0311, 1e-6, log=logH)
ph = cmath.phase(U(0.0457 * cmath.exp(1j * math.radians(49))))
inside = []
for a in (lo + (hi - lo) * k / 4 for k in (1, 2, 3)):
    fits = scan(a); reads = []
    for seed in (32, 33, 34):                      # three independent draws per point (stability, not a thread)
        reads.append(max((natural(a * cmath.exp(1j * ph), *f, N=2000, seed=seed) for f in fits), key=lambda t: t[0]))
    inside.append(dict(abs_u=a, assignments=[list(map(list, f)) for f in fits], f7=[r[0] for r in reads], fJ=[r[1] for r in reads],
                       f7_med=statistics.median(r[0] for r in reads), fJ_med=statistics.median(r[1] for r in reads)))
# three vectors on the rung step itself: one-spurion window centre, D1832 lepton slip, neutrino theta-step
vec = dict(one_spurion_centre=math.sqrt(lo * hi), lepton_slip=0.0253, neutrino_theta=math.exp(-9 * math.pi / 8))
c = statistics.median(vec.values()); s = max(vec.values()) - min(vec.values())
out = dict(window=[lo, hi], edge_res=[lw, hw], rounds=[ln, hn], width_factor=hi / lo, inside=inside,
           natural_all=all(p['f7_med'] >= 0.05 and p['fJ_med'] >= 0.2 for p in inside),
           contains=dict(median_0p027=lo <= 0.027 <= hi, u_d_0p02587=lo <= 0.02587 <= hi, lepton_0p0253=lo <= 0.0253 <= hi),
           three_vectors=vec, vector_centre=c, vector_spread=s, centre_vs_median=c / 0.027 - 1, log_lo=logL, log_hi=logH)
print(json.dumps({k: v for k, v in out.items() if not k.startswith('log')}, indent=1))
json.dump(out, open('field_tests/results/d1932_ring0_rungstep.json', 'w'), indent=1)
