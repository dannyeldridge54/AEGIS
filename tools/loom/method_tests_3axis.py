"""D1976: the three method tests re-pulsed on THREE AXES in tandem (Danny 18:08) — S (time/cosmology: T_R), T (scales: m3/2), U (matter: u);
M_N tied to its derived value (no longer a knob). Bounds now enter as DATA (one-sided penalties): wino >= 660 GeV, gravitino-box Omega_w <= 0.12,
M_N window (fixed, automatically met). Data: n_s, alpha_s, ln Y_B, quark u, wino bound, gravitino box  =>  6 data, 3 knobs, dof = 3.
Each test is PULSED: re-run with three noise seeds (three readings) and repeated until the headline number moves < 0.01 for 7 pulses in a row."""
import json, math, sys
import numpy as np
from scipy.optimize import least_squares
m_phi = 4.93e12
def raw(p):
    m32, TR, u = 2.58e5 * math.exp(p[0]), 3.7e8 * math.exp(p[1]), 0.02663 * math.exp(p[2]); MN = 1.844e11
    Ns = 50.3 + math.log(TR / 3.7e8) / 3; ns = 1 - 0.0294 * 50.3 / Ns
    a_s = 0.11401 * (m32 / 2.58e5) ** (-0.0254)
    Br = 0.0233; eps = 2.281e-5
    Y = (28 / 79) * 1.5 * (TR / m_phi) * eps * Br
    M2 = 686.5 * m32 / 2.58e5; Om = 0.017 * (TR / 3.2e8) * (M2 / 660) ** 1.5
    return ns, a_s, math.log(Y), u, M2, Om
SIG = np.array([0.0027, 0.0011, 0.10, 0.0008])
REAL = np.array([0.9728, 0.1180, math.log(0.87e-10), 0.02663])
def resid(p, data):
    ns, a_s, lY, u, M2, Om = raw(p)
    r = list((np.array([ns, a_s, lY, u]) - data) / SIG)
    r.append(max(0.0, (660 - M2) / 20.0))           # one-sided: wino bound, 20 GeV soft width
    r.append(max(0.0, (Om - 0.12) / 0.012))         # one-sided: gravitino box, 10 % soft width
    return np.array(r)
def fit(data, drop=None):
    f = (lambda p: np.delete(resid(p, data), drop)) if drop is not None else (lambda p: resid(p, data))
    r = least_squares(f, np.zeros(3), bounds=(-3, 3)); return r.x, r.fun
def T1(seed, n=150):
    rng = np.random.default_rng(seed); ok = []
    for _ in range(n):
        truth = rng.uniform(-0.4, 0.4, 3)
        while True:                                   # truths must respect the bounds (physical planted worlds)
            ns, a_s, lY, u, M2, Om = raw(truth)
            if M2 >= 660 and Om <= 0.12: break
            truth = rng.uniform(-0.4, 0.4, 3)
        tv = np.array([ns, a_s, lY, u]); data = tv + rng.normal(0, SIG)
        x, _ = fit(data); pv = np.array(raw(x)[:4]); ok.append(np.all(np.abs(pv - tv) <= 2 * SIG))
    return float(np.mean(ok))
def T2(seed, n=150):
    rng = np.random.default_rng(seed); fb = []
    for _ in range(n):
        data = rng.uniform(REAL - 5 * SIG, REAL + 5 * SIG); x, r = fit(data); fb.append(np.all(np.abs(r) <= 2))
    return float(np.mean(fb))
def pulse(test):
    vals, nulls, seed, prev = [], 0, 10, None
    while nulls < 7 and seed < 60:
        reads = [test(seed + j) for j in range(3)]; seed += 3
        vals += reads; c = float(np.mean(vals))
        nulls = nulls + 1 if (prev is not None and abs(c - prev) < 0.01) else 0; prev = c
    return dict(centre=float(np.mean(vals)), spread=float(np.std(vals)), readings=len(vals), pulses_to_converge=seed // 3)
out = {}
out['T1_coverage'] = pulse(T1)
out['T2_false_balance'] = pulse(T2)
x, r = fit(REAL); ns, a_s, lY, u, M2, Om = raw(x)
out['T3'] = dict(dof=6 - 3, chi2=float(np.sum(r ** 2)), knobs=dict(m32=2.58e5 * math.exp(x[0]), T_R=3.7e8 * math.exp(x[1]), u=0.02663 * math.exp(x[2])),
                 wino=M2, Omega_w=Om, pulls=dict(zip(['n_s', 'alpha_s', 'lnY', 'u', 'wino_bound', 'box'], map(float, r))))
hold = {}
for i, nm in enumerate(['n_s', 'alpha_s', 'ln Y_B']):
    xi, _ = fit(REAL, drop=i); pv = raw(xi)[i]; hold[nm] = dict(predicted=float(pv), real=float(REAL[i]), pull=float((pv - REAL[i]) / SIG[i]))
out['T3']['hold_out'] = hold
out['verdicts'] = dict(T1='PASS' if out['T1_coverage']['centre'] >= 0.9 else 'FAIL', T2='PASS' if out['T2_false_balance']['centre'] <= 0.2 else 'FAIL',
                       T3='dof %d; balanced (chi2/dof <= 1)? %s' % (3, out['T3']['chi2'] / 3 <= 1))
print(json.dumps(out, indent=1, default=float)); json.dump(out, open('field_tests/results/d1976_method_3axis.json', 'w'), indent=1, default=float)
