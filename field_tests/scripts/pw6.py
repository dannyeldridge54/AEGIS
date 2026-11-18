import sys, math, time; sys.path.insert(0, '.')
from tools.serapis_calc.pipeline import predict_fast
TR, g = 7.389e8, 228.75
P_of = lambda C: 15*4/(64*math.pi**6*C)
out = open('field_tests/results/pw6_inverse_meter.txt', 'w')
def say(s): print(s, flush=True); out.write(s + '\n'); out.flush()
cache = {}
def ns(lnC):
    if lnC not in cache: cache[lnC] = predict_fast('serapis_e', math.exp(lnC), TR, 1.0, g)
    return cache[lnC]
t0 = time.time(); ok = True
for tgt in (0.970, 0.972, 0.974, 0.976, 0.978):
    Plin = 780.1*math.exp(-(tgt - 0.974393)/0.011711)
    x0 = math.log(1.25e-6) + (tgt - 0.974393)/0.011711; x1 = x0 + 0.02
    f0, f1 = ns(x0)['ns'] - tgt, ns(x1)['ns'] - tgt
    for _ in range(8):
        x2 = x1 - f1*(x1 - x0)/(f1 - f0); x0, f0 = x1, f1; x1 = x2; f1 = ns(x1)['ns'] - tgt
        if abs(f1) <= 2e-6: break
    R = ns(x1); Pex = P_of(math.exp(x1)); dev = Plin/Pex - 1
    if 0.972 <= tgt <= 0.976 and abs(dev) > 0.03: ok = False
    say(f"n_s {tgt:.3f}: P_lin {Plin:.1f} | exact C {math.exp(x1):.4e} P {Pex:.1f} (lin/exact−1 {dev:+.2%}) N* {R['Nstar']:.3f} n_s {R['ns']:.6f} r {R['r']:.4e} α_s {R['alpha_s']:.4e}")
for P in (560.0, 975.0):
    say(f"natural edge P {P}: linear n_s {0.974393 - 0.011711*math.log(P/780.1):.5f}")
say(f"PW6 expectation (≤3 % for n_s 0.972–0.976): {'PASS' if ok else 'FAIL'}  ({time.time()-t0:.0f} s)")
