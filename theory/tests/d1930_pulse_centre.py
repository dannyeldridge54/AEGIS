"""D1930: first Loom pulse (rule 6h), from the middle outwards. Ring 0: the shared rung step at the median (0.027).
Ring 1: alpha_s with a self-consistent AMSB spectrum, for S at rho (m3/2 2.58e5) and S at i (7.6e5)."""
import json, math, cmath, sys
sys.path.insert(0, 'tools/loom'); sys.path.insert(0, 'tools/weave_cm')
from triangulate import bracket, fixed_point
from weave_tools import weave_rg2
src = open('theory/tests/d1925_onespurion.py').read().split('u = U(0.0457')[0]; exec(src)
out = {}
# ---- ring 0: one-spurion window around the median step 0.027
has = lambda a: len(scan(a)) > 0
logL, logH = [], []
assert has(0.027) and not has(0.0234) and not has(0.0311)
lo_edge, lo_w, lo_n = bracket(has, 0.0234, 0.027, 1e-5, log=logL)       # f flips False -> True
hi_edge, hi_w, hi_n = bracket(has, 0.027, 0.0311, 1e-5, log=logH)       # True -> False
ph = cmath.phase(U(0.0457 * cmath.exp(1j * math.radians(49))))
inside = [lo_edge + (hi_edge - lo_edge) * k / 4 for k in (1, 2, 3)]
nat = []
for a in inside:
    fits = scan(a); best = max((natural(a * cmath.exp(1j * ph), *f, N=2000, seed=30) for f in fits), key=lambda t: t[0])
    nat.append(dict(abs_u=a, n_fit=len(fits), f7=best[0], fJ=best[1]))
targets = dict(median_step=0.027, u_d_D1828=0.02587, u_lepton_D1832=0.0253, neutrino_theta=0.0292)
out['ring0'] = dict(window=[lo_edge, hi_edge], edge_res=[lo_w, hi_w], rounds=[lo_n, hi_n], inside=nat,
                    contains={k: lo_edge <= v <= hi_edge for k, v in targets.items()},
                    dist_from_window={k: (0 if lo_edge <= v <= hi_edge else min(abs(v - lo_edge), abs(v - hi_edge))) for k, v in targets.items()},
                    log_lo=logL, log_hi=logH)
# ---- ring 1: alpha_s, self-consistent gluino
MZ = 91.1876
def a3_at(mu, a_s):   # one-loop SM running from MZ to mu (n_f=6 above m_t ~ fine at this precision)
    return 1 / (1 / a_s + 7 / (2 * math.pi) * math.log(mu / MZ))
def spectrum(a_s, m32):
    mg = m32 * 3 / (4 * math.pi) * 0.092   # start
    for _ in range(50): mg = 3 * a3_at(mg, a_s) / (4 * math.pi) * m32
    mw = m32 * (1 / 29.9) / (4 * math.pi); ms = 4.7e5 * m32 / 2.58e5
    return mg, mw, ms
def one_loop(mw, mg, ms):
    aem, s2 = 127.95, 0.23122; x0 = [0.6 * (1 - s2) * aem, s2 * aem]
    SM1, MS1 = [41 / 10, -19 / 6, -7], [33 / 5, 1, -3]
    def b(mu):
        if mu >= ms: return MS1
        bb = list(SM1)
        if mu >= mw: bb[1] += 4 / 3
        if mu >= mg: bb[2] += 2
        return bb
    pts = sorted([MZ, mw, mg, ms])
    def inv(mu):
        x = [x0[0], x0[1], 0.0]; t = [p for p in pts if p < mu] + [mu]
        for p0, p1 in zip(t, t[1:]):
            bb = b(math.sqrt(p0 * p1)); x = [x[i] - bb[i] / (2 * math.pi) * math.log(p1 / p0) for i in range(3)]
        return x
    lo, hi = 1e12, 1e18
    for _ in range(80):
        mid = math.sqrt(lo * hi); x = inv(mid); lo, hi = (mid, hi) if x[0] > x[1] else (lo, mid)
    x = inv(mid); return 1 / (x[0] - x[2])     # alpha_3(MZ) with alpha_3(M12) = alpha_12
def readers(m32):
    def ga(a_s): mg, mw, ms = spectrum(a_s, m32); return weave_rg2({'m_wino': mw, 'm_gluino': mg, 'm_scalar': ms})['alpha_s_unif']
    def gb(a_s): mg, mw, ms = spectrum(a_s, m32); return one_loop(mw, mg, ms)
    def gc(a_s): mg, mw, ms = spectrum(a_s, m32); return weave_rg2({'m_wino': mw, 'm_gluino': mg, 'm_scalar': 4.7e5})['alpha_s_unif']
    return [ga, gb, gc]
for tag, m32 in (('S_at_rho', 2.58e5), ('S_at_i', 7.6e5)):
    log = []; c, s, n = fixed_point(readers(m32), 0.1147, 1e-5, log=log)
    mg, mw, ms = spectrum(c, m32)
    out['ring1_' + tag] = dict(alpha_s=c, spread=s, rounds=n, pull=(c - 0.1180) / 0.0009, gluino=mg, wino=mw, scalars=ms, log=log)
print(json.dumps({k: (v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items() if not kk.startswith('log')}) for k, v in out.items()}, indent=1, default=float))
json.dump(out, open('field_tests/results/d1930_pulse_centre.json', 'w'), indent=1, default=float)
