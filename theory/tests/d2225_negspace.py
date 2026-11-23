"""D2225 part A (PREREG_D2225_NEGSPACE): DKL threshold on the model's modular vacuum tau = i (primary) and rho; universal flux; every (Db32, Db12)."""
import itertools, json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..', '..'); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(ROOT, 'tools', 'rings'))
import mpmath
import d2224_strand_engine as E
import rings as G
def L(tau):
    tau = mpmath.mpc(tau); q = mpmath.exp(2j * mpmath.pi * tau); eta = mpmath.exp(2j * mpmath.pi * tau / 24) * mpmath.qp(q)
    return float(-mpmath.log(tau.imag * abs(eta) ** 4))
SIG = math.sqrt(0.0009 ** 2 + 0.00057 ** 2); MMIN = 1.145e16 * (2.4 / 16) ** 0.25
a0, _ = E.alpha_s(0, 0); a32, _ = E.alpha_s(0, -0.25); a12, _ = E.alpha_s(0.3, 0)
h32, h12 = (1 / a32 - 1 / a0) / -0.25, (1 / a12 - 1 / a0) / 0.3
out = dict(guard=a0)
for name, tau in (('tau_i', 1j), ('rho', complex(-0.5, math.sqrt(3) / 2))):
    Lv = L(tau); rows = []
    for b32, b12 in itertools.product(range(-6, 7), range(-6, 7)):
        d32, d12 = b32 * Lv / (4 * math.pi), b12 * Lv / (4 * math.pi)
        r = dict(db32=b32, db12=b12, d32=round(d32, 5), d12=round(d12, 5))
        if abs(1 / a0 + h32 * d32 + h12 * d12 - 1 / 0.118) > 0.30: r['prefiltered_out'] = True; rows.append(r); continue
        a, M = E.alpha_s(d12, d32); clamped = M < 1.01e10 or M > 0.99e20
        hoy = bool(G.W.weave_nuclear({'dalpha_s': a - 0.118, 'alpha_s': 0.118})['inside'])
        pull = (a - 0.118) / SIG
        r.update(alpha_s=round(a, 6), pull=round(pull, 3), M12=float(f'{M:.4g}'), clamped=clamped, hoyle=hoy,
                 stable_0p1MP=bool(not clamped and abs(pull) <= 2 and MMIN <= M <= 2.4e17 and hoy), stable_MP=bool(not clamped and abs(pull) <= 2 and MMIN <= M <= 2.4e18 and hoy))
        rows.append(r)
    st = [r for r in rows if r.get('stable_0p1MP')]
    out[name] = dict(L=Lv, n_pairs=len(rows), n_stable_0p1MP=len(st), n_stable_MP=sum(bool(r.get('stable_MP')) for r in rows), stable=st,
                     evaluated=[r for r in rows if 'alpha_s' in r])
out['reading_tau_i'] = ('CONDITIONAL: forces ring balances at the model vacuum tau = i if the Z2xZ6p visible N=2 spectrum gives one of the stable (Db32, Db12)'
                        if out['tau_i']['n_stable_0p1MP'] else 'excluded at tau = i')
json.dump(out, open(os.path.join(ROOT, 'field_tests', 'results', 'd2225_negspace.json'), 'w'), indent=1)
for k in ('tau_i', 'rho'): print(k, 'L', round(out[k]['L'], 4), 'stable', out[k]['n_stable_0p1MP'], '/', out[k]['n_pairs'], [(r['db32'], r['db12'], r['alpha_s'], r['pull'], r['M12']) for r in out[k]['stable']])
print(out['reading_tau_i'])
