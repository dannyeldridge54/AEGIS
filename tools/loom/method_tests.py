"""Tests OF the method (Danny 18:04: 'what would scientists do to test this method'). Standard validation for any fitting/balancing engine:
T1 INJECTION–RECOVERY: plant a known 'truth' (knobs), make fake data = model(truth) + noise, run the balancer aimed at the DATA CENTRE,
   check it recovers the truth (coverage should be ~95 % at 2σ; bias ~0).
T2 NULL / FALSE-BALANCE RATE: feed data the model did NOT generate (random values inside the observed ranges); count how often the balancer
   still reports 'balance' (χ²/dof ≤ 1 or all pulls ≤ 2). A high rate means the knobs can balance ANYTHING, so balance is not evidence.
T3 DEGREES OF FREEDOM + HOLD-OUT on the REAL data centres: dof = data points − free knobs; fit without one observable, predict it.
Model: the resonance engine's observables (D1972): n_s(T_R), alpha_s(m3/2, single stack), Y_B(T_R, M_N), quark-window centre(u); knobs m3/2, T_R, M_N, u."""
import json, math, random
import numpy as np
from scipy.optimize import least_squares
m_phi = 4.93e12
def model(p):                                   # p = log knobs relative to derived: [ln m32/2.58e5, ln TR/3.7e8, ln MN/1.844e11, ln u/0.02663]
    m32, TR, MN, u = 2.58e5 * math.exp(p[0]), 3.7e8 * math.exp(p[1]), 1.844e11 * math.exp(p[2]), 0.02663 * math.exp(p[3])
    Ns = 50.3 + math.log(TR / 3.7e8) / 3; ns = 1 - 0.0294 * 50.3 / Ns
    a_s = 0.11401 * (m32 / 2.58e5) ** (-0.0254)
    Br = 0.0233 * (MN / 1.844e11) ** 2; eps = 2.281e-5 * MN / 1.844e11
    Y = (28 / 79) * 1.5 * (TR / m_phi) * eps * Br
    return np.array([ns, a_s, math.log(Y), u])
NAMES = ['n_s', 'alpha_s', 'ln Y_B', 'quark u']
SIG = np.array([0.0027, 0.0011, 0.10, 0.0008])          # data errors (Y_B: 10 %; u: window half-width)
REAL = np.array([0.9728, 0.1180, math.log(0.87e-10), 0.02663])
def fit(data, mask=None, x0=None):
    m = np.ones(4, bool) if mask is None else mask
    f = lambda p: ((model(p) - data) / SIG)[m]
    r = least_squares(f, np.zeros(4) if x0 is None else x0, bounds=(-3, 3))
    return r.x, float(np.sum(r.fun ** 2)), int(m.sum())
rng = np.random.default_rng(4); out = {}
# T1 injection-recovery
cover, bias = [], []
for _ in range(200):
    truth = rng.uniform(-0.5, 0.5, 4)
    data = model(truth) + rng.normal(0, SIG)
    x, chi2, n = fit(data)
    pred = model(x); true_obs = model(truth)
    cover.append(np.all(np.abs(pred - true_obs) <= 2 * SIG)); bias.append(x - truth)
out['T1'] = dict(coverage_2sigma=float(np.mean(cover)), mean_knob_bias=np.mean(bias, 0).round(4).tolist(),
                 knob_scatter=np.std(bias, 0).round(4).tolist(),
                 note='coverage of the OBSERVABLES; knob scatter shows which knobs are actually pinned by the data')
# T2 false-balance on data the model did not generate
lo = REAL - 5 * SIG; hi = REAL + 5 * SIG
fb = []
for _ in range(200):
    data = rng.uniform(lo, hi)
    x, chi2, n = fit(data)
    fb.append(np.all(np.abs((model(x) - data) / SIG) <= 2))
out['T2'] = dict(false_balance_rate=float(np.mean(fb)), note='fraction of random data sets (±5σ around the real centres) the balancer still "balances"')
# T3 real data: dof and hold-out
x, chi2, n = fit(REAL)
out['T3'] = dict(dof=4 - 4, chi2_all=chi2, knobs_fitted=dict(m32=2.58e5 * math.exp(x[0]), T_R=3.7e8 * math.exp(x[1]), M_N=1.844e11 * math.exp(x[2]), u=0.02663 * math.exp(x[3])))
hold = {}
for i in range(4):
    m = np.ones(4, bool); m[i] = False
    xi, c, n = fit(REAL, m)
    hold[NAMES[i]] = dict(predicted=float(model(xi)[i]), real=float(REAL[i]), pull=float((model(xi)[i] - REAL[i]) / SIG[i]))
out['T3']['hold_out'] = hold
print(json.dumps(out, indent=1, default=float)); json.dump(out, open('field_tests/results/d1974_method_tests.json', 'w'), indent=1, default=float)
