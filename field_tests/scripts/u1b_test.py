import sys, time, numpy as np; sys.path.insert(0, '.')
from tools.serapis_calc.ms_jit import build_spline, spectra_msjit
from tools.serapis_calc.pipeline import build
from tools.janus_calc.core import Model, spectra3
ref = {(1.0e-6, 50.7): (0.97225, 4.4499e-4), (1.15e-6, 50.7): (0.97384, 4.6319e-4), (1.0e-6, 50.133): (0.97172, 4.5210e-4), (1.15e-6, 50.140): (0.97329, 4.7008e-4)}
g1 = tuple(np.linspace(-0.1, 0.1, 9)); g2 = tuple(np.linspace(-0.05, 0.05, 9)); ok = [True]*5
for (C, N), (ns0, r0) in ref.items():
    m, p0 = build_spline('serapis_e', C); spectra_msjit(m, p0, N, dlnk=(0.0,), bd=200)  # compile
    t = time.time(); a = spectra_msjit(m, p0, N, dlnk=g1, bd=4000); ta = time.time() - t
    b = spectra_msjit(m, p0, N, dlnk=g2, bd=4000); c = spectra_msjit(m, p0, N, dlnk=g1, bd=8000)
    _, V, dV, q0 = build('serapis_e', C); j = spectra3(Model(V, dV, q0, Nmax=4000), N)
    t1 = abs(a['ns'] - ns0) <= 1e-5 and abs(a['r']/r0 - 1) <= 2e-4; t2 = ta <= 15; t3 = abs(a['alpha_s'] - b['alpha_s']) <= 2e-5 and abs(a['alpha_s'] - c['alpha_s']) <= 2e-5; t4 = abs(a['alpha_s'] - j['alpha_s']) <= 3e-5
    for i, v in enumerate((t1, t2, t3, t4), 1): ok[i] &= v
    print(f"C {C:.2e} N* {N}: n_s {a['ns']:.6f} (TK1 {ns0}) r {a['r']:.5e} | {ta:.1f}s | α_s ±0.1 {a['alpha_s']:.5e}, ±0.05 {b['alpha_s']:.5e}, bd8000 {c['alpha_s']:.5e} | Janus3 {j['alpha_s']:.5e} (Δ {a['alpha_s']-j['alpha_s']:+.1e}) | T1 {t1} T2 {t2} T3 {t3} T4 {t4}", flush=True)
print('U1b VERDICT: ' + ' '.join(f"T{i} {'PASS' if ok[i] else 'FAIL'}" for i in range(1, 5)) + (' → ADOPT' if all(ok[1:4]) else ' → not adopted'))
