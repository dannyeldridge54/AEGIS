"""W1 (locked PREREG_W1_recompute)."""
import sys, json, time; sys.path.insert(0, '.')
from tools.serapis_calc.pipeline import predict, build
from tools.serapis_calc.ms import Background, spectra
t0 = time.time(); B = predict('serapis_e', C=1.15e-6, TR=1e7); L = [f"baseline: N* {B['Nstar']:.3f} n_s {B['ns']:.6f} r {B['r']:.4e} a_s {B['alpha_s']:.4e}"]; print(L[-1], flush=True)
m, V, dV, p0 = build('serapis_e', 1.15e-6); bg = Background(V, dV, p0)
def d(x): return (x['ns'] - B['ns'], x['r']/B['r'] - 1, x['alpha_s'] - B['alpha_s'])
res = {}
res['w_N'] = [d(spectra(bg, B['Nstar'] + s)) for s in (1, -1)]
res['w_C'] = [d(predict('serapis_e', C=1.15e-6*(1 + 0.1*s), TR=1e7)) for s in (1, -1)]
res['w_T'] = [d(predict('serapis_e', C=1.15e-6, TR=1e7*10**s)) for s in (1, -1)]
sig = 0.0030; out = {}
for k, (p, mm) in res.items():
    asym = abs(p[0] + mm[0])/max(abs(p[0]), abs(mm[0]), 1e-15); out[k] = dict(plus=p, minus=mm, strength=max(abs(p[0]), abs(mm[0]))/sig, asym=asym)
    L.append(f"{k}: +wave dn_s {p[0]:+.2e} dr/r {p[1]:+.2e} da {p[2]:+.2e} | −wave dn_s {mm[0]:+.2e} dr/r {mm[1]:+.2e} da {mm[2]:+.2e} | strength {out[k]['strength']:.3f} σ_SPA | asymmetry {asym:.2f}{' NONLINEAR' if asym > 0.2 else ''}")
    print(L[-1], flush=True)
L.append(f"n_s distance: SPA {(B['ns'] - 0.9684)/0.0030:+.2f}σ, SPA+DESI {(B['ns'] - 0.9728)/0.0027:+.2f}σ")
L.append("ordering nstar_e vs bhk_tilt: " + ("CONFIRMED" if out['w_N']['strength'] > out['w_C']['strength'] else "REVERSED") + f" ({time.time()-t0:.0f} s)")
open('field_tests/results/w1_recompute.txt', 'w').write('\n'.join(L) + '\n'); json.dump(out, open('docs/web/w1.json', 'w'), indent=1); print('\n'.join(L[-2:]))
