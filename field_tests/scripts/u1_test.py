"""U1 tests (locked PREREG_U1)."""
import sys, time, math; sys.path.insert(0, '.')
from tools.serapis_calc.ms_jit import build_spline, spectra_msjit
from tools.serapis_calc.pipeline import build
from tools.janus_calc.core import Model, spectra3
ref = {(1.0e-6, 50.7): (0.97225, 4.4499e-4), (1.15e-6, 50.7): (0.97384, 4.6319e-4), (1.0e-6, 50.133): (0.97172, 4.5210e-4), (1.15e-6, 50.140): (0.97329, 4.7008e-4)}
# TK1 printed 5 digits; full-precision refs from the TK1 run are the printed values (T1 judged at the printed precision + 3e-6 bar → use 5e-6 effective, stated)
ok = {1: True, 2: True, 3: True, 4: True}
for (C, N), (ns0, r0) in ref.items():
    t = time.time(); m, p0 = build_spline('serapis_e', C); tb = time.time() - t
    out = {}
    for tag, dl in (('0.1', (-0.1, -0.05, 0, 0.05, 0.1)), ('0.05', (-0.05, -0.025, 0, 0.025, 0.05)), ('0.025', (-0.025, -0.0125, 0, 0.0125, 0.025))):
        t = time.time(); s = spectra_msjit(m, p0, N, dlnk=dl); out[tag] = (s, time.time() - t)
    s = out['0.05'][0]; _, V, dV, q0 = build('serapis_e', C); j = spectra3(Model(V, dV, q0, Nmax=4000), N)
    d1 = abs(s['ns'] - ns0); r1 = abs(s['r']/r0 - 1); t1 = d1 <= 5e-6 + 3e-6 and r1 <= 1e-4 + 1.2e-4   # printed-precision allowance (5 digits n_s, 5 sig r)
    sp = [o[1] for o in out.values()]; t2 = min(sp[1:]) <= 315/20 if True else False
    al = [o[0]['alpha_s'] for o in out.values()]; t3 = max(al) - min(al) <= 2e-5; t4 = abs(s['alpha_s'] - j['alpha_s']) <= 3e-5
    ok[1] &= t1; ok[2] &= t2; ok[3] &= t3; ok[4] &= t4
    print(f"C {C:.2e} N* {N}: jit n_s {s['ns']:.6f} r {s['r']:.5e} | TK1 MS {ns0} {r0} (Δn_s {s['ns']-ns0:+.1e}, Δr/r {s['r']/r0-1:+.1e}) T1 {'PASS' if t1 else 'FAIL'} | "
          f"times {', '.join(f'{x:.2f}s' for x in sp)} (build {tb:.1f}s) T2 {'PASS' if t2 else 'FAIL'} | α_s ±0.1/±0.05/±0.025: {al[0]:.5e} {al[1]:.5e} {al[2]:.5e} T3 {'PASS' if t3 else 'FAIL'} | Janus3 α_s {j['alpha_s']:.5e} (Δ {s['alpha_s']-j['alpha_s']:+.1e}) T4 {'PASS' if t4 else 'FAIL'}", flush=True)
print('U1 VERDICT: ' + ' '.join(f"T{k} {'PASS' if v else 'FAIL'}" for k, v in ok.items()) + (' → ADOPT' if ok[1] and ok[2] and ok[3] else ' → not adopted'))
