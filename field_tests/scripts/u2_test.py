import sys, time; sys.path.insert(0, '.')
from tools.serapis_calc.pipeline import predict_fast
ok = [True]*4
for C, TR, N0, ns0, r0, a0 in ((1.0e-6, 6.6e8, 50.133, 0.97172, 4.5210e-4, None), (1.15e-6, 2.0e10, 51.272, 0.974380, 4.56395e-4, -9.4559e-4)):
    t = time.time(); p = predict_fast('serapis_e', C, TR); dt = time.time() - t
    t1 = abs(p['Nstar'] - N0) <= 0.002 and abs(p['ns'] - ns0) <= 1e-5 and abs(p['r']/r0 - 1) <= 2e-4; t2 = dt <= 40; t3 = True if a0 is None else abs(p['alpha_s'] - a0) <= 5e-6
    ok[1] &= t1; ok[2] &= t2; ok[3] &= t3
    print(f"C {C:.2e} T_R {TR:.1e}: N* {p['Nstar']:.4f} (TK1 {N0}) n_s {p['ns']:.6f} ({ns0}) r {p['r']:.5e} ({r0}) α_s {p['alpha_s']:.5e} ({a0}) | {dt:.1f}s | T1 {t1} T2 {t2} T3 {t3}", flush=True)
print('U2 VERDICT: ' + ' '.join(f"T{i} {'PASS' if ok[i] else 'FAIL'}" for i in (1, 2, 3)) + (' → ADOPT' if ok[1] and ok[2] else ' → not adopted'))
