"""Inverse string meter (PW6 D1268; tool T1): a measured n_s -> C and Im S·Im ρ for SERAPIS-E at the leptogenesis T_R.
Table: exact inversion (Janus N* + U1b exact MS) at T_R 7.389e8 GeV, MSSM g* 228.75, N_eff = 4. Status: postulate (scored on future data)."""
import math
TABLE = [  # ns, C, P, Nstar, r, alpha_s  (field_tests/results/pw6_inverse_meter.txt)
 (0.970, 8.2928e-07, 1175.9, 50.163, 4.3217e-04, -8.9896e-04),
 (0.972, 1.0232e-06, 953.0, 50.171, 4.5436e-04, -9.4315e-04),
 (0.974, 1.2131e-06, 803.8, 50.180, 4.7744e-04, -9.8936e-04),
 (0.976, 1.3990e-06, 697.1, 50.188, 5.0145e-04, -1.0378e-03),
 (0.978, 1.5807e-06, 616.9, 50.196, 5.2638e-04, -1.0871e-03)]
TR0, G = 7.389e8, 228.75
P_of = lambda C: 15*4/(64*math.pi**6*C)
def _interp(ns):
    T = TABLE; i = 0
    while i < len(T) - 2 and T[i + 1][0] < ns: i += 1
    a, b = T[i], T[i + 1]; f = (ns - a[0])/(b[0] - a[0])
    L = lambda k: math.exp(math.log(a[k]) + f*(math.log(b[k]) - math.log(a[k])))
    li = lambda k: a[k] + f*(b[k] - a[k])
    return dict(ns=ns, C=L(1), P=L(2), Nstar=li(3), r=li(4), alpha_s=li(5), engine='PW6 table (log-interp)')
def _exact(ns, T_R):
    from .pipeline import predict_fast
    cache = {}
    def f(x):
        if x not in cache: cache[x] = predict_fast('serapis_e', math.exp(x), T_R, 1.0, G)
        return cache[x]['ns'] - ns
    x0 = math.log(1.25e-6) + (ns - 0.974393)/0.011711; x1 = x0 + 0.02; f0, f1 = f(x0), f(x1)
    for _ in range(8):
        x2 = x1 - f1*(x1 - x0)/(f1 - f0); x0, f0 = x1, f1; x1 = x2; f1 = f(x1)
        if abs(f1) <= 2e-6: break
    R = cache[x1]; C = math.exp(x1)
    return dict(ns=ns, C=C, P=P_of(C), Nstar=R['Nstar'], r=R['r'], alpha_s=R['alpha_s'], engine='exact secant (predict_fast)')
def meter(ns, ns_sigma=None, T_R=TR0, exact=False):
    ns = float(ns); use_exact = exact or abs(T_R/TR0 - 1) > 1e-6 or not (TABLE[0][0] <= ns <= TABLE[-1][0])
    out = _exact(ns, T_R) if use_exact else _interp(ns)
    if ns_sigma:
        lo = meter(ns + ns_sigma, None, T_R, exact)['P']; hi = meter(ns - ns_sigma, None, T_R, exact)['P']
        out['P_range'] = [lo, hi]; out['P_rel_sigma'] = 0.5*(hi - lo)/out['P']
    out.update(T_R=T_R, N_eff=4, status='postulate (PW6, D1268)'); return out
